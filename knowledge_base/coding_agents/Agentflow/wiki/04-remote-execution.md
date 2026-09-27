> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Remote execution: SSH, EC2, ECS runners
**In one sentence:** Agentflow can run an agent step on your own machine, in a local Docker container, or on AWS cloud machines using SSH (Secure Shell, remote login protocol), EC2 (Elastic Compute Cloud, rentable virtual machines on AWS), and ECS (Elastic Container Service, running Docker containers on AWS).

## Key points
- Each node picks its machine with `target={"kind": ...}`; the registry maps `local`, `container`, `ssh`, `ec2`, and `ecs` to a runner class (`agentflow/runners/registry.py:13`).
- SSH (Secure Shell, remote login protocol) execution shells out to the system `ssh` binary with no extra Python dependency, using `BatchMode=yes` and `StrictHostKeyChecking=accept-new` (`agentflow/runners/ssh.py:23`, `agentflow/runners/ssh.py:34`).
- EC2 (Elastic Compute Cloud, rentable virtual machines on AWS) by default launches one fresh virtual machine per node, waits for SSH (Secure Shell, remote login protocol), runs the command, then terminates the machine (`agentflow/runners/ec2.py:25`, `agentflow/runners/ec2.py:76`, `agentflow/runners/ec2.py:250`).
- Nodes that set the same `shared` name reuse one EC2 (Elastic Compute Cloud, rentable virtual machines on AWS) machine; the manager launches on first use, returns the same address on later use, and terminates only after the last user releases it (`agentflow/runners/ec2.py:234`, `agentflow/cloud/shared.py:54`, `agentflow/cloud/shared.py:96`).
- EC2 (Elastic Compute Cloud, rentable virtual machines on AWS) auto-discovery fills in a missing AMI (Amazon Machine Image, a template for a virtual machine), SSH (Secure Shell, remote login protocol) key pair, and VPC (Virtual Private Cloud, your private network section in AWS) network when you omit them (`agentflow/runners/ec2.py:109`, `agentflow/cloud/aws.py:67`, `agentflow/cloud/aws.py:85`, `agentflow/cloud/aws.py:11`).
- ECS (Elastic Container Service, running Docker containers on AWS) Fargate builds a Docker image with the agent tools, pushes it to ECR, registers a task definition, and polls CloudWatch logs until the task stops (`agentflow/runners/ecs.py:25`, `agentflow/runners/ecs.py:133`, `agentflow/runners/ecs.py:199`).
- Local runs the command directly as a child process while container wraps the same local logic in a `docker run --rm` call with mounted work folders; container is a subclass of the local runner (`agentflow/runners/local.py:278`, `agentflow/runners/container.py:18`, `agentflow/runners/container.py:11`).
- Zero-config is partial: you can omit AMI (Amazon Machine Image), key, subnets, and cluster, but you still need AWS credentials, boto3, a default VPC (Virtual Private Cloud), Docker for ECS (Elastic Container Service) builds, and agent login keys forwarded from your machine (`agentflow/cloud/aws.py:22`, `agentflow/runners/ec2.py:37`, `agentflow/runners/ecs.py:48`, `agentflow/runners/ec2.py:143`).

---
## How a node picks a runner
Each pipeline step sets a `target` dictionary with a `kind` field. The registry creates one runner object per kind (`agentflow/runners/registry.py:13`).
Local helpers that shape shell commands live in the large shell module, and the local runner only imports three small helpers from it: rendering `shell_init`, checking for a `{command}` placeholder, and detecting interactive bash (`agentflow/runners/local.py:9`, `agentflow/local_shell.py:131`, `agentflow/local_shell.py:138`, `agentflow/local_shell.py:2118`).

## SSH runner
The SSH (Secure Shell, remote login protocol) runner builds a remote shell line of the form `cd <workdir> && <env> <command>` and passes it to `ssh destination remote_script` (`agentflow/runners/ssh.py:44`, `agentflow/runners/ssh.py:49`).
It honors a non-default port with `-p` and an identity file with `-i` (`agentflow/runners/ssh.py:35`, `agentflow/runners/ssh.py:37`).
Execution streams stdout and stderr lines, supports timeout from `node.timeout_seconds`, and maps timeout to exit 124 and cancel to exit 130 (`agentflow/runners/ssh.py:109`, `agentflow/runners/ssh.py:135`).

## EC2 runner
The EC2 (Elastic Compute Cloud, rentable virtual machines on AWS) runner launches with `run_instances`, tags the machine `agentflow-<node-id>`, optionally adds install script as `UserData` and spot pricing, then waits for running plus status checks before reading its IP address (`agentflow/runners/ec2.py:39`, `agentflow/runners/ec2.py:70`, `agentflow/runners/ec2.py:76`).
Real remote work is delegated to the SSH (Secure Shell, remote login protocol) runner against a short-lived SSH (Secure Shell, remote login protocol) target built from the new IP, username, and identity file (`agentflow/runners/ec2.py:153`, `agentflow/runners/ec2.py:194`).
Before running, it merges your local agent keys into the environment and prepends an auth-setup shell snippet so the remote CLI finds its login (`agentflow/runners/ec2.py:143`, `agentflow/runners/ec2.py:182`, `agentflow/cloud/installer.py:68`).
Verbatim EC2 target spec from the example:

