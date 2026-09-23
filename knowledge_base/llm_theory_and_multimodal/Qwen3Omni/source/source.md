# QwenLM/Qwen3-Omni
Source: https://github.com/QwenLM/Qwen3-Omni
Kind: repo
Fetched: 2026-09-22T14:34:22.185712+00:00
Tool: git-clone
PDF: https://github.com/QwenLM/Qwen3-Omni

# QwenLM/Qwen3-Omni

Commit: e4235853125589c789f06a2dd83e9f4126df5e9d

## README

# Qwen3-Omni

<br>

<p align="center">
    <img src="https://qianwen-res.oss-cn-beijing.aliyuncs.com//Qwen3-Omni/qwen3_omni_logo.png" width="400"/>
<p>

<p align="center">
        💜 <a href="https://chat.qwen.ai/"><b>Qwen Chat</b></a>&nbsp&nbsp | &nbsp&nbsp🤗 <a href="https://huggingface.co/collections/Qwen/qwen3-omni-68d100a86cd0906843ceccbe">Hugging Face</a>&nbsp&nbsp | &nbsp&nbsp🤖 <a href="https://modelscope.cn/collections/Qwen3-Omni-867aef131e7d4f">ModelScope</a>&nbsp&nbsp | &nbsp&nbsp📑 <a href="https://qwen.ai/blog?id=65f766fc2dcba7905c1cb69cc4cab90e94126bf4&from=research.latest-advancements-list">Blog</a>&nbsp&nbsp | &nbsp&nbsp📚 <a href="https://github.com/QwenLM/Qwen3-Omni/tree/main/cookbooks">Cookbooks</a>&nbsp&nbsp | &nbsp&nbsp📑 <a href="https://arxiv.org/pdf/2509.17765">Paper</a>&nbsp&nbsp
<br>
🖥️ <a href="https://huggingface.co/spaces/Qwen/Qwen3-Omni-Demo">Hugging Face Demo</a>&nbsp&nbsp | &nbsp&nbsp 🖥️ <a href="https://modelscope.cn/studios/Qwen/Qwen3-Omni-Demo">ModelScope Demo</a>&nbsp&nbsp | &nbsp&nbsp💬 <a href="https://github.com/QwenLM/Qwen/blob/main/assets/wechat.png">WeChat (微信)</a>&nbsp&nbsp | &nbsp&nbsp🫨 <a href="https://discord.gg/CV4E9rpNSD">Discord</a>&nbsp&nbsp | &nbsp&nbsp📑 <a href="https://help.aliyun.com/zh/model-studio/user-guide/qwen-omni">API</a>

</p>

We release **Qwen3-Omni**, the natively end-to-end multilingual omni-modal foundation models. It is designed to process diverse inputs including text, images, audio, and video, while delivering real-time streaming responses in both text and natural speech. Click the video below for more information 😃

<details open>
<summary>English Version</summary>
<a href="https://youtu.be/_zdOrPju4_g" target="_blank">
  <img src="https://qianwen-res.oss-cn-beijing.aliyuncs.com/Qwen3-Omni/videocover.png" alt="Open English Video"/>
</a>
</details>

<details>
<summary>Chinese Version</summary>
<a href="https://youtu.be/Wtjsw5deXfQ" target="_blank">
  <img src="https://qianwen-res.oss-cn-beijing.aliyuncs.com/Qwen3-Omni/videocover.png" alt="打开中文视频"/>
</a>
</details>


