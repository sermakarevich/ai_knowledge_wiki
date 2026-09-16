> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Model seam, fake provider, pricing

**In one sentence:** All model access goes through the free `chat()` function dispatched by `Provider` config, with an OpenAI-compatible HTTP path and a deterministic fake responder plus substring-matched USD pricing.

## Key points
- The `chat()` seam in `model/client.py:18` is the sole entry point — every model call in the course goes through it (`model/client.py:1`).
- `Provider` in `model/provider.py:78` is pure config (`base_url` / `model` / `api_key`) plus an optional `responder` callable; `chat()` calls `responder` when set, else `complete_openai` (`model/client.py:38`).
- `complete_openai()` in `model/openai_compatible.py:23` POSTs to `{base_url}/chat/completions` (`model/openai_compatible.py:59`) and supports blocking plus SSE streaming via `on_delta` (`model/openai_compatible.py:56`).
- `FakeProvider` in `model/fake.py:22` and `fake()` in `model/fake.py:48` provide the offline second implementation: callable / per-turn list / fixed default replies (`model/fake.py:37`).
- `LLMResponse` in `model/provider.py:68` normalizes all results to `content` / `reasoning` / `tool_calls` / `usage` / `finish_reason` / `raw`.
- Pricing in `model/pricing.py:17` maps model-id substrings to `(prompt, completion)` USD-per-1M rates; unknown/local models cost `0.0` (`model/pricing.py:26`).
- Package surface is re-exported in `model/__init__.py:12` (`chat`, `Provider`, `FakeProvider`, `fake`, `complete_openai`, pricing helpers, presets, defaults).

---

## The `chat()` seam

The seam is a free module-level function by design, so callers do `from model import chat` and tests can `patch.object(mod, "chat")` (`model/client.py:8`).

Quoted verbatim (`model/client.py:18`):

```python
def chat(
    messages: list[dict],
    *,
    model: str | None = None,
    tools: list | None = None,
    temperature: float = 0.0,
    max_tokens: int = 1024,
    timeout: float = 180.0,
    provider: Provider | None = None,
    on_delta: OnDelta | None = None,
) -> LLMResponse:
```

Dispatch logic (`model/client.py:38`):

```python
provider = provider or Provider.from_env()
if provider.responder is not None:
    resp = provider.responder(
        messages,
        model=model,
        tools=tools,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    if on_delta is not None:
        if resp.reasoning:
            on_delta("reasoning", resp.reasoning)
        if resp.content:
            on_delta("content", resp.content)
    return resp
return complete_openai(
    provider,
    messages,
    model=model,
    tools=tools,
    temperature=temperature,
    max_tokens=max_tokens,
    timeout=timeout,
    on_delta=on_delta,
)
```

Notes:
- `max_tokens` defaults to `1024` because the default model is a reasoning model that spends tokens on `reasoning_content` before visible content (`model/client.py:31`).
- A `responder` provider has no network to stream, so its final content is replayed through `on_delta` once, keeping the streaming path exercised offline (`model/client.py:34`).

## `Provider` config and `LLMResponse`

Quoted verbatim (`model/provider.py:24`):

```python
DEFAULT_BASE_URL = "http://localhost:1234/v1"
DEFAULT_MODEL = "google/gemma-4-26b-a4b"
DEFAULT_API_KEY = "lm-studio"
```

Streaming sink type (`model/provider.py:31`):

```python
OnDelta = Callable[[str, str], None]
```

Response shape (`model/provider.py:67`):

```python
@dataclass
class LLMResponse:
    content: str
    reasoning: str | None = None
    tool_calls: list = field(default_factory=list)
    usage: dict = field(default_factory=dict)
    finish_reason: str | None = None
    raw: dict = field(default_factory=dict)
```

Provider shape (`model/provider.py:77`):

```python
@dataclass
class Provider:
    base_url: str
    model: str
    api_key: str = "x"
    responder: Callable[..., LLMResponse] | None = None
```

Behavior:
- `Provider.from_env()` in `model/provider.py:94` loads `.env` via the minimal loader in `model/provider.py:52` (real env vars always win) and reads `LLM_BASE_URL` / `LLM_MODEL` / `LLM_API_KEY` with the defaults above (`model/provider.py:97`).
- `from_env` always leaves `responder` as `None` — env-configured providers go over HTTP (`model/provider.py:83`).
- Presets switch the same agent in one line (`model/provider.py:104`): `lmstudio()` in `model/provider.py:105` targets `http://localhost:1234/v1`, `openrouter()` in `model/provider.py:109` targets `https://openrouter.ai/api/v1`, `ollama()` in `model/provider.py:113` targets `http://localhost:11434/v1`, `openai()` in `model/provider.py:117` targets `https://api.openai.com/v1`.
- `.env` parsing strips inline `# comments` and matching surrounding quotes via `_unquote` in `model/provider.py:34`, and honors `export KEY=value` lines (`model/provider.py:61`).

## OpenAI-compatible HTTP path

Quoted verbatim (`model/openai_compatible.py:23`):

```python
def complete_openai(
    provider: Provider,
    messages: list[dict],
    *,
    model: str | None = None,
    tools: list | None = None,
    temperature: float = 0.0,
    max_tokens: int = 1024,
    timeout: float = 180.0,
    on_delta: OnDelta | None = None,
) -> LLMResponse:
```

