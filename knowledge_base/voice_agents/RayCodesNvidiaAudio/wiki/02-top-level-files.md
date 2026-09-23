> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Top-Level Files
**In one sentence:** The top-level files provide the runnable two-turn demo (`main.py`), the full speech-to-speech agent engine (`voicechat_agent.py`), and the ignore rules (`.gitignore`) that keep checkpoints, audio, and bytecode out of version control.
## Key points
- `main.py` is the official pipeline runner that executes two full-duplex speech-to-speech turns — general conversation plus dynamic tool calling — via `VoiceChatAgent` (main.py:22, main.py:33).
- `main.py` initializes the agent with `VoiceChatAgent(checkpoint_dir="./checkpoint")`, downloading the Hugging Face checkpoint if not present (main.py:39).
- `voicechat_agent.py` implements the `VoiceChatAgent` engine for streaming speech understanding, dialogue reasoning, and native tool calling around model `nvidia/NVIDIA-NemotronLabs-VoiceChat-11B` (voicechat_agent.py:73, voicechat_agent.py:92).
- `VoiceChatAgent.__init__` takes `checkpoint_dir: str = "./checkpoint"`, selects `cuda` vs `cpu` with `bfloat16` vs `float32`, then calls `download_checkpoint()` and `_load_model()` (voicechat_agent.py:181).
- `VoiceChatAgent.process_turn(user_audio_wav, output_audio_file="output_response.wav")` runs one spoken dialogue turn and returns `user_audio`, `generated_text`, `tool_call`, `tool_response`, `output_audio_file`, `sample_rate`, and `turn_latency_ms` (voicechat_agent.py:217, voicechat_agent.py:252).
- `execute_tool_call(tool_name, arguments)` executes three live tools — `get_weather` (via `wttr.in`), `get_stock_price`, and `get_top_news` — and returns an error dict for unrecognized names (voicechat_agent.py:119, voicechat_agent.py:172).
- `.gitignore` excludes `assets/`, `checkpoint/`, `__pycache__/`, `*.wav`, `*.mp3`, `*.log`, and `.DS_Store` (`.gitignore:1`).
---
## .gitignore
Repository hygiene: generated artifacts are never committed (`.gitignore:1`).

```gitignore
assets/
checkpoint/
__pycache__/
*.wav
*.mp3
*.log
.DS_Store
```

| Entry (`.gitignore:1`) | Purpose |
|---|---|
| `assets/` | Excludes binary/media assets directory |
| `checkpoint/` | Excludes downloaded model checkpoint directory |
| `__pycache__/` | Excludes Python bytecode cache |
| `*.wav` / `*.mp3` | Excludes input/output speech audio files |
| `*.log` | Excludes log files |
| `.DS_Store` | Excludes macOS Finder metadata |

## main.py — pipeline runner
Official pipeline runner for real full-duplex speech-to-speech inference and dynamic tool calling using `nvidia/NVIDIA-NemotronLabs-VoiceChat-11B` (main.py:22).

```python
import sys
from voicechat_agent import VoiceChatAgent

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')


def run_voicechat_demo():
    # Initialize agent (downloads Hugging Face checkpoint if not present)
    agent = VoiceChatAgent(checkpoint_dir="./checkpoint")  # main.py:39
```

| Demo step (main.py:33) | Call | Inputs / outputs |
|---|---|---|
| Scenario 1: General Knowledge Conversation Turn (main.py:42) | `agent.process_turn(query_audio_1, output_audio_file="general_conversation_output.wav")` (main.py:44) | Input `general_conversation.wav` (main.py:43); prints `result_1['user_audio']`, `result_1['generated_text']`, `result_1['output_audio_file']` (main.py:46) |
| Scenario 2: Dynamic Tool Calling Turn, Mumbai Weather (main.py:51) | `agent.process_turn(query_audio_2, output_audio_file="mumbai_weather_output.wav")` (main.py:53) | Input `mumbai_weather_tool_call.wav` (main.py:52); prints `result_2['user_audio']`, `result_2['tool_call']`, `result_2['tool_response']`, `result_2['output_audio_file']` (main.py:55) |

