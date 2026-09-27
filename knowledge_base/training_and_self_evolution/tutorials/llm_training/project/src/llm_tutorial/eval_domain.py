"""Chapter 08 — the domain harness: CyberMetric, a 4-option multiple-choice cybersecurity quiz.

    download split                          - fetch a CyberMetric split into runs/data/cybermetric/
    evaluate-hf model_dir --split 2000       - greedy-letter or loglik accuracy on an HF checkpoint
    evaluate-ollama name --split 500         - same, through Ollama's /api/chat

Two scoring modes:
- "letter" (default): render the question as text, generate up to 8 tokens, parse the first
  A-D letter out of the reply. Simple, matches how a chat model is actually used, but a model
  that never learned to answer "just the letter" can score nearly 0 even if it "knows" the
  answer — small/undertrained models are especially prone to this.
- "loglik": score P(A) vs P(B) vs P(C) vs P(D) directly from the model's next-token logits after
  the prompt, and take the argmax. This is what `lm_eval`'s multiple-choice tasks do internally
  (chapter 08's general suite) and it is far more robust for small models: it never depends on
  the model choosing to *format* its answer as a bare letter.
"""

import json
import math
import random
import re
import unicodedata
from pathlib import Path

import httpx
import typer
from rich.console import Console

app = typer.Typer(add_completion=False, help=__doc__)
console = Console()

CYBERMETRIC_BASE_URL = "https://huggingface.co/datasets/tihanyin/CyberMetric/resolve/main"
DEFAULT_CACHE_DIR = Path("runs/data/cybermetric")
DEFAULT_OLLAMA_URL = "http://127.0.0.1:11434"
LETTERS = ("A", "B", "C", "D")


# --------------------------------------------------------------------------------- download


def download_split(split: str, cache_dir: str | Path = DEFAULT_CACHE_DIR, timeout: float = 120.0) -> Path:
    """Download `CyberMetric-<split>-v1.json` (split in {"500", "2000", "10000"}) into
    `cache_dir`, skipping the request if the file is already there."""
    cache_dir = Path(cache_dir)
    cache_dir.mkdir(parents=True, exist_ok=True)
    filename = f"CyberMetric-{split}-v1.json"
    out_path = cache_dir / filename
    if out_path.exists():
        return out_path
    resp = httpx.get(f"{CYBERMETRIC_BASE_URL}/{filename}", timeout=timeout, follow_redirects=True)
    resp.raise_for_status()
    out_path.write_bytes(resp.content)
    return out_path


def load_split(split: str, cache_dir: str | Path = DEFAULT_CACHE_DIR) -> list[dict]:
    """Load `runs/data/cybermetric/CyberMetric-<split>-v1.json`, downloading it first if needed.

    Structure (verified against the real dataset, 2026-08-30):
    `{"questions": [{"question": str, "answers": {"A": str, ..., "D": str},
    "solution": "A".."D", "category": str (optional, present in some splits)}]}`.
    """
    path = download_split(split, cache_dir)
    data = json.loads(path.read_text())
    return data["questions"]


# --------------------------------------------------------------------------------- dedup


def _normalise(text: str) -> str:
    text = unicodedata.normalize("NFKC", text).lower()
    return " ".join(text.split())


def dedup_train(train_items: list[dict], eval_items: list[dict]) -> list[dict]:
    """Remove any `train_items` question whose normalised text also appears in `eval_items`
    (whitespace/case-insensitive). CyberMetric-10000 is a superset built independently of
    CyberMetric-2000/-500, so without this, training on the 10000-split would leak eval questions."""
    eval_texts = {_normalise(item["question"]) for item in eval_items}
    return [item for item in train_items if _normalise(item["question"]) not in eval_texts]


# --------------------------------------------------------------------------------- prompt


def format_mcq(item: dict, style: str = "letter") -> str:
    """Render one CyberMetric item as a prompt: the question, the four options as `A) ... D) ...`,
    and an instruction to answer with the letter only."""
    lines = [item["question"], ""]
    for letter in LETTERS:
        lines.append(f"{letter}) {item['answers'][letter]}")
    lines.append("")
    lines.append("Answer with the letter only.")
    return "\n".join(lines)


_LETTER_RE = re.compile(r"(?:answer\s*:?\s*)?\(?\b([A-D])\b\)?", re.IGNORECASE)


def parse_letter(text: str) -> str | None:
    """Extract the first standalone A-D letter from a model reply. Handles a bare letter
    ("B"), "Answer: B", "(C)", and a letter followed by punctuation ("A."). Returns None if
    no letter is found (an unparsable/refused answer, scored as wrong)."""
    match = _LETTER_RE.search(text.strip())
    if match is None:
        return None
    return match.group(1).upper()


# --------------------------------------------------------------------------------- bootstrap CI


