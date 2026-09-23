> PDF location (no local copy): https://github.com/PaddlePaddle/PaddleSpeech

# PaddlePaddle/PaddleSpeech
Source: https://github.com/PaddlePaddle/PaddleSpeech
Kind: repo
Fetched: 2026-09-22T14:31:25.710576+00:00
Tool: git-clone

# PaddlePaddle/PaddleSpeech

Commit: 6b25a400008d393f9c3af837b3c692b17f29ee1a

## README

([简体中文](./README_cn.md)|English)
<p align="center">
  <img src="./docs/images/PaddleSpeech_logo.png" />
</p>

<p align="center">
    <a href="./LICENSE"><img src="https://img.shields.io/badge/license-Apache%202-red.svg"></a>
    <a href="https://github.com/PaddlePaddle/PaddleSpeech/releases"><img src="https://img.shields.io/github/v/release/PaddlePaddle/PaddleSpeech?color=ffa"></a>
    <a href="support os"><img src="https://img.shields.io/badge/os-linux%2C%20win%2C%20mac-pink.svg"></a>
    <a href=""><img src="https://img.shields.io/badge/python-3.8+-aff.svg"></a>
    <a href="https://github.com/PaddlePaddle/PaddleSpeech/graphs/contributors"><img src="https://img.shields.io/github/contributors/PaddlePaddle/PaddleSpeech?color=9ea"></a>
    <a href="https://github.com/PaddlePaddle/PaddleSpeech/commits"><img src="https://img.shields.io/github/commit-activity/m/PaddlePaddle/PaddleSpeech?color=3af"></a>
    <a href="https://github.com/PaddlePaddle/PaddleSpeech/issues"><img src="https://img.shields.io/github/issues/PaddlePaddle/PaddleSpeech?color=9cc"></a>
    <a href="https://github.com/PaddlePaddle/PaddleSpeech/stargazers"><img src="https://img.shields.io/github/stars/PaddlePaddle/PaddleSpeech?color=ccf"></a>
    <a href="=https://pypi.org/project/paddlespeech/"><img src="https://img.shields.io/pypi/dm/PaddleSpeech"></a>
    <a href="=https://pypi.org/project/paddlespeech/"><img src="https://static.pepy.tech/badge/paddlespeech"></a>
    <a href="https://huggingface.co/spaces"><img src="https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Spaces-blue"></a>
</p>
<div align="center">  
<h4>
    <a href="#quick-start"> Quick Start </a>
  | <a href="#documents"> Documents </a>
  | <a href="#model-list"> Models List </a>
  | <a href="https://aistudio.baidu.com/aistudio/course/introduce/25130"> AIStudio Courses </a>
  | <a href="https://arxiv.org/abs/2205.12007"> NAACL2022 Best Demo Award Paper </a>
  | <a href="https://gitee.com/paddlepaddle/PaddleSpeech"> Gitee </a>
</h4>
</div>

------------------------------------------------------------------------------------

