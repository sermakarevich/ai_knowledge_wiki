# xcc-zach/xtalk
PDF location (no local PDF): https://github.com/xcc-zach/xtalk
Source: https://github.com/xcc-zach/xtalk
Kind: repo
Fetched: 2026-09-22T14:57:26.444649+00:00
Tool: git-clone

# xcc-zach/xtalk

Commit: 28b842988bcebde172f8f961c7ef152ecfbfce8b

## README

# X-Talk
<img width="460" height="249" alt="xtalk-logo-new" src="https://github.com/user-attachments/assets/4e252ce8-7450-4335-b86a-4b9b26200792" />

[![Live Demo](https://img.shields.io/badge/Live-Demo-brightgreen?style=for-the-badge)](https://xtalk.sjtuxlance.com/)
[![Docs](https://img.shields.io/badge/Documentation-Available-green?style=for-the-badge)](https://xtalk.readthedocs.io/)
[![arXiv](https://img.shields.io/badge/arXiv-Tech_Report-B31B1B?style=for-the-badge&logo=arxiv&logoColor=white)](https://arxiv.org/abs/2512.18706)
![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue?style=for-the-badge&labelColor=555555)](https://opensource.org/licenses/Apache-2.0)


<!-- <img src="PENDING" alt="Watermark" style="width: 40px; height: auto"> -->
> ⚠️ X-Talk is in active prototyping. Interfaces and functions are subject to change. We will try to keep interfaces stable.

X-Talk is an open-source full-duplex cascaded spoken dialogue system framework featuring:
- ⚡ **Low-Latency, Interruptible, Human-Like Speech Interaction**
    - Speech flow is optimized to support **impressive low latency**
    - Enables **natural user interruption** during interaction
    - **Paralinguistic information** (e.g. environment noise, emotion) is encoded in parallel to support in-depth understanding and empathy
- 🧪 **Researcher Friendly**
    - **New models and relevant logic** can be added [within one Python script](#introduce-a-new-model), and seamlessly integrated with the default pipeline.
- 🧩 **Super Lightweight**
    - The framework backend is **pure Python**; nothing to build and install beyond `pip install`.
- 🏭 **Production Ready**
    - **Concurrency** is ensured through asynchronous backend
    - Websocket-based implementation empowers deployment **from web browsers to edge devices**.


## 📚 Contents

- [Demo](#demo)
- [Installation](#installation)
- [Quickstart](#quickstart)
- [Docs](#docs)
- [Contributing](#contributing)
- [Acknowledgements](#acknowledgements)
- [License](#license)

<a id="demo"></a>


### Online Demo
[Demo Link](https://xtalk.sjtuxlance.com/)

This demo runs on 4090 cluster with 8-bit quantized *SenseVoice* as speech recognizer, *IndexTTS 1.5* as speech generator, and 4-bit quantized *Qwen3-30B-A3B* as language model. Though at the cost of intelligence due to a relatively small language model, it demonstrates low latency.



### Demo Videos
<table class="center">
<tr>
    <td width=50% style="border: none">
        <video controls autoplay loop src="https://github.com/user-attachments/assets/8db97785-a990-4747-b9c2-c45905ac0ef5" muted="false"></video>
    </td>
    <td width=50% style="border: none">
        <video controls autoplay loop src="https://github.com/user-attachments/assets/5d27fb42-5bf6-448d-abd9-d132d1cace01" muted="false"></video>
    </td>
</tr>
<tr>
    <td width=50% style="border: none">
        <video controls autoplay loop src="https://github.com/user-attachments/assets/793ee442-32bd-46ea-8319-39b86288c5fe" muted="false"></video>
    </td>
    <td width=50% style="border: none">
        <video controls autoplay loop src="https://github.com/user-attachments/assets/6cdd60c2-d192-4883-9865-196e5bc0bb1d" muted="false"></video>
    </td>
</tr>
<tr>
    <td width=50% style="border: none">
        <video controls autoplay loop src="https://github.com/user-attachments/assets/570cac89-cfd0-4073-9575-783f74420b42" muted="false"></video>
    </td>
    <td width=50% style="border: none">
        <video controls autoplay loop src="https://github.com/user-attachments/assets/b366c4ea-b1a6-41fd-8bba-3db184c4297b" muted="false"></video>
    </td>
</tr>
<tr>
    <td width=50% style="border: none">
        <video controls autoplay loop src="https://github.com/user-attachments/assets/917ac610-efd6-4787-8f5b-5b18d7c248f3" muted="false"></video>
    </td>
    <td width=50% style="border: none">
        <video controls autoplay loop src="https://github.com/user-attachments/assets/9dd89902-e6d1-4f6c-ba17-6441b0b48a74" muted="false"></video>
    </td>
</tr>
<tr>
    <td width=50% style="border: none">
        <video controls autoplay loop src="https://github.com/user-attachments/assets/edd9be47-ecbb-41e8-abc4-dccb67166ac3" muted="false"></video>
    </td>
    <td width=50% style="border: none">
        <video controls autoplay loop src="https://github.com/user-attachments/assets/50261970-e03c-47a9-8f2d-a3fa186b2ac3" muted="false"></video>
    </td>
</tr>
</table>

The tour guiding demos are conducted with *Qwen3-Next-80B-A3B-Instruct* as language model, and the other eight demos are aligned with the online demo setting. Larger language models are more intelligent at the cost of latency.

<a id="installation"></a>


## 🛠️ Installation

```bash
pip install git+https://github.com/xcc-zach/xtalk.git@main
```

<a id="quickstart"></a>


## 🚀 Quickstart

We will use APIs from AliCloud to demonstrate the basic capability of **X-Talk**.

First, install dependencies for AliCloud and server script:
```bash
pip install "xtalk[ali,example] @ git+https://github.com/xcc-zach/xtalk.git@main"
```

Then, obtain an API key from [AliCloud Bailian Platform](https://bailian.console.aliyun.com/?tab=model#/api-key). We will be using free-tier service (currently) from AliCloud.

> Online service may be unstable and of high latency. We recommend using locally deployed models for better user experience. See [server config tutorial](https://xtalk.readthedocs.io/tutorial/config_the_service/) and [local deployment recipe](https://xtalk.readthedocs.io/tutorial/sample_config_for_fully_local_deployment/) for details.

After that, create a JSON config specifying the models to use, and **fill in <API_KEY>** with the key you obtained:

```json
{
    "asr": {
        "type": "Qwen3ASRFlashRealtime",
        "params": {
            "api_key": "<API_KEY>"
        }
    },
    "llm_agent": {
        "type": "DefaultAgent",
        "params": {
            "model": {
                "api_key": "<API_KEY>",
                "model": "qwen-plus-2025-12-01",
                "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1"
            }
        }
    },
    "tts": {
        "type": "CosyVoice",
        "params": {
            "api_key": "<API_KEY>"
        }
    }
}
```

The next step is to compose the startup script. Since we also need to link frontend webpage and scripts to get the demo working, the startup script is ready at `examples/sample_app/configurable_server.py`. We simply need to start the server with the config file (**fill in <PATH_TO_CONFIG>.json** with the path to the config file we just created) and a custom port:
```bash
git clone https://github.com/xcc-zach/xtalk.git
cd xtalk
python examples/sample_app/configurable_server.py  --port 7635 --config <PATH_TO_CONFIG>.json
```

Finally, our demo is ready at `http://localhost:7635`. View it in the browser!

<a id="docs"></a>


## 📕 Docs

Docs [here](https://xtalk.readthedocs.io/)

## pyproject.toml

```
[build-system]
requires = ["setuptools>=68", "wheel", "setuptools_scm[toml]>=8"]
build-backend = "setuptools.build_meta"

[project]
name            = "xtalk"
description     = "AI conversational agent framework"
readme          = "README.md"
authors         = [{ name = "xcc", email = "2867389537@qq.com" }]
license         = { text = "MIT" }
requires-python = ">=3.10"
dependencies    = [
  "langchain >=0.3.0, <0.4.0",
  "langchain-core >=0.3.0, <0.4.0",
  "langchain-openai",
  "langchain-chroma",
  "PyYAML",
  "fastapi",
  "numpy",
  "aiohttp",
  "requests"
]
dynamic         = ["version"]

[project.optional-dependencies]
dev  = ["pytest", "pytest-cov"]
testing = [
  "requests",
  "soundfile",
  "websockets",
  "uvicorn[standard]",
  "soxr",
  "torch",
]
ali = [
  "dashscope >=1.25.3",
  "certifi"
]
elevenlabs = [
  "websockets"
]
chattts = [
  "ChatTTS",
  "torch",
  "torchaudio"
]
f5tts = [
  "f5-tts",
  "torch",
  "torchaudio"
]
kokoro = [
  "kokoro >=0.9.4",
  "soundfile",
  "misaki[zh]",
  "misaki[ja]"
]
bark = [
  "transformers >=4.45.0",
  "scipy",
  "torch"
]
cosyvoice-local = [
  "grpcio",
  "grpcio-tools", 
  "numpy",
  "soundfile",
  "librosa",
  "soxr"
]
index-tts = [
  "requests",
  "aiohttp",
  "soundfile",
  "soxr",
  "numpy"
]
gpt-sovits = [
  "soundfile",
  "soxr",
]
paraformer-local = [
  "torch",
  "torchaudio",
  "funasr",
  "huggingface_hub",
  "modelscope"
]
sense-voice-small = [
  "torch",
  "torchaudio",
  "funasr",
  "huggingface_hub",
  "modelscope"
]
sherpa-onnx-asr = [
  "numpy",
  "websockets",
]
agentic-asr = [
  "numpy",
  "websockets",
]
ct-punt = [
  "torch",
  "torchaudio",
  "funasr",
  "huggingface_hub",
  "modelscope"
]
zipformer-local = [
  "numpy>=1.21",
  "sherpa-onnx",
  "soundfile"
]
llm-local = [
  "transformers >=4.45.0",
  "torch",
  "accelerate"
]
whisper = [
  "openai-whisper"
]
ten-turn-detection = [
  "transformers >=4.45.0",
  "torch",
]
edge-tts = [
  "edge-tts"
]
silero-vad = [
  "numpy",
  "onnxruntime",
  "websockets",
]
fast-enhancer = [
  "numpy",
  "requests",
  "onnxruntime",
  "websockets",
]
pywebrtc-audio = [
  "websockets",
]
rubberband = [
  "pyrubberband"
]
pyannote = ["pyannote.audio","torchvision"]
soulx-duplug = [
  "websockets",
]
turn-sense = [
  "aiohttp",
  "numpy",
]
example = [
  "pypdf",
  "fastapi==0.128.0",
  "jinja2",
  "python-multipart",
  "uvicorn[standard]",
]
[tool.setuptools]
package-dir = {"" = "src"}

[tool.setuptools_scm]
version_scheme = "post-release"
local_scheme   = "no-local-version"

[tool.pytest.ini_options]
addopts   = ["--import-mode=importlib", "-q"]
testpaths = ["tests"]

[tool.ruff]
exclude = ["*_pb2.py", "*_pb2_grpc.py"]

```

## Top-level layout

- .gitattributes (~1 lines)
- .github/ (dir, 5 files, ~89 lines)
- .gitignore (~187 lines)
- .pre-commit-config.yaml (~15 lines)
- .readthedocs.yaml (~13 lines)
- AGENTS.md (~24 lines)
- app/ (dir, 254 files, ~59786 lines)
- configs/ (dir, 2 files, ~56 lines)
- CONTRIBUTING.md (~84 lines)
- docs/ (dir, 118 files, ~26620 lines)
- examples/ (dir, 12 files, ~5518 lines)
- frontend/ (dir, 47 files, ~6409 lines)
- LICENSE (~17 lines)
- mkdocs.yml (~141 lines)
- pyproject.toml (~175 lines)
- README.md (~170 lines)
- scripts/ (dir, 2 files, ~2482 lines)
- src/ (dir, 124 files, ~30537 lines)
- tests/ (dir, 19 files, ~5121 lines)