Blocking path:
- Builds `payload` with `model`, `messages`, `temperature`, `max_tokens`, plus `tools` only when set (`model/openai_compatible.py:47`).
- POSTs with `Authorization: Bearer <api_key>` header (`model/openai_compatible.py:59`) to `f"{base_url}/chat/completions"` (`model/openai_compatible.py:60`).
- Treats HTTP-200-with-`{"error": ...}` or empty `choices` as `RuntimeError(f"model returned no choices: {detail}")` instead of a bare `KeyError`/`IndexError` (`model/openai_compatible.py:71`).
- Maps `choices[0].message` to `content` / `reasoning_content` / `tool_calls`, passes through `usage` (with `usage: null` coerced to `{}`), `finish_reason`, and `raw` (`model/openai_compatible.py:78`).

Streaming path:
- `_stream_openai()` in `model/openai_compatible.py:106` adds `"stream": True` and `"stream_options": {"include_usage": True}` (`model/openai_compatible.py:114`), uses `httpx.stream` POST (`model/openai_compatible.py:115`), and folds chunks via `assemble_stream` (`model/openai_compatible.py:123`).
- `_iter_sse_chunks()` in `model/openai_compatible.py:88` yields parsed JSON per `data:` line, skips blanks/keep-alives, stops at `[DONE]`, and skips non-JSON lines (`model/openai_compatible.py:94`).
- `assemble_stream()` in `model/openai_compatible.py:126` is pure over parsed chunk dicts (testable offline); it accumulates `content` / `reasoning`, merges tool-call fragments by `index`, and takes `usage` / `finish_reason` from trailing chunks (`model/openai_compatible.py:141`).
- `_merge_tool_call()` in `model/openai_compatible.py:170` keys the accumulator by `index` with default `{"id": "", "type": "function", "function": {"name": "", "arguments": ""}}` (`model/openai_compatible.py:173`); the first fragment carries `id`/`name`, later ones append `arguments` (`model/openai_compatible.py:176`).

## Fake provider

Quoted verbatim (`model/fake.py:27`):

```python
def __init__(
    self,
    *,
    scripted: Callable[[list[dict]], str] | list[str] | None = None,
    default: str = "ok",
) -> None:
```

Quoted verbatim (`model/fake.py:37`):

```python
def __call__(self, messages: list[dict], **_kwargs) -> LLMResponse:
```

Quoted verbatim (`model/fake.py:48`):

```python
def fake(
    *,
    scripted: Callable[[list[dict]], str] | list[str] | None = None,
    default: str = "ok",
) -> Provider:
```

Behavior:
- `FakeProvider` in `model/fake.py:22` counts calls with `itertools.count()` (`model/fake.py:35`); a callable `scripted` is invoked with `messages` (`model/fake.py:39`), a non-empty list is consumed in order then the last reply repeats via `scripted[min(i, len(scripted) - 1)]` (`model/fake.py:41`), otherwise `default` (`"ok"`) is returned (`model/fake.py:43`).
- Every call returns `LLMResponse(content=content, finish_reason="stop")` (`model/fake.py:45`).
- `fake()` builds `Provider(base_url="fake://local", model="fake", api_key="x", responder=FakeProvider(...))` (`model/fake.py:54`).
- Canonical usages from the module docstring (`model/fake.py:7`): `Agent(provider=fake(scripted=lambda msgs: "PONG"))`, `Agent(provider=fake(scripted=["a", "b"]))`, `Agent(provider=fake())`.

## Pricing and cost

Quoted verbatim (`model/pricing.py:17`):

```python
PRICES: dict[str, tuple[float, float]] = {
    "gpt-4o-mini": (0.15, 0.60),
    "gpt-4o": (2.50, 10.00),
    "claude-3-5-haiku": (0.80, 4.00),
    "claude-3-5-sonnet": (3.00, 15.00),
    "llama-3.1-70b": (0.12, 0.30),
}
```

Quoted verbatim (`model/pricing.py:26`):

```python
def price_for(model: str | None) -> tuple[float, float]:
```

Quoted verbatim (`model/pricing.py:37`):

```python
def cost(model: str | None, prompt_tokens: int, completion_tokens: int = 0) -> float:
```

Quoted verbatim (`model/pricing.py:43`):

```python
def cost_from_usage(model: str | None, usage: dict) -> float:
```

Quoted verbatim (`model/pricing.py:55`):

```python
def format_cost(dollars: float) -> str:
```

Behavior:
- Rates are USD per 1,000,000 tokens, illustrative — edit `PRICES` per provider (`model/pricing.py:16`).
- `price_for` lowercases the model id and matches by substring, returning `(0.0, 0.0)` for empty/unknown/local models (`model/pricing.py:28`).
- `cost` computes `(prompt_tokens * p_rate + completion_tokens * c_rate) / 1_000_000` (`model/pricing.py:40`).
- `cost_from_usage` returns `0.0` on empty usage (`model/pricing.py:46`); when prompt/completion split is missing it prices `total_tokens` at the prompt rate (`model/pricing.py:50`).
- `format_cost` renders `f"${dollars:.4f}"` so sub-cent calls stay visible (`model/pricing.py:57`).

## Package surface

`model/__init__.py:12` re-exports `chat`, `FakeProvider`, `fake`, `complete_openai`, `PRICES`, `cost`, `cost_from_usage`, `format_cost`, `price_for`, `Provider`, `LLMResponse`, `OnDelta`, `DEFAULT_API_KEY`, `DEFAULT_BASE_URL`, `DEFAULT_MODEL`, `lmstudio`, `ollama`, `openai`, `openrouter`, with `__all__` in `model/__init__.py:35`. The package docstring states the extension rule: add a model without touching the harness — the harness depends only on `chat` and `Provider` (`model/__init__.py:1`).

**Covers:** component 02
