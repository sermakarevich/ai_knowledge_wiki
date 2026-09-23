[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Top-level-files
**In one sentence:** The repo's top level provides two Gradio demo entry points — a multimodal chat demo (`web_demo.py`) and an audio-captioning demo (`web_demo_captioner.py`) — each loadable via transformers or vLLM.
## Key points
- `web_demo.py` loads either `Qwen3OmniMoeForConditionalGeneration` (transformers path) or `vLLM LLM` (vLLM path) plus a `Qwen3OmniMoeProcessor`, selected by `args.use_transformers` (web_demo.py:27-51).
- `web_demo.py` forces `VLLM_USE_V1='0'` and `VLLM_WORKER_MULTIPROC_METHOD='spawn'` before importing vLLM (web_demo.py:5-6).
- `web_demo.py` offers three TTS voices `['Chelsie', 'Ethan', 'Aiden']` with `DEFAULT_VOICE='Chelsie'`, and warns audio generation is unsupported under vLLM (web_demo.py:56-63).
- `web_demo.py` reformats Gradio history into chat messages, converting uploads by mimetype to `image`/`video`/`audio` items with `.webm`-to-`.mp4` conversion, and evicts old turns beyond image 1 / video 5 / audio 5 limits (web_demo.py:92-187).
- `web_demo.py` runs transformers inference via `processor.apply_chat_template` + `process_mm_info(messages, use_audio_in_video=True)` + `model.generate(..., thinker_max_new_tokens=32768, speaker=voice_choice, ...)` with 24 kHz WAV output, or vLLM inference via `SamplingParams(temperature, top_p, top_k, max_tokens=16384)` (web_demo.py:189-224).
- `web_demo_captioner.py` is an audio-only captioning demo whose vLLM path is limited to `limit_mm_per_prompt={'audio': 1}` and `max_model_len=65536` (web_demo_captioner.py:12-42).
- `web_demo_captioner.py` exposes a single-audio Gradio UI (upload/microphone, temperature/top_p/top_k sliders, Submit/Clear) backed by `generate_caption_from_audio` / `on_submit`, with defaults `DEFAULT_CKPT_PATH="Qwen/Qwen3-Omni-30B-A3B-Captioner"` and server port `8901` (web_demo_captioner.py:286-414).
---
## web_demo.py
Multimodal chat demo (379 lines; chunk content truncated — see note below).

Model loading (`_load_model_processor`):
```python
if args.use_transformers:
    from transformers import Qwen3OmniMoeForConditionalGeneration
    if args.flash_attn2:
        model = Qwen3OmniMoeForConditionalGeneration.from_pretrained(args.checkpoint_path,
                                                                    dtype='auto',
                                                                    attn_implementation='flash_attention_2',
                                                                    device_map="auto")
    else:
        model = Qwen3OmniMoeForConditionalGeneration.from_pretrained(args.checkpoint_path, device_map="auto", dtype='auto')
else:
    from vllm import LLM
    model = LLM(
        model=args.checkpoint_path, trust_remote_code=True, gpu_memory_utilization=0.95,
        tensor_parallel_size=torch.cuda.device_count(),
        limit_mm_per_prompt={'image': 1, 'video': 5, 'audio': 10},
        max_num_seqs=1,
        max_model_len=32768,
        seed=1234,
    )
processor = Qwen3OmniMoeProcessor.from_pretrained(args.checkpoint_path)
```
(web_demo.py:27-51)

Demo settings: `VOICE_LIST = ['Chelsie', 'Ethan', 'Aiden']`, `DEFAULT_VOICE = 'Chelsie'` (web_demo.py:56-57); transformers + `generate_audio` installs a voice-assistant `default_system_prompt` (short, ≤50 words, spoken content only, same language as user), otherwise `model.disable_talker()` is called (web_demo.py:66-70).

History handling: `format_history(history, system_prompt)` maps each upload via `client_utils.get_mimetype` to `image`/`video`/`audio` (video `.webm` converted by `to_mp4` via `ffmpeg -y -i <path> -c:v libx264 -preset ultrafast -tune fastdecode -pix_fmt yuv420p -c:a aac -b:a 128k`), orders media items before text, and drops oldest image/video/audio turns beyond `IMAGE_TURN_LIMIT = 1`, `VIDEO_TURN_LIMIT = 5`, `AUDIO_TURN_LIMIT = 5` (web_demo.py:72-187).

Inference `predict(messages, voice_choice=DEFAULT_VOICE, temperature=0.7, top_p=0.8, top_k=20)` (web_demo.py:189): transformers branch calls `model.generate(**inputs, thinker_return_dict_in_generate=True, thinker_max_new_tokens=32768, thinker_do_sample=True, thinker_temperature=temperature, thinker_top_p=top_p, thinker_top_k=top_k, speaker=voice_choice, use_audio_in_video=True)` and renders returned audio at `samplerate=24000` via `soundfile` + `processing_utils.save_bytes_to_cache(wav_bytes, "audio.wav", ...)` (web_demo.py:196-213); vLLM branch uses `SamplingParams(temperature=temperature, top_p=top_p, top_k=top_k, max_tokens=16384)` with `multi_modal_data` image/video/audio dicts (web_demo.py:215-224).

Truncation note: the chunk cuts `web_demo.py` inside `media_predict(audio, video, history, system_prompt, voice_choice, temperature, top_p, top_k)` at the fragment `for f in files: if f: his` (web_demo.py:~226-230); the remaining ~10048 characters (Gradio layout, `demo.queue().launch()` args, CLI `_get_args`, `__main__`) are not present, so they are not covered here.

## web_demo_captioner.py
Audio-only captioning demo (185 lines, fully present).

Model loading mirrors `web_demo.py` except the vLLM branch uses `limit_mm_per_prompt={'audio': 1}`, `max_model_len=65536`, `seed=1234`, `gpu_memory_utilization=0.95` (web_demo_captioner.py:12-42).

Caption path `generate_caption_from_audio(audio_path, temperature, top_p, top_k)` builds a single-turn message `{"role": "user", "content": [{"type": "audio", "audio": audio_path}]}` (web_demo_captioner.py:286-292); transformers branch calls `model.generate(**inputs, thinker_return_dict_in_generate=True, thinker_max_new_tokens=32768, thinker_do_sample=True, thinker_temperature=temperature, thinker_top_p=top_p, thinker_top_k=top_k, use_audio_in_video=True)` (web_demo_captioner.py:302-311); vLLM branch calls `SamplingParams(temperature=temperature, top_p=top_p, top_k=top_k, max_tokens=32768)` with `multi_modal_data: {'audio': audios}` (web_demo_captioner.py:322-343).

Gradio UI: `gr.Blocks(theme=gr.themes.Soft(...))` titled `# Qwen3-Omni-30B-A3B-Captioner Demo`, with `gr.Audio(sources=['upload', 'microphone'], type="filepath")`, sliders `Temperature (0.1–2.0, default 0.6)`, `Top P (0.05–1.0, default 0.95)`, `Top K (1–100, default 20)`, `Submit`/`Clear` buttons, `gr.Textbox(label="Caption Result", lines=15)`, and launch `demo.queue(default_concurrency_limit=1 if use_transformers else 100, max_size=100).launch(max_threads=100, ssr_mode=False, share=..., inbrowser=..., server_port=..., server_name=...)` (web_demo_captioner.py:354-393).

CLI flags (`_get_args`, defaults verbatim):

| Flag | Default | Notes |
| --- | --- | --- |
| `-c, --checkpoint-path` | `Qwen/Qwen3-Omni-30B-A3B-Captioner` | `DEFAULT_CKPT_PATH` (web_demo_captioner.py:396-402) |
| `--flash-attn2` | `False` (store_true) | passes `attn_implementation='flash_attention_2'` (web_demo_captioner.py:403-404) |
| `--use-transformers` | `False` (store_true) | transformers vs vLLM (web_demo_captioner.py:405-406) |
| `--share` | `False` (store_true) | public link (web_demo_captioner.py:407-408) |
| `--inbrowser` | `False` (store_true) | auto-open tab (web_demo_captioner.py:409-410) |
| `--server-port` | `8901` | demo port (web_demo_captioner.py:411) |
| `--server-name` | `127.0.0.1` | demo host (web_demo_captioner.py:412) |

Entry: `args = _get_args(); model, processor = _load_model_processor(args); _launch_demo(args, model, processor)` (web_demo_captioner.py:418-421).

**Covers:** `web_demo.py`, `web_demo_captioner.py`