Entry point calls `run_voicechat_demo()` under `if __name__ == "__main__":` (main.py:65).

## voicechat_agent.py — agent engine
Full-duplex real-time speech AI engine for streaming speech understanding, dialogue reasoning, and native tool calling (voicechat_agent.py:73).

```python
MODEL_ID = "nvidia/NVIDIA-NemotronLabs-VoiceChat-11B"  # voicechat_agent.py:92
```

### System prompt and tool protocol
Official system prompt for the Nemotron VoiceChat tool-calling protocol (voicechat_agent.py:94). Verbatim decision process (voicechat_agent.py:97):

> 1. Does the request match one of your available tools below? If yes, you MUST call that tool - never answer it directly from your own knowledge, even if you think you know the answer.
> 2. Is it a general knowledge question (history, science, geography, math, facts, etc.)? If yes, answer directly from your own knowledge - do not call any tool.
> 3. Does it require an external action or live data that none of your tools cover (e.g. ordering food, sending email)? If yes, politely say you don't have that capability.

Constraints stated verbatim in the prompt (voicechat_agent.py:102): call a tool ONLY when the request matches `<AVAILABLE_TOOLS>`; never invent or call a tool name not literally listed (voicechat_agent.py:102). Tool-call arguments must be values the user spoke; if a required argument is missing, ask the user and never guess (voicechat_agent.py:104). On tool failure, do not retry for the same request; report the API issue (voicechat_agent.py:106).

| Tool (voicechat_agent.py:109) | Description | Parameters (`required`) |
|---|---|---|
| `get_weather` | Get the current weather for a city | `city: string` (`["city"]`) |
| `get_stock_price` | Get the current stock price for a given ticker symbol | `symbol: string` (`["symbol"]`) |
| `get_top_news` | Get today's top one news headline from Google News | `topic: string` (`[]`) |

Wire format (voicechat_agent.py:111): call with `<TOOLCALL>[{"name": "tool_name1", "arguments": {"arg1": "val1"}}]</TOOLCALL>` (voicechat_agent.py:112); tool results return as `<TOOL_RESPONSE>[{"tool_response1"}]</TOOL_RESPONSE>` (voicechat_agent.py:114).

### execute_tool_call
Real dynamic live tool execution handler fetching live data over HTTP for predicted parameters (voicechat_agent.py:119):

```python
def execute_tool_call(tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:  # voicechat_agent.py:119
```

| Branch | Behavior |
|---|---|
| `get_weather` (voicechat_agent.py:124) | Reads `arguments.get("city", "")`, errors with `City parameter is missing.` when empty (voicechat_agent.py:125); fetches `https://wttr.in/{city}?format=j1` with `User-Agent: Mozilla/5.0` and 5 s timeout, returning `status`, `city`, `temperature` (`temp_C`), `condition` (`weatherDesc`), `humidity`, `wind` (`windspeedKmph`) (voicechat_agent.py:131); on exception returns `status: success` fallback `28°C / Light rain / 87% / 19 km/h` for that city (voicechat_agent.py:146) |
| `get_stock_price` (voicechat_agent.py:155) | Uppercases `arguments.get("symbol", "")` and returns `status`, `symbol`, `query_time: Real-time`, `status_msg: Fetched live market data for ticker {symbol}` (voicechat_agent.py:156) |
| `get_top_news` (voicechat_agent.py:164) | Lowercases `arguments.get("topic", "technology")` and returns `status`, `topic`, fixed headline `NVIDIA announces new breakthrough capabilities in Nemotron VoiceChat 11B.` (voicechat_agent.py:165) |
| Unknown tool (voicechat_agent.py:172) | Returns `{"status": "error", "message": f"Tool '{tool_name}' not recognized in available tools registry."}` (voicechat_agent.py:173) |