## News
* 2025.09.26: ⭐️⭐️⭐️ Qwen3-Omni reaches top-1 on Hugging Face Trending! 
* 2025.09.22: 🎉🎉🎉 We have released [Qwen3-Omni](https://huggingface.co/collections/Qwen/qwen3-omni-68d100a86cd0906843ceccbe). For more details, please check our [blog](https://qwen.ai/blog?id=65f766fc2dcba7905c1cb69cc4cab90e94126bf4&from=research.latest-advancements-list)!

## Contents <!-- omit in toc -->

- [Overview](#overview)
  - [Introduction](#introduction)
  - [Model Architecture](#model-architecture)
  - [Cookbooks for Usage Cases](#cookbooks-for-usage-cases)
- [QuickStart](#quickstart)
  - [Model Description and Download](#model-description-and-download)
  - [Transformers Usage](#transformers-usage)
  - [vLLM Usage](#vllm-usage)
  - [DashScope API Usage](#dashscope-api-usage)
  - [Usage Tips (Recommended Reading)](#usage-tips-recommended-reading)
- [Interaction with Qwen3-Omni](#interaction-with-qwen3-omni)
  - [Online Demo](#online-demo)
  - [Real-Time Interaction](#real-time-interaction)
  - [Launch Local Web UI Demo](#launch-local-web-ui-demo)
- [Docker](#-docker)
- [Evaluation](#evaluation)
  - [Performance of Qwen3-Omni](#performance-of-qwen3-omni)
  - [Setting for Evaluation](#setting-for-evaluation)
- [Citation](#citation)

## Overview
### Introduction

<p align="center">
    <img src="https://qianwen-res.oss-cn-beijing.aliyuncs.com/Qwen3-Omni/q3o_introduction.png" width="90%"/>
<p>

Qwen3-Omni is the natively end-to-end multilingual omni-modal foundation models. It processes text, images, audio, and video, and delivers real-time streaming responses in both text and natural speech. We introduce several architectural upgrades to improve performance and efficiency. Key features:

* **State-of-the-art across modalities**: Early text-first pretraining and mixed multimodal training provide native multimodal support. While achieving strong audio and audio-video results, unimodal text and image performance does not regress. Reaches SOTA on 22 of 36 audio/video benchmarks and open-source SOTA on 32 of 36; ASR, audio understanding, and voice conversation performance is comparable to Gemini 2.5 Pro.

* **Multilingual**: Supports 119 text languages, 19 speech input languages, and 10 speech output languages.
  - **Speech Input**: English, Chinese, Korean, Japanese, German, Russian, Italian, French, Spanish, Portuguese, Malay, Dutch, Indonesian, Turkish, Vietnamese, Cantonese, Arabic, Urdu.
  - **Speech Output**: English, Chinese, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean.

* **Novel Architecture**: MoE-based Thinker–Talker design with AuT pretraining for strong general representations, plus a multi-codebook design that drives latency to a minimum.

* **Real-time Audio/Video Interaction**: Low-latency streaming with natural turn-taking and immediate text or speech responses.

* **Flexible Control**: Customize behavior via system prompts for fine-grained control and easy adaptation.

* **Detailed Audio Captioner**: Qwen3-Omni-30B-A3B-Captioner is now open source: a general-purpose, highly detailed, low-hallucination audio captioning model that fills a critical gap in the open-source community.

### Model Architecture

<p align="center">
    <img src="https://qianwen-res.oss-cn-beijing.aliyuncs.com/Qwen3-Omni/overview.png" width="80%"/>
<p>

### Cookbooks for Usage Cases

Qwen3-Omni supports a wide range of multimodal application scenarios, covering various domain tasks involving audio, image, video, and audio-visual modalities. Below are several cookbooks demonstrating the usage cases of Qwen3-Omni and these cookbooks include our actual execution logs. You can first follow the [QuickStart](#quickstart) guide to download the model and install the necessary inference environment dependencies, then run and experiment locally—try modifying prompts or switching model types, and enjoy exploring the capabilities of Qwen3-Omni!

<table>
  <thead>
    <tr>
      <th>Category</th>
      <th>Cookbook</th>
      <th>Description</th>
      <th>Open</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td rowspan="6">Audio</td>
      <td><a href="https://github.com/QwenLM/Qwen3-Omni/blob/main/cookbooks/speech_recognition.ipynb">Speech Recognition</a></td>
      <td>Speech recognition, supporting multiple languages and long audio.</td>
      <td><a href="https://colab.research.google.com/github/QwenLM/Qwen3-Omni/blob/main/cookbooks/speech_recognition.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a></td>
    </tr>
    <tr>
      <td><a href="https://github.com/QwenLM/Qwen3-Omni/blob/main/cookbooks/speech_translation.ipynb">Speech Translation</a></td>
      <td>Speech-to-Text / Speech-to-Speech translation.</td>
      <td><a href="https://colab.research.google.com/github/QwenLM/Qwen3-Omni/blob/main/cookbooks/speech_translation.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a></td>
    </tr>
    <tr>
      <td><a href="https://github.com/QwenLM/Qwen3-Omni/blob/main/cookbooks/music_analysis.ipynb">Music Analysis</a></td>
      <td>Detailed analysis and appreciation of any music, including style, genre, rhythm, etc.</td>
      <td><a href="https://colab.research.google.com/github/QwenLM/Qwen3-Omni/blob/main/cookbooks/music_analysis.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a></td>
    </tr>
    <tr>
      <td><a href="https://github.com/QwenLM/Qwen3-Omni/blob/main/cookbooks/sound_analysis.ipynb">Sound Analysis</a></td>
      <td>Description and analysis of various sound effects and audio signals.</td>
      <td><a href="https://colab.research.google.com/github/QwenLM/Qwen3-Omni/blob/main/cookbooks/sound_analysis.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a></td>
    </tr>
    <tr>
      <td><a href="https://github.com/QwenLM/Qwen3-Omni/blob/main/cookbooks/audio_caption.ipynb">Audio Caption</a></td>
      <td>Audio captioning, detailed description of any audio input.</td>
      <td><a href="https://colab.research.google.com/github/QwenLM/Qwen3-Omni/blob/main/cookbooks/audio_caption.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a></td>
    </tr>
    <tr>
      <td><a href="https://github.com/QwenLM/Qwen3-Omni/blob/main/cookbooks/mixed_audio_analysis.ipynb">Mixed Audio Analysis</a></td>
      <td>Analysis of mixed audio content, such as speech, music, and environmental sounds.</td>
      <td><a href="https://colab.research.google.com/github/QwenLM/Qwen3-Omni/blob/main/cookbooks/mixed_audio_analysis.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a></td>
    </tr>
    <tr>
      <td rowspan="7">Visual</td>
      <td><a href="https://github.com/QwenLM/Qwen3-Omni/blob/main/cookbooks/ocr.ipynb">OCR</a></td>
      <td>OCR for complex images.</td>
      <td><a href="https://colab.research.google.com/github/QwenLM/Qwen3-Omni/blob/main/cookbooks/ocr.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a></td>
    </tr>
    <tr>
      <td><a href="https://github.com/QwenLM/Qwen3-Omni/blob/main/cookbooks/object_grounding.ipynb">Object Grounding</a></td>
      <td>Target detection and grounding.</td>
      <td><a href="https://colab.research.google.com/github/QwenLM/Qwen3-Omni/blob/main/cookbooks/object_grounding.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a></td>
    </tr>
    <tr>
      <td><a href="https://github.com/QwenLM/Qwen3-Omni/blob/main/cookbooks/image_question.ipynb">Image Question</a></td>
      <td>Answering arbitrary questions about any image.</td>
      <td><a href="https://colab.research.google.com/github/QwenLM/Qwen3-Omni/blob/main/cookbooks/image_question.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a></td>
    </tr>
    <tr>
      <td><a href="https://github.com/QwenLM/Qwen3-Omni/blob/main/cookbooks/image_math.ipynb">Image Math</a></td>
      <td>Solving complex mathematical problems in images, highlighting the capabilities of the Thinking model.</td>
      <td><a href="https://colab.research.google.com/github/QwenLM/Qwen3-Omni/blob/main/cookbooks/image_math.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a></td>
    </tr>
    <tr>
      <td><a href="https://github.com/QwenLM/Qwen3-Omni/blob/main/cookbooks/video_description.ipynb">Video Description</a></td>
      <td>Detailed description of video content.</td>
      <td><a href="https://colab.research.google.com/github/QwenLM/Qwen3-Omni/blob/main/cookbooks/video_description.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a></td>
    </tr>
    <tr>
      <td><a href="https://github.com/QwenLM/Qwen3-Omni/blob/main/cookbooks/video_navigation.ipynb">Video Navigation</a></td>
      <td>Generating navigation commands from first-person motion videos.</td>
      <td><a href="https://colab.research.google.com/github/QwenLM/Qwen3-Omni/blob/main/cookbooks/video_navigation.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a></td>
    </tr>
    <tr>
      <td><a href="https://github.com/QwenLM/Qwen3-Omni/blob/main/cookbooks/video_scene_transition.ipynb">Video Scene Transition</a></td>
      <td>Analysis of scene transitions in videos.</td>
      <td><a href="https://colab.research.google.com/github/QwenLM/Qwen3-Omni/blob/main/cookbooks/video_scene_transition.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a></td>
    </tr>
    <tr>
      <td rowspan="3">Audio-Visual</td>
      <td><a href="https://github.com/QwenLM/Qwen3-Omni/blob/main/cookbooks/audio_visual_q

... (truncated, 89137 more characters)

## Top-level layout

- .github/ (dir, 4 files, ~151 lines)
- assets/ (dir, 1 files, ~0 lines)
- cookbooks/ (dir, 18 files, ~6718 lines)
- docker/ (dir, 1 files, ~92 lines)
- LICENSE (~201 lines)
- README.md (~2192 lines)
- web_demo.py (~378 lines)
- web_demo_captioner.py (~185 lines)