def ci95(correct: list[bool], n_boot: int = 2000, seed: int = 1234) -> tuple[float, float]:
    """A 95% bootstrap confidence interval for the mean of a 0/1 list (accuracy).

    Resamples `correct` with replacement `n_boot` times, takes the mean each time, and returns
    the 2.5th/97.5th percentile of that distribution. On CyberMetric-500 (n=500) a 1-2 point
    difference between two runs is routinely *inside* this interval — i.e. noise, not a real
    difference — which is why the chapter reports it next to every accuracy number.
    """
    if not correct:
        return (0.0, 0.0)
    rng = random.Random(seed)
    n = len(correct)
    means = []
    for _ in range(n_boot):
        sample = [correct[rng.randrange(n)] for _ in range(n)]
        means.append(sum(sample) / n)
    means.sort()
    lo = means[int(0.025 * n_boot)]
    hi = means[min(int(0.975 * n_boot), n_boot - 1)]
    return (lo, hi)


# --------------------------------------------------------------------------------- HF evaluation


def evaluate_hf(
    model_dir: str,
    split: str = "2000",
    batch_size: int = 16,
    adapter: str | None = None,
    chat: bool = True,
    mode: str = "letter",
    cache_dir: str | Path = DEFAULT_CACHE_DIR,
    load_in_4bit: bool = False,
) -> dict:
    """Greedy-generate (mode="letter") or score-by-logprob (mode="loglik") CyberMetric answers
    for an HF checkpoint. Needs GPU/`transformers` — not exercised by the CPU test suite.

    `load_in_4bit=True` (added in chapter 09) loads the base in 4-bit NF4 instead of bf16. It is
    the only way to evaluate a 27B model on a 24 GB card: bf16 weights alone would be ~54 GB. The
    accuracy it reports is therefore the accuracy *of the quantised model*, which is the model the
    QLoRA adapter was trained against anyway.
    """
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    from .chat import attach_chat_template, render

    items = load_split(split, cache_dir)
    tokenizer = AutoTokenizer.from_pretrained(model_dir)
    if chat and tokenizer.chat_template is None:
        attach_chat_template(tokenizer)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    load_kwargs: dict = {"dtype": torch.bfloat16 if device == "cuda" else torch.float32}
    if load_in_4bit:
        from transformers import BitsAndBytesConfig

        load_kwargs["quantization_config"] = BitsAndBytesConfig(
            load_in_4bit=True, bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.bfloat16, bnb_4bit_use_double_quant=True,
        )
        # A 4-bit model cannot be moved with `.to()` afterwards — it has to be placed at load time.
        load_kwargs["device_map"] = {"": 0}
    model = AutoModelForCausalLM.from_pretrained(model_dir, **load_kwargs)
    if adapter:
        from peft import PeftModel

        model = PeftModel.from_pretrained(model, adapter)
    model = model.eval() if load_in_4bit else model.to(device).eval()

    correct: list[bool] = []
    per_category: dict[str, list[bool]] = {}
    for item in items:
        prompt_text = format_mcq(item)
        if chat:
            prompt = render([{"role": "user", "content": prompt_text}], tokenizer, add_generation_prompt=True)
        else:
            prompt = prompt_text
        inputs = tokenizer(prompt, return_tensors="pt", add_special_tokens=not chat).to(device)

        if mode == "loglik":
            predicted = _score_loglik(model, tokenizer, inputs)
        else:
            with torch.no_grad():
                generated = model.generate(
                    **inputs, max_new_tokens=8, do_sample=False,
                    pad_token_id=tokenizer.pad_token_id or tokenizer.eos_token_id,
                )
            reply = tokenizer.decode(generated[0, inputs["input_ids"].shape[1]:], skip_special_tokens=True)
            predicted = parse_letter(reply)

        is_correct = predicted == item["solution"]
        correct.append(is_correct)
        category = item.get("category")
        if category:
            per_category.setdefault(category, []).append(is_correct)

    accuracy = sum(correct) / len(correct)
    return {
        "dataset": "CyberMetric",
        "split": split,
        "n": len(correct),
        "accuracy": accuracy,
        "ci95": ci95(correct),
        "per_category": {cat: sum(vals) / len(vals) for cat, vals in per_category.items()},
    }


def _score_loglik(model, tokenizer, inputs) -> str:
    """Score the 4 letter continuations by summed log-probability of their first token and
    return the highest-scoring letter (the ~20-line "loglik" mode)."""
    import torch

    with torch.no_grad():
        logits = model(**inputs).logits[0, -1]
    log_probs = torch.log_softmax(logits, dim=-1)
    best_letter, best_score = None, -math.inf
    for letter in LETTERS:
        token_ids = tokenizer.encode(letter, add_special_tokens=False)
        if not token_ids:
            continue
        score = log_probs[token_ids[0]].item()
        if score > best_score:
            best_letter, best_score = letter, score
    return best_letter


# --------------------------------------------------------------------------------- perplexity