### VoiceChatAgent class
Official agent that downloads the checkpoint, initializes PyTorch CUDA models, and runs full-duplex streaming speech inference (voicechat_agent.py:176).

```python
class VoiceChatAgent:  # voicechat_agent.py:176
    def __init__(self, checkpoint_dir: str = "./checkpoint"):  # voicechat_agent.py:181
        self.checkpoint_dir = checkpoint_dir
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.torch_dtype = torch.bfloat16 if torch.cuda.is_available() else torch.float32
```

Optional `transformers` import sets `HAS_TRANSFORMERS` (`AutoModelForCausalLM, AutoTokenizer, AutoProcessor`), else `False` (voicechat_agent.py:86). Constructor flow (voicechat_agent.py:181): Step 1 downloads the checkpoint via `self.download_checkpoint()` (voicechat_agent.py:187); Step 2 sets `self.tokenizer = None`, `self.model = None`, then calls `self._load_model()` (voicechat_agent.py:190).

`download_checkpoint() -> str` downloads the official checkpoint from Hugging Face (voicechat_agent.py:194): if `checkpoint_dir` is missing or empty, prints `📥 Downloading official {MODEL_ID} checkpoint...` and calls `snapshot_download(repo_id=MODEL_ID, local_dir=checkpoint_dir, resume_download=True)` (voicechat_agent.py:196); otherwise returns `checkpoint_dir` unchanged (voicechat_agent.py:200).

`_load_model()` loads the Nemotron Nano V2 9B LLM backbone and Fast Conformer speech encoder/decoder (voicechat_agent.py:202): prints `⚙️ Loading NVIDIA Nemotron VoiceChat 11B pipeline on {device}...` (voicechat_agent.py:204); only when `HAS_TRANSFORMERS` and `model_path` exists, loads `AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)` and `AutoModelForCausalLM.from_pretrained(model_path, torch_dtype=torch_dtype, device_map="auto" if CUDA else None, trust_remote_code=True)`, printing `Checkpoint setup info: {e}` on failure (voicechat_agent.py:205).

`process_turn(user_audio_wav: str, output_audio_file: str = "output_response.wav") -> Dict[str, Any]` runs one end-to-end full-duplex spoken dialogue turn (voicechat_agent.py:217): encodes 16 kHz WAV input via the Fast Conformer encoder, generates dialogue tokens or `<TOOLCALL>` via the Nemotron Nano V2 9B backbone, executes a live API call and feeds back `<TOOL_RESPONSE>` when predicted, and synthesizes 22.05 kHz output WAV via the neural TTS decoder (voicechat_agent.py:218). Implementation builds `full_prompt = f"{SYSTEM_PROMPT}\nUser Input: {user_audio_wav}"` (voicechat_agent.py:225); when model and tokenizer exist, tokenizes to the device, runs `model.generate(**inputs, max_new_tokens=256)` under `torch.no_grad()`, and decodes with `skip_special_tokens=True`, else `generated_text = ""` (voicechat_agent.py:227). It parses `re.search(r"<TOOLCALL>(.*?)</TOOLCALL>", generated_text)` (voicechat_agent.py:236); on match, JSON-parses group 1, takes `payload[0]["name"]` and `payload[0]["arguments"]`, calls `execute_tool_call(tool_name, tool_args)`, and wraps the result as `<TOOL_RESPONSE>[{json}]>` (voicechat_agent.py:240); parse failures yield `<TOOL_RESPONSE>[{"error": "{e}"}]` (voicechat_agent.py:249). Return dict keys (voicechat_agent.py:252): `user_audio` (echo of input), `generated_text`, `tool_call` (`<TOOLCALL>{json}</TOOLCALL>` or `None`), `tool_response`, `output_audio_file`, `sample_rate: "22.05 kHz"` (voicechat_agent.py:258), `turn_latency_ms: 448.0` (voicechat_agent.py:259).

**Covers:** `.gitignore`, `main.py`, `voicechat_agent.py`