```
        target={
            "kind": "ec2",
            "region": "ap-northeast-1",
            "instance_type": "t3.micro",
            "ami": "ami-0d52744d6551d851e",
            "username": "ubuntu",
            "install_agents": ["codex"],
        },
```

## Shared EC2 instances
Setting `shared` to the same string across nodes makes them share one machine instead of launching one per node (`agentflow/runners/ec2.py:231`).
The manager keeps a reference count, pre-registered from the expected node count, so the machine survives between sequential steps and is cleaned only when the count reaches zero (`agentflow/cloud/shared.py:34`, `agentflow/cloud/shared.py:66`, `agentflow/cloud/shared.py:96`).
Cleanup can snapshot the machine to a new AMI (Amazon Machine Image) and either terminate it or leave it running per the `terminate` flag (`agentflow/cloud/shared.py:103`, `agentflow/cloud/shared.py:109`, `agentflow/runners/ec2.py:265`).
A final `cleanup` pass terminates leftovers from crashed nodes (`agentflow/cloud/shared.py:118`).

## ECS Fargate runner
ECS (Elastic Container Service, running Docker containers on AWS) Fargate needs no server management: Agentflow ensures the cluster, log group, and execution IAM role exist, then registers and runs one task (`agentflow/runners/ecs.py:74`, `agentflow/runners/ecs.py:86`, `agentflow/runners/ecs.py:95`).
If no `image` is given but `install_agents` is set, it renders a Dockerfile with the agent CLIs, builds with `docker build`, and pushes to ECR; otherwise it falls back to plain `ubuntu:24.04` (`agentflow/runners/ecs.py:329`, `agentflow/cloud/installer.py:45`, `agentflow/runners/ecs.py:339`).
The task definition runs `bash -c` with the auth snippet plus the agent command, wires environment variables, and sends logs to `/agentflow/<node-id>` (`agentflow/runners/ecs.py:149`, `agentflow/runners/ecs.py:160`, `agentflow/runners/ecs.py:164`).
Results come from polling `describe_tasks` until `STOPPED`, then reading the container exit code and CloudWatch log lines (`agentflow/runners/ecs.py:234`, `agentflow/runners/ecs.py:255`).
Verbatim ECS target spec from the example:

```
        target={
            "kind": "ecs",
            "region": "ap-northeast-1",
            "cluster": "agentflow",
            "image": "ubuntu:24.04",
            "subnets": [],
            "security_groups": [],
        },
```

## Local vs container runners
Local writes helper files to disk, ensures the working folder exists, and spawns the prepared command with merged environment variables (`agentflow/runners/local.py:270`, `agentflow/runners/local.py:271`, `agentflow/runners/local.py:278`).
Container builds a `docker run --rm` command that mounts the host work, runtime, and app folders, passes env with `-e`, and sets the work folder with `-w` (`agentflow/runners/container.py:18`, `agentflow/runners/container.py:31`, `agentflow/runners/container.py:38`).
Its plan reports kind `container` with image, engine, workdir, and env in the payload (`agentflow/runners/container.py:60`, `agentflow/runners/container.py:67`).
Tests cover local shell wrapping, missing workdir creation, timeout exit 124, cancel exit 130, and container plan shape (`tests/test_runners.py:27`, `tests/test_runners.py:54`, `tests/test_runners.py:610`, `tests/test_runners.py:560`, `tests/test_runners.py:695`).

## What auto-discovery hides and what you still need
EC2 (Elastic Compute Cloud, rentable virtual machines on AWS) discovery finds the newest Ubuntu 24.04 AMI (Amazon Machine Image) from Canonical, creates or reuses an `agentflow` SSH (Secure Shell, remote login protocol) key saved under `~/.agentflow/keys/<region>.pem`, and picks public subnets plus an `agentflow` security group with port 22 open (`agentflow/cloud/aws.py:67`, `agentflow/cloud/aws.py:85`, `agentflow/cloud/aws.py:27`, `agentflow/cloud/aws.py:54`).
ECS (Elastic Container Service, running Docker containers on AWS) reuses the same VPC (Virtual Private Cloud) discovery when subnets or security groups are empty (`agentflow/runners/ecs.py:301`).
Still required: AWS credentials and region access, `boto3` installed, a default VPC (Virtual Private Cloud) in the region, local Docker for ECS (Elastic Container Service) image builds, and local agent logins such as `~/.codex/auth.json` or `~/.claude/.credentials.json` so keys can be forwarded (`agentflow/cloud/aws.py:22`, `agentflow/runners/ecs.py:48`, `agentflow/cloud/aws.py:126`, `agentflow/cloud/aws.py:154`).

**Covers:** agentflow/runners/*.py, agentflow/cloud/*.py, examples/ec2_remote.py, examples/ecs_fargate.py