def perplexity(model, tokenizer, texts: list[str], max_len: int = 1024, batch_size: int = 4) -> dict:
    """Mean negative log-likelihood per token (and its exponential, the perplexity) of `texts`.

    Accuracy is a *step function*: a model can drift a long way before a single answer letter
    flips, and then several flip at once. Perplexity is continuous — "how surprised is the model
    by this text" — so it sees drift that accuracy is still rounding away. Chapter 10 records two
    of them for every variant: on the correct CyberMetric answers (does the model still like the
    domain?) and on held-out SmolTalk chats (does it still like ordinary conversation?).

    Takes an already-loaded `model` and `tokenizer` rather than a path, because chapter 10 calls it
    several times against one model that took a minute to load. Padding tokens are masked out with
    `-100` so a short text in a batch of long ones does not get counted as a run of easy tokens.
    """
    import torch

    device = next(model.parameters()).device
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token = tokenizer.eos_token
    total_nll, total_tokens = 0.0, 0
    for start in range(0, len(texts), batch_size):
        batch = texts[start : start + batch_size]
        enc = tokenizer(batch, return_tensors="pt", padding=True, truncation=True,
                        max_length=max_len).to(device)
        labels = enc["input_ids"].clone()
        labels[enc["attention_mask"] == 0] = -100
        with torch.no_grad():
            logits = model(input_ids=enc["input_ids"], attention_mask=enc["attention_mask"]).logits
        # Next-token prediction: logits at position i predict the token at position i+1.
        shift_logits = logits[:, :-1, :].float()
        shift_labels = labels[:, 1:]
        loss = torch.nn.functional.cross_entropy(
            shift_logits.reshape(-1, shift_logits.size(-1)), shift_labels.reshape(-1),
            ignore_index=-100, reduction="sum",
        )
        total_nll += loss.item()
        total_tokens += int((shift_labels != -100).sum())
    mean_nll = total_nll / max(total_tokens, 1)
    return {"nll": mean_nll, "perplexity": math.exp(min(mean_nll, 20.0)), "n_texts": len(texts),
            "n_tokens": total_tokens}


def domain_perplexity_texts(items: list[dict]) -> list[str]:
    """The question plus its *correct* answer, in the same shape training used — the text a
    domain-specialised model should find least surprising."""
    return [f"{format_mcq(item)}\n{item['solution']}) {item['answers'][item['solution']]}" for item in items]


# --------------------------------------------------------------------------------- Ollama evaluation


def evaluate_ollama(
    model_name: str,
    split: str = "500",
    base_url: str = DEFAULT_OLLAMA_URL,
    cache_dir: str | Path = DEFAULT_CACHE_DIR,
    timeout: float = 120.0,
) -> dict:
    """Same accuracy computation, generating through Ollama's `/api/chat` (`think: false`,
    `temperature 0`) instead of a local HF forward pass."""
    items = load_split(split, cache_dir)
    correct: list[bool] = []
    per_category: dict[str, list[bool]] = {}
    for item in items:
        payload = {
            "model": model_name,
            "messages": [{"role": "user", "content": format_mcq(item)}],
            "stream": False,
            "think": False,
            "options": {"temperature": 0},
        }
        resp = httpx.post(f"{base_url}/api/chat", json=payload, timeout=timeout)
        resp.raise_for_status()
        reply = resp.json()["message"]["content"]
        predicted = parse_letter(reply)
        is_correct = predicted == item["solution"]
        correct.append(is_correct)
        category = item.get("category")
        if category:
            per_category.setdefault(category, []).append(is_correct)

    accuracy = sum(correct) / len(correct)
    return {
        "dataset": "CyberMetric",
        "split": split,
        "n": len(correct),
        "accuracy": accuracy,
        "ci95": ci95(correct),
        "per_category": {cat: sum(vals) / len(vals) for cat, vals in per_category.items()},
    }


# --------------------------------------------------------------------------------- CLI


@app.command()
def download(split: str = typer.Argument(..., help='"500", "2000" or "10000"')) -> None:
    path = download_split(split)
    console.print(f"downloaded {path}")


@app.command(name="evaluate-hf")
def evaluate_hf_cmd(
    model_dir: str = typer.Argument(...),
    split: str = typer.Option("2000"),
    batch_size: int = typer.Option(16),
    adapter: str = typer.Option(None),
    mode: str = typer.Option("letter", help='"letter" or "loglik"'),
    load_in_4bit: bool = typer.Option(False, help="load the base in 4-bit NF4 (needed for the 27B)"),
) -> None:
    from .config import write_metrics

    result = evaluate_hf(model_dir, split=split, batch_size=batch_size, adapter=adapter, mode=mode,
                         load_in_4bit=load_in_4bit)
    console.print(result)
    run_dir = Path("runs/eval_baselines") / Path(model_dir).name
    write_metrics(run_dir, {"domain": result})


@app.command(name="evaluate-ollama")
def evaluate_ollama_cmd(
    name: str = typer.Argument(...),
    split: str = typer.Option("500"),
    base_url: str = typer.Option(DEFAULT_OLLAMA_URL, help="Ollama base URL, e.g. http://127.0.0.1:11434"),
) -> None:
    from .config import write_metrics

    result = evaluate_ollama(name, split=split, base_url=base_url)
    console.print(result)
    write_metrics(Path("runs/eval_baselines") / name.replace(":", "_"), {"domain": result})


if __name__ == "__main__":
    app()