**PaddleSpeech** is an open-source toolkit on [PaddlePaddle](https://github.com/PaddlePaddle/Paddle) platform for a variety of critical tasks in speech and audio, with the state-of-art and influential models. 

**PaddleSpeech** won the [NAACL2022 Best Demo Award](https://2022.naacl.org/blog/best-demo-award/), please check out our paper on [Arxiv](https://arxiv.org/abs/2205.12007).

##### Speech Recognition

<div align = "center">
<table style="width:100%">
  <thead>
    <tr>
      <th> Input Audio  </th>
      <th width="550"> Recognition Result  </th>
    </tr>
  </thead>
  <tbody>
   <tr>
      <td align = "center">
      <a href="https://paddlespeech.cdn.bcebos.com/PaddleAudio/en.wav" rel="nofollow">
            <img align="center" src="./docs/images/audio_icon.png" width="200 style="max-width: 100%;"></a><br>
      </td>
      <td >I knocked at the door on the ancient side of the building.</td>
    </tr>
    <tr>
      <td align = "center">
      <a href="https://paddlespeech.cdn.bcebos.com/PaddleAudio/zh.wav" rel="nofollow">
            <img align="center" src="./docs/images/audio_icon.png" width="200" style="max-width: 100%;"></a><br>
      </td>
      <td>我认为跑步最重要的就是给我带来了身体健康。</td>
    </tr>
  </tbody>
</table>

</div>

##### Speech Translation (English to Chinese)

<div align = "center">
<table style="width:100%">
  <thead>
    <tr>
      <th> Input Audio  </th>
      <th width="550"> Translations Result  </th>
    </tr>
  </thead>
  <tbody>
   <tr>
      <td align = "center">
      <a href="https://paddlespeech.cdn.bcebos.com/PaddleAudio/en.wav" rel="nofollow">
            <img align="center" src="./docs/images/audio_icon.png" width="200 style="max-width: 100%;"></a><br>
      </td>
      <td >我 在 这栋 建筑 的 古老 门上 敲门。</td>
    </tr>
  </tbody>
</table>

</div>

##### Text-to-Speech
<div align = "center">
<table style="width:100%">
  <thead>
    <tr>
      <th width="550" > Input Text</th>
      <th>Synthetic Audio</th>
    </tr>
  </thead>
  <tbody>
   <tr>
      <td>Life was like a box of chocolates, you never know what you're gonna get.</td>
      <td align = "center">
      <a href="https://paddlespeech.cdn.bcebos.com/Parakeet/docs/demos/tacotron2_ljspeech_waveflow_samples_0.2/sentence_1.wav" rel="nofollow">
            <img align="center" src="./docs/images/audio_icon.png" width="200" style="max-width: 100%;"></a><br>
      </td>
    </tr>
    <tr>
      <td>早上好，今天是2020/10/29，最低温度是-3°C。</td>
      <td align = "center">
      <a href="https://paddlespeech.cdn.bcebos.com/Parakeet/docs/demos/parakeet_espnet_fs2_pwg_demo/tn_g2p/parakeet/001.wav" rel="nofollow">
            <img align="center" src="./docs/images/audio_icon.png" width="200" style="max-width: 100%;"></a><br>
      </td>
    </tr>
    <tr>
      <td>季姬寂，集鸡，鸡即棘鸡。棘鸡饥叽，季姬及箕稷济鸡。鸡既济，跻姬笈，季姬忌，急咭鸡，鸡急，继圾几，季姬急，即籍箕击鸡，箕疾击几伎，伎即齑，鸡叽集几基，季姬急极屐击鸡，鸡既殛，季姬激，即记《季姬击鸡记》。</td>
      <td align = "center">
      <a href="https://paddlespeech.cdn.bcebos.com/Parakeet/docs/demos/jijiji.wav" rel="nofollow">
            <img align="center" src="./docs/images/audio_icon.png" width="200" style="max-width: 100%;"></a><br>
      </td>
    </tr>
    <tr>
      <td>大家好，我是 parrot 虚拟老师，我们来读一首诗，我与春风皆过客，I and the spring breeze are passing by，你携秋水揽星河，you take the autumn water to take the galaxy。</td>
      <td align = "center">
      <a href="https://paddlespeech.cdn.bcebos.com/Parakeet/docs/demos/labixiaoxin.wav" rel="nofollow">
            <img align="center" src="./docs/images/audio_icon.png" width="200" style="max-width: 100%;"></a><br>
      </td>
    </tr>
    <tr>
      <td>宜家唔系事必要你讲，但系你所讲嘅说话将会变成呈堂证供。</td>
      <td align = "center">
      <a href="https://paddlespeech.cdn.bcebos.com/Parakeet/docs/demos/chengtangzhenggong.wav" rel="nofollow">
            <img align="center" src="./docs/images/audio_icon.png" width="200" style="max-width: 100%;"></a><br>
      </td>
    </tr>
    <tr>
      <td>各个国家有各个国家嘅国歌</td>
      <td align = "center">
      <a href="https://paddlespeech.cdn.bcebos.com/Parakeet/docs/demos/gegege.wav" rel="nofollow">
            <img align="center" src="./docs/images/audio_icon.png" width="200" style="max-width: 100%;"></a><br>
      </td>
    </tr>
  </tbody>
</table>

</div>

For more synthesized audios, please refer to [PaddleSpeech Text-to-Speech samples](https://paddlespeech.readthedocs.io/en/latest/tts/demo.html).

##### Punctuation Restoration
<div align = "center">
<table style="width:100%">
  <thead>
    <tr>
      <th width="390"> Input Text </th>
      <th width="390"> Output Text </th>
    </tr>
  </thead>
  <tbody>
   <tr>
      <td>今天的天气真不错啊你下午有空吗我想约你一起去吃饭</td>
      <td>今天的天气真不错啊！你下午有空吗？我想约你一起去吃饭。</td>
    </tr>
  </tbody>
</table>

</div>


### Features

Via the easy-to-use, efficient, flexible and scalable implementation, our vision is to empower both industrial application and academic research, including training, inference & testing modules, and deployment process. To be more specific, this toolkit features at:
- 📦  **Ease of Use**: low barriers to install, [CLI](#quick-start), [Server](#quick-start-server), and [Streaming Server](#quick-start-streaming-server) is available to quick-start your journey.
- 🏆  **Align to the State-of-the-Art**: we provide high-speed and ultra-lightweight models, and also cutting-edge technology. 
- 🏆  **Streaming ASR and TTS System**: we provide production ready streaming asr and streaming tts system.
- 💯  **Rule-based Chinese frontend**: our frontend contains Text Normalization and Grapheme-to-Phoneme (G2P, including Polyphone and Tone Sandhi). Moreover, we use self-defined linguistic rules to adapt Chinese context.
- 📦  **Varieties of Functions that Vitalize both Industrial and Academia**:
  - 🛎️  *Implementation of critical audio tasks*: this toolkit contains audio functions like  Automatic Speech Recognition, Text-to-Speech Synthesis, Speaker Verification, KeyWord Spotting, Audio Classification, and Speech Translation, etc.
  - 🔬  *Integration of mainstream models and datasets*: the toolkit implements modules that participate in the whole pipeline of the speech tasks, and uses mainstream datasets like LibriSpeech, LJSpeech, AIShell, CSMSC, etc. See also [model list](#model-list) for more details.
  - 🧩  *Cascaded models application*: as an extension of the typical traditional audio tasks, we combine the workflows of the aforementioned tasks with other fields like Natural language processing (NLP) and Computer Vision (CV).

### Recent Update
- 🎉 2025.09.01: Add [Whisper large v3 and turbo model](https://github.com/PaddlePaddle/PaddleSpeech/tree/develop/demos/whisper).
- 🤗 2025.08.11: Add [code-switch online model and server demo](./examples/tal_cs/asr1/).
- 👑 2023.05.31: Add [WavLM ASR-en](https://github.com/PaddlePaddle/PaddleSpeech/blob/develop/examples/librispeech/asr5), WavLM fine-tuning for ASR on LibriSpeech.
- 🎉 2023.05.18: Add [Squeezeformer](https://github.com/PaddlePaddle/PaddleSpeech/tree/develop/examples/aishell/asr1), Squeezeformer training for ASR on Aishell.
- 👑 2023.05.04: Add [HuBERT ASR-en](https://github.com/PaddlePaddle/PaddleSpeech/blob/develop/examples/librispeech/asr4), HuBERT fine-tuning for ASR on LibriSpeech.
- ⚡ 2023.04.28: Fix [0-d tensor](https://github.com/PaddlePaddle/PaddleSpeech/pull/3214), with the upgrade of paddlepaddle==2.5, the problem of modifying 0-d tensor has been solved.
- 👑 2023.04.25: Add [AMP for U2 conformer](https://github.com/PaddlePaddle/PaddleSpeech/pull/3167).
- 🔥 2023.04.06: Add [subtitle file (.srt format) generation example](./demos/streaming_asr_server).
- 🔥 2023.03.14: Add SVS(Singing Voice Synthesis) examples with Opencpop dataset, including [DiffSinger](./examples/opencpop/svs1)、[PWGAN](./examples/opencpop/voc1) and [HiFiGAN](./examples/opencpop/voc5), the effect is continuously optimized.
- 👑 2023.03.09: Add [Wav2vec2ASR-zh](./examples/aishell/asr3).
- 🎉 2023.03.07: Add [TTS ARM Linux C++ Demo (with C++ Chinese Text Frontend)](./demos/TTSArmLinux).
- 🔥 2023.03.03 Add Voice Conversion [StarGANv2-VC synthesize pipeline](./examples/vctk/vc3).
- 🎉 2023.02.16: Add [Cantonese TTS](./examples/canton/tts3).
- 🔥 2023.01.10: Add [code-switch asr CLI and Demos](./demos/speech_recognition).
- 👑 2023.01.06: Add [code-switch asr tal_cs recipe](./examples/tal_cs/asr1/).
- 🎉 2022.12.02: Add [end-to-end Prosody Prediction pipeline](./examples/csmsc/tts3_rhy) (including using prosody labels in Acoustic Model).
- 🎉 2022.11.30: Add [TTS Android Demo](./demos/TTSAndroid).
- 🤗 2022.11.28: PP-TTS and PP-ASR demos are available in [AIStudio](https://aistudio.baidu.com/aistudio/modelsoverview) and [official website
 of paddlepaddle](https://www.paddlepaddle.org.cn/models).
- 👑 2022.11.18: Add [Whisper CLI and Demos](https://github.com/PaddlePaddle/PaddleSpeech/pull/2640), support multi language recognition and translation.
- 🔥 2022.11.18: Add [Wav2vec2 CLI and Demos](./demos/speech_ssl), Support ASR and Feature Extraction.
- 🎉 2022.11.17: Add [male voice for TTS](https://github.com/PaddlePaddle/PaddleSpeech/pull/2660).
- 🔥 2022.11.07: Add [U2/U2++ C++ High Performance Streaming ASR Deployment](https://github.com/PaddlePaddle/PaddleSpeech/blob/develop/runtime/examples/u2pp_ol/wenetspeech).
- 👑 2022.11.01: Add [Adversarial Loss](https://arxiv.org/pdf/1907.04448.pdf) for [Chinese English mixed TTS](./examples/zh_en_tts/tts3).
- 🔥 2022.10.26: Add [Prosody Prediction](./examples/other/rhy) for TTS.
- 🎉 2022.10.21: Add [SSML](https://github.com/PaddlePaddle/PaddleSpeech/discussions/2538) for TTS Chinese Text Frontend.
- 👑 2022.10.11: Add [Wav2vec2ASR-en](./examples/librispeech/asr3), wav2vec2.0 fine-tuning for ASR on LibriSpeech.
- 🔥 2022.09.26: Add Voice Cloning, TTS finetune, and [ERNIE-SAT](https://arxiv.org/abs/2211.03545) in [PaddleSpeech Web Demo](./demos/speech_web).
- ⚡ 2022.09.09: Add AISHELL-3 Voice Cloning [example](./examples/aishell3/vc2) with ECAPA-TDNN speaker enc

... (truncated, 36275 more characters)

## setup.py

```
# Copyright (c) 2020 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import contextlib
import inspect
import io
import os
import subprocess as sp
import sys
from pathlib import Path

from setuptools import Command
from setuptools import find_packages
from setuptools import setup
from setuptools.command.develop import develop
from setuptools.command.install import install
from setuptools.command.test import test

HERE = Path(os.path.abspath(os.path.dirname(__file__)))

VERSION = '0.0.0'
COMMITID = 'none'


def determine_python_version():
    """
    Determine the current python version. The function return a string such as '3.7'.
    """
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}"
    return python_version


def determine_opencc_version():
    # get gcc version
    gcc_version = None
    try:
        output = sp.check_output(
            ['gcc', '--version'], stderr=sp.STDOUT, text=True)
        for line in output.splitlines():
            if "gcc" in line:
                gcc_version = line.split()[-1]
    except Exception as e:
        gcc_version = None

    # determine opencc version
    if gcc_version:
        if int(gcc_version.split(".")[0]) < 9:
            return "opencc==1.1.6"  # GCC<9 need opencc==1.1.6
    return "opencc"  # default


def determine_scipy_version():
    # get python version
    python_version = determine_python_version()

    # determine scipy version
    if python_version == "3.8":
        return "scipy>=1.4.0, <=1.12.0"  # Python3.8 need scipy>=1.4.0, <=1.12.0
    return "scipy"  # default


def determine_matplotlib_version():
    # get python version
    python_version = determine_python_version()

    # determine matplotlib version
    if python_version == "3.8" or python_version == "3.9":
        return "matplotlib<=3.8.4"  # Python3.8/9 need matplotlib<=3.8.4
    return "matplotlib"  # default


base = [
    "braceexpand",
    "editdistance",
    "g2p_en",
    "g2pM",
    "h5py",
    "hyperpyyaml",
    "inflect",
    "jsonlines",
    "numpy",
    "librosa>=0.9",
    determine_scipy_version(),  # scipy or scipy>=1.4.0, <=1.12.0
    "loguru",
    determine_matplotlib_version(),  # matplotlib or matplotlib<=3.8.4
    "nara_wpe",
    "onnxruntime>=1.11.0",
    determine_opencc_version(),  # opencc or opencc==1.1.6
    "opencc-python-reimplemented",
    "pandas",
    "paddlenlp>=2.4.8",
    "paddleslim>=2.3.4",
    "ppdiffusers>=0.9.0",
    "paddlespeech_feat",
    "praatio>=6.0.0",
    "prettytable",
    "pydantic",
    "pypinyin",
    "pypinyin-dict",
    "python-dateutil",
    "pyworld>=0.2.12",
    "pyyaml",
    "resampy",
    "sacrebleu",
    "soundfile",
    "textgrid",
    "timer",
    "ToJyutping",
    "typeguard",
    "webrtcvad",
    "yacs>=0.1.8",
    "zhon",
    "scikit-learn",
    "pathos",
    "kaldiio",
    "ffmpeg-python",
    "ffmpy",
    "flatten_dict",
    "pyloudnorm",
    "rich",
    "tiktoken",
]

server = ["pattern_singleton", "websockets"]

requirements = {
    "install":
    base + server,
    "develop": [
        "ConfigArgParse",
        "coverage",
        "gpustat",
        "paddlespeech_ctcdecoders",
        "phkit",
        "pypi-kenlm",
        "snakeviz",
        "sox",
        "soxbindings",
        "unidecode",
        "yq",
        "pre-commit",
    ]
}


def check_call(cmd: str, shell=False, executable=None):
    try:
        sp.check_call(
            cmd.split(),
            shell=shell,
            executable="/bin/bash" if shell else executable)
    except sp.CalledProcessError as e:
        print(
            f"{__file__}:{inspect.currentframe().f_lineno}: CMD: {cmd}, Error:",
            e.output,
            file=sys.stderr)
        raise e


def check_output(cmd: str, shell=False):
    try:
        out_bytes = sp.check_output(cmd.split())
    except sp.CalledProcessError as e:
        out_bytes = e.output  # Output generated before error
        code = e.returncode  # Return code
        print(
            f"{__file__}:{inspect.currentframe().f_lineno}: CMD: {cmd}, Error:",
            out_bytes,
            file=sys.stderr)
    return out_bytes.strip().decode('utf8')


@contextlib.contextmanager
def pushd(new_dir):
    old_dir = os.getcwd()
    os.chdir(new_dir)
    print(new_dir)
    yield
    os.chdir(old_dir)
    print(old_dir)


def read(*names, **kwargs):
    with io.open(
            os.path.join(os.path.dirname(__file__), *names),
            encoding=kwargs.get("encoding", "utf8")) as fp:
        return fp.read()


def _remove(files: str):
    for f in files:
        f.unlink()


################################# Install ##################################


def _post_install(install_lib_dir):
    # tools/make
    tool_dir = HERE / "tools"
    _remove(tool_dir.glob("*.done"))
    with pushd(tool_dir):
        check_call("make")
    print("tools install.")

    # ctcdecoder
    ctcdecoder_dir = HERE / 'third_party/ctc_decoders'
    with pushd(ctcdecoder_dir):
        check_call("bash -e setup.sh")
    print("ctcdecoder install.")


class DevelopCommand(develop):
    def run(self):
        develop.run(self)
        # must after develop.run, or pkg install by shell will not see
        self.execute(_post_install, (self.install_lib, ), msg="Post Install...")


class InstallCommand(install):
    def run(self):
        install.run(self)


class TestCommand(test):
    def finalize_options(self):
        test.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # Run nose ensuring that argv simulates running nosetests directly
        import nose
        nose.run_exit(argv=['nosetests', '-w', 'tests'])


# cmd: python setup.py upload
class UploadCommand(Command):
    description = "Build and publish the package."
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            print("Removing previous dist/ ...")
            shutil.rmtree(str(HERE / "dist"))
        except OSError:
            pass
        print("Building source distribution...")
        sp.check_call([sys.executable, "setup.py", "sdist"])
        print("Uploading package to PyPi...")
        sp.check_call(["twine", "upload", "dist/*"])
        sys.exit()


################################# Version ##################################
def write_version_py(filename='paddlespeech/__init__.py'):
    import paddlespeech
    if hasattr(paddlespeech,
               "__version__") and paddlespeech.__version__ == VERSION:
        return
    with open(filename, "a") as f:
        out_str = f"\n__version__ = '{VERSION}'\n"
        print(out_str)
        f.write(f"\n__version__ = '{VERSION}'\n")

    COMMITID = check_output("git rev-parse HEAD")
    with open(filename, 'a') as f:
        out_str = f"\n__commit__ = '{COMMITID}'\n"
        print(out_str)
        f.write(f"\n__commit__ = '{COMMITID}'\n")

    print(f"{inspect.currentframe().f_code.co_name} done")


def remove_version_py(filename='paddlespeech/__init__.py'):
    with open(filename, "r") as f:
        lines = f.readlines()
    with open(filename, "w") as f:
        for line in lines:
            if "__version__" in line or "__commit__" in line:
                continue
            f.write(line)
    print(f"{inspect.currentframe().f_code.co_name} done")


@contextlib.contextmanager
def version_info():
    write_version_py()
    yield
    remove_

... (truncated, 2577 more characters)
```

## setup.cfg

```
[build_ext]
debug=0

[metadata]
license_file = LICENSE
description-file = README.md

[magformat]
formatters=yapf

[easy_install]
index-url=https://pypi.tuna.tsinghua.edu.cn/simple

```

## Top-level layout

- .clang-format (~29 lines)
- .flake8 (~56 lines)
- .gitconfig (~48 lines)
- .github/ (dir, 9 files, ~273 lines)
- .gitignore (~56 lines)
- .mergify.yml (~137 lines)
- .pre-commit-config.yaml (~68 lines)
- .pre-commit-hooks/ (dir, 2 files, ~146 lines)
- .readthedocs.yml (~26 lines)
- .style.yapf (~3 lines)
- .travis.yml (~35 lines)
- audio/ (dir, 133 files, ~27354 lines)
- dataset/ (dir, 37 files, ~2435 lines)
- demos/ (dir, 285 files, ~28761 lines)
- docker/ (dir, 3 files, ~111 lines)
- docs/ (dir, 755 files, ~17805 lines)
- examples/ (dir, 861 files, ~61678 lines)
- LICENSE (~201 lines)
- MANIFEST.in (~2 lines)
- paddlespeech/ (dir, 834 files, ~155907 lines)
- README.md (~1042 lines)
- README_cn.md (~1048 lines)
- runtime/ (dir, 508 files, ~198450 lines)
- setup.cfg (~12 lines)
- setup.py (~389 lines)
- tests/ (dir, 91 files, ~9800 lines)
- third_party/ (dir, 40 files, ~3703 lines)
- tools/ (dir, 27 files, ~1347 lines)
- utils/ (dir, 75 files, ~11266 lines)

