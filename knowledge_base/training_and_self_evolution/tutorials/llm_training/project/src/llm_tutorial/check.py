"""Connectivity/speed check. `--cpu` runs on the Mac (just prints versions, no GPU
expected); the default mode runs on rtx and additionally benchmarks the GPU.
"""

import sys
import time

import typer

app = typer.Typer(add_completion=False, invoke_without_command=True)


def _versions() -> dict[str, str]:
    import peft
    import torch
    import transformers
    import trl

    return {
        "python": sys.version.split()[0],
        "torch": torch.__version__,
        "transformers": transformers.__version__,
        "trl": trl.__version__,
        "peft": peft.__version__,
    }


def _bf16_matmul_tflops(n: int = 4096, iters: int = 20) -> float:
    import torch

    a = torch.randn(n, n, dtype=torch.bfloat16, device="cuda")
    b = torch.randn(n, n, dtype=torch.bfloat16, device="cuda")
    torch.cuda.synchronize()
    start = time.perf_counter()
    for _ in range(iters):
        a @ b
    torch.cuda.synchronize()
    elapsed = time.perf_counter() - start
    flops_per_matmul = 2 * n**3
    return (flops_per_matmul * iters) / elapsed / 1e12


@app.callback()
def main(cpu: bool = typer.Option(False, "--cpu", help="CPU-only check (Mac): versions only.")) -> None:
    import torch

    versions = _versions()
    for name, version in versions.items():
        print(f"{name}: {version}")
    print(f"torch.cuda.is_available(): {torch.cuda.is_available()}")

    if cpu:
        if torch.cuda.is_available():
            print("warning: CUDA is available but --cpu was requested")
        return

    if not torch.cuda.is_available():
        print("error: CUDA is not available, this must run on rtx")
        raise typer.Exit(1)

    name = torch.cuda.get_device_name(0)
    free_bytes, total_bytes = torch.cuda.mem_get_info(0)
    print(f"GPU: {name}")
    print(f"memory: {free_bytes / 1024**3:.1f} GB free / {total_bytes / 1024**3:.1f} GB total")

    tflops = _bf16_matmul_tflops()
    print(f"bf16 4096x4096 matmul: {tflops:.1f} TFLOP/s")

    try:
        import fla  # noqa: F401

        print("fla importable: True")
    except ImportError:
        print("fla importable: False")


if __name__ == "__main__":
    app()
