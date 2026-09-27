"""Chapter 09 — domain fine-tuning with LoRA / QLoRA.

    prepare-data                     - build runs/data/cybermetric/train_dedup.json
    train  configs/ft_*.yaml         - LoRA (or QLoRA) SFT, writes runs/<run>/adapter + metrics.json
    evaluate run                     - domain accuracy + general suite for a finished run
    merge  run                       - merge_and_unload() the adapter into a bf16 checkpoint
    ablate configs/ablation_4b.yaml  - loop a list of variants, write summary.json + ablation.png
    samples run                      - before/after generations for 6 fixed prompts

LoRA (Low-Rank Adaptation) freezes every pretrained weight matrix `W` and learns a small update
`ΔW = B·A` beside it, where `A` is `r × in` and `B` is `out × r` with `r` (the *rank*) much
smaller than either dimension. The forward pass becomes `y = W·x + (alpha/r) · B·(A·x)`. Only `A`
and `B` get gradients, so the optimizer state — the single biggest slice of training memory —
shrinks by the same factor as the parameter count.

QLoRA adds one more trick: the frozen `W` is stored in 4-bit NF4 (a normal-float quantisation
grid tuned for normally-distributed weights) and de-quantised to bf16 on the fly inside each
matmul. The adapters stay in bf16, so the *learned* part is full precision while the *frozen*
part costs a quarter of the memory. That is what lets a 27B model train on one 24 GB card.
"""

import json
import re
import time
from pathlib import Path
from typing import Literal

import typer
import yaml
from pydantic import BaseModel, ConfigDict, Field
from rich.console import Console
from rich.table import Table

from .config import load_yaml, write_metrics
from .eval_domain import DEFAULT_CACHE_DIR, dedup_train, format_mcq, load_split

app = typer.Typer(add_completion=False, help=__doc__)
console = Console()

TRAIN_FILE = "runs/data/cybermetric/train_dedup.json"

# ---------------------------------------------------------------------------------- config


class ReplayConfig(BaseModel):
    """Chapter 10 uses this: mix `n` general-chat conversations back into a domain training set
    so the model keeps its general abilities ("replay" / "rehearsal"). Chapter 09 leaves n=0."""

    model_config = ConfigDict(extra="forbid")
    dataset: str | None = None
    subsets: list[str] = Field(default_factory=lambda: ["smol-magpie-ultra"])
    n: int = 0


class DataConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")
    train_file: str = TRAIN_FILE
    format: Literal["mcq_chat", "mcq_self_distill"] = "mcq_chat"
    n_train: int | None = None
    replay: ReplayConfig = Field(default_factory=ReplayConfig)


class LoraSettings(BaseModel):
    model_config = ConfigDict(extra="forbid")
    r: int = 16
    alpha: int = 32
    dropout: float = 0.05
    # "all-linear" | "attention" | "mlp" | "attention+mlp" | an explicit list | a raw regex string
    target_modules: str | list[str] = "all-linear"
    modules_to_save: list[str] = Field(default_factory=list)


class EvalSettings(BaseModel):
    model_config = ConfigDict(extra="forbid")
    domain_split: str = "500"
    general: bool = True
    general_config: str = "configs/eval_general_4b.yaml"
    load_in_4bit: bool = False


class FTConfig(BaseModel):
    """The schema of every `configs/ft_*.yaml`. `extra="forbid"` + the `Literal` on `quant` mean
    a typo in the YAML fails immediately with a readable error instead of being silently ignored."""

    model_config = ConfigDict(extra="forbid")
    run_name: str
    base: str
    quant: Literal["none", "nf4"] = "none"
    lora: LoraSettings = Field(default_factory=LoraSettings)
    data: DataConfig = Field(default_factory=DataConfig)
    max_len: int = 1024
    epochs: float = 2
    lr: float = 1e-4
    schedule: str = "cosine"
    warmup_ratio: float = 0.03
    per_device_batch: int = 8
    grad_accum: int = 2
    bf16: bool = True
    gradient_checkpointing: bool = True
    liger: bool = False
    eval: EvalSettings = Field(default_factory=EvalSettings)
    seed: int = 1337

    @classmethod
    def from_yaml(cls, path: str | Path) -> "FTConfig":
        return cls.model_validate(load_yaml(path))

    @property
    def run_dir(self) -> Path:
        return Path("runs") / self.run_name

    @property
    def adapter_dir(self) -> Path:
        return self.run_dir / "adapter"


# ------------------------------------------------------------------------------ target modules

# Preset names a config may use instead of spelling out the module list.
#
# `all-linear` is peft's own magic string: every `nn.Linear` in the model except the output head.
# On Qwen3.5-4B that is 4 kinds of layer, because the model is a *hybrid*: 24 of its 32 blocks use
# Gated DeltaNet (linear-recurrent attention, projections named `in_proj_qkv`/`in_proj_z`/
# `in_proj_a`/`in_proj_b`/`out_proj`) and only 8 use ordinary Gated Attention (`q_proj`/`k_proj`/
# `v_proj`/`o_proj`). Every block has an MLP (`gate_proj`/`up_proj`/`down_proj`).
#
# Consequence: the classic "attention-only" LoRA recipe (`q_proj,k_proj,v_proj,o_proj`) adapts
# only 8 of 32 blocks on this architecture — a much weaker intervention than the same recipe on a
# pure-attention model such as Llama. We keep the DeltaNet projections OUT of the attention-only
# preset (so the ablation measures the classic recipe as people actually write it) and IN
# `all-linear` (so the recommended default really does touch every block).
TARGET_PRESETS: dict[str, str | list[str]] = {
    "all-linear": "all-linear",
    "attention": ["q_proj", "k_proj", "v_proj", "o_proj"],
    "mlp": ["gate_proj", "up_proj", "down_proj"],
    "attention+mlp": ["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
    "deltanet": ["in_proj_qkv", "in_proj_z", "in_proj_a", "in_proj_b", "out_proj"],
}

# Fallback for checkpoints that load as the multimodal `Qwen3_5ForConditionalGeneration` instead
# of the text-only `Qwen3_5ForCausalLM`: there, "all-linear" would also adapt the vision tower's
# `qkv`/`proj`/`fc1`/`fc2` layers — parameters we never train and never even feed an image to.
# This regex keeps LoRA inside the language model.
LANGUAGE_MODEL_LINEAR_RE = r".*language_model.*\.(q_proj|k_proj|v_proj|o_proj|gate_proj|up_proj|down_proj)$"


def resolve_target_modules(spec: str | list[str]) -> str | list[str]:
    """Turn a config's `lora.target_modules` into what peft's `LoraConfig` wants.

    A list passes through, a known preset name expands, and anything else is handed to peft as-is
    (peft treats a plain string as either the magic `"all-linear"` or a regex over module names).
    """
    if isinstance(spec, list):
        return spec
    return TARGET_PRESETS.get(spec, spec)


def match_module_names(pattern: str, names: list[str]) -> list[str]:
    """Which of `names` peft would adapt for a regex `target_modules` (`re.fullmatch`, the same
    rule peft uses). Pure, so the test suite can check the vision-tower regex without a GPU."""
    compiled = re.compile(pattern)
    return [name for name in names if compiled.fullmatch(name)]


def is_multimodal(model) -> bool:
    """True when the loaded class carries a vision tower next to the language model."""
    return hasattr(model, "visual") or hasattr(getattr(model, "model", None), "visual")


# ------------------------------------------------------------------------------ training data


def prepare_train_file(
    out_path: str | Path = TRAIN_FILE,
    train_split: str = "10000",
    eval_splits: tuple[str, ...] = ("2000", "500"),
    cache_dir: str | Path = DEFAULT_CACHE_DIR,
) -> dict:
    """Build the fine-tuning set: CyberMetric-10000 minus every question that also appears in the
    evaluation splits. Without this step the "domain accuracy" number would be measuring
    memorisation of questions the model was literally trained on."""
    train_items = load_split(train_split, cache_dir)
    eval_items: list[dict] = []
    for split in eval_splits:
        eval_items += load_split(split, cache_dir)
    kept = dedup_train(train_items, eval_items)
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps({"questions": kept}, indent=1))
    stats = {
        "train_split": train_split,
        "eval_splits": list(eval_splits),
        "n_before": len(train_items),
        "n_after": len(kept),
        "n_removed": len(train_items) - len(kept),
        "path": str(out_path),
    }
    console.print(stats)
    return stats


def build_train_examples(items: list[dict], tokenizer=None, style: str = "mcq_chat") -> list[dict]:
    """One CyberMetric item -> one `{"messages": [user, assistant]}` chat.

    The user turn is exactly the string chapter 08's evaluator sends (`format_mcq`), and the
    assistant turn is `"<LETTER>) <option text>"` — the letter FIRST. That ordering is not
    cosmetic: the evaluator reads the first standalone A-D letter out of the reply, so a model
    trained to say "Confidentiality, which is D" would be scored on a letter it never emitted.
    Training the answer in the shape the metric parses is part of the metric's design.
    """
    if style not in ("mcq_chat", "mcq_self_distill"):
        raise ValueError(f"unknown train example style: {style!r}")
    examples = []
    for item in items:
        letter = item["solution"]
        answer = item["answers"][letter]
        target = f"{letter}) {answer}"
        if style == "mcq_self_distill":
            # Chapter 10: train on the *base model's own* wording of the right answer (written by
            # `distill()` into the `self_answer` field) instead of the terse canned string. It is
            # still forced to begin with the letter so the evaluator parses it, but everything
            # after the letter is text the model already assigns high probability to — that is the
            # whole point: a target close to the model's own distribution moves the weights less.
            self_answer = (item.get("self_answer") or "").strip()
            if self_answer:
                target = self_answer if self_answer.startswith(f"{letter})") else f"{target}. {self_answer}"
        examples.append(
            {
                "messages": [
                    {"role": "user", "content": format_mcq(item)},
                    {"role": "assistant", "content": target},
                ]
            }
        )
    return examples


def to_prompt_completion(examples: list[dict], tokenizer) -> list[dict]:
    """Render `{"messages": ...}` chats into TRL's *prompt-completion* text format.

    Why not hand TRL the conversation and set `assistant_only_loss=True` (what chapter 05 did)?
    Because that flag needs `{% generation %}` tags in the chat template to know which tokens are
    the assistant's, and Qwen3.5's official template has none — the mask comes back all zeros and
    the model trains on nothing. With a `{"prompt", "completion"}` pair TRL masks the prompt by
    token count instead, which needs no template cooperation at all.

    Rendering it ourselves also lets us pass `enable_thinking=False`. Left at Qwen's default the
    generation prompt ends with a bare `<think>\\n` and the model is taught to answer *inside* a
    reasoning block; with the flag off the template emits a closed, empty `<think>\\n\\n</think>`
    and the answer follows it directly — the same shape the evaluator generates against.
    """
    from .chat import render

    rows = []
    for example in examples:
        messages = example["messages"]
        prompt_messages = messages[:-1]
        completion = messages[-1]["content"]
        rows.append(
            {
                "prompt": render(prompt_messages, tokenizer, add_generation_prompt=True, enable_thinking=False),
                "completion": completion,
            }
        )
    return rows


def load_replay_examples(replay: ReplayConfig, seed: int) -> list[dict]:
    """`n` general-chat conversations from `replay.dataset` (SmolTalk), as `{"messages": ...}`.

    Multi-turn conversations are collapsed to "everything before the last assistant turn" ->
    "the last assistant turn", because the prompt-completion format has exactly one completion.
    """
    if not replay.dataset or replay.n <= 0:
        return []
    from datasets import concatenate_datasets, load_dataset

    parts = [load_dataset(replay.dataset, subset, split="train").select_columns(["messages"]) for subset in replay.subsets]
    full = concatenate_datasets(parts) if len(parts) > 1 else parts[0]
    full = full.shuffle(seed=seed).select(range(min(replay.n, len(full))))
    examples = []
    for row in full:
        messages = row["messages"]
        if len(messages) < 2 or messages[-1]["role"] != "assistant":
            continue
        examples.append({"messages": messages})
    return examples


def build_dataset(cfg: FTConfig, tokenizer):
    """The full training set: CyberMetric chats (+ optional replay), rendered and shuffled."""
    import random

    from datasets import Dataset

    items = json.loads(Path(cfg.data.train_file).read_text())["questions"]
    if cfg.data.n_train:
        items = items[: cfg.data.n_train]
    examples = build_train_examples(items, tokenizer, style=cfg.data.format)
    n_domain = len(examples)
    examples += load_replay_examples(cfg.data.replay, cfg.seed)
    n_replay = len(examples) - n_domain

    rows = to_prompt_completion(examples, tokenizer)
    random.Random(cfg.seed).shuffle(rows)
    console.print(f"train rows: {len(rows)} ({n_domain} domain + {n_replay} replay)")
    return Dataset.from_list(rows), {"n_domain": n_domain, "n_replay": n_replay}


# ------------------------------------------------------------------------------ self-distillation

SELF_DISTILL_FILE = "runs/data/cybermetric/train_selfdistill.json"

# The distillation prompt. The model is TOLD the right answer and asked only to phrase it — we are
# not testing it, we are harvesting its own style. "One or two sentences" keeps the target short
# enough that 160 new tokens almost always contain a complete thought.
SELF_DISTILL_SYSTEM = (
    "You are a cybersecurity expert writing model answers for a study guide. "
    "You are given a multiple-choice question and the correct option. "
    "Reply with the correct option letter and text, then one or two sentences explaining why it is "
    "correct. Start your reply with the letter."
)


def build_distill_prompt(item: dict) -> str:
    letter = item["solution"]
    return (
        f"{format_mcq(item)}\n\n"
        f"The correct answer is {letter}) {item['answers'][letter]}.\n"
        "Write the study-guide answer now."
    )


def distill(
    base: str = "Qwen/Qwen3.5-4B",
    train_file: str = TRAIN_FILE,
    out_path: str = SELF_DISTILL_FILE,
    max_new_tokens: int = 160,
    batch_size: int = 32,
    n: int | None = None,
) -> dict:
    """Write `train_selfdistill.json`: every training question plus a `self_answer` field holding
    the *base model's own* explanation of the correct option.

    Why bother? Fine-tuning moves weights in proportion to how surprised the model is by the
    target. A canned string like "B) Confidentiality" is short but stylistically alien; the model
    has to move a long way to make it likely, and that movement is what damages unrelated
    abilities. If the target is a sentence the model would have produced anyway, the gradient is
    small where the model is already right and only sharpens *which option* it picks. This is the
    "on-policy" / self-distillation idea that the 2025-26 fine-tuning literature keeps returning
    to: keep the training distribution close to the model's own.

    Greedy (`do_sample=False`) and `enable_thinking=False`, so the run is reproducible and the
    output is an answer rather than a reasoning trace.
    """
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    from .chat import render

    items = json.loads(Path(train_file).read_text())["questions"]
    if n:
        items = items[:n]
    tokenizer = AutoTokenizer.from_pretrained(base, padding_side="left")
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token = tokenizer.eos_token
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = AutoModelForCausalLM.from_pretrained(
        base, dtype=torch.bfloat16 if device == "cuda" else torch.float32
    ).to(device).eval()

    start = time.perf_counter()
    out_items: list[dict] = []
    for offset in range(0, len(items), batch_size):
        batch = items[offset : offset + batch_size]
        prompts = [
            render(
                [{"role": "system", "content": SELF_DISTILL_SYSTEM},
                 {"role": "user", "content": build_distill_prompt(item)}],
                tokenizer, add_generation_prompt=True, enable_thinking=False,
            )
            for item in batch
        ]
        enc = tokenizer(prompts, return_tensors="pt", padding=True, add_special_tokens=False).to(device)
        with torch.no_grad():
            generated = model.generate(**enc, max_new_tokens=max_new_tokens, do_sample=False,
                                       pad_token_id=tokenizer.pad_token_id)
        replies = tokenizer.batch_decode(generated[:, enc["input_ids"].shape[1]:], skip_special_tokens=True)
        for item, reply in zip(batch, replies):
            out_items.append({**item, "self_answer": " ".join(reply.split())})
        done = offset + len(batch)
        elapsed = time.perf_counter() - start
        console.print(f"distilled {done}/{len(items)}  ({elapsed / 60:.1f} min, "
                      f"eta {elapsed / done * (len(items) - done) / 60:.1f} min)")

    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"questions": out_items}, indent=1))
    n_started_with_letter = sum(
        1 for it in out_items if it["self_answer"].startswith(f"{it['solution']})")
    )
    stats = {
        "base": base, "path": str(out), "n": len(out_items),
        "started_with_correct_letter": n_started_with_letter,
        "mean_chars": sum(len(it["self_answer"]) for it in out_items) / max(len(out_items), 1),
        "wall_seconds": time.perf_counter() - start,
    }
    console.print(stats)
    return stats


# ------------------------------------------------------------------------------ model loading


def load_base(cfg: FTConfig):
    """Load the frozen base model (bf16, or 4-bit NF4 when `quant: nf4`) and wrap it in LoRA."""
    import torch
    from peft import LoraConfig, get_peft_model
    from transformers import AutoModelForCausalLM, BitsAndBytesConfig

    cuda = torch.cuda.is_available()
    quantization_config = None
    if cfg.quant == "nf4":
        # double_quant additionally quantises the quantisation constants themselves — roughly
        # another 0.4 bits per parameter saved, free.
        quantization_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.bfloat16,
            bnb_4bit_use_double_quant=True,
        )

    model = AutoModelForCausalLM.from_pretrained(
        cfg.base,
        dtype=torch.bfloat16 if cfg.bf16 else torch.float32,
        quantization_config=quantization_config,
        device_map={"": 0} if cuda else None,
    )
    console.print(f"loaded {type(model).__name__} from {cfg.base} (quant={cfg.quant})")

    # Liger must be applied to the bare HF model: its patcher dispatches on the model class and
    # refuses a `PeftModelForCausalLM` wrapper.
    liger_status = _maybe_apply_liger(model) if cfg.liger else "not requested"
    console.print(f"liger-kernel: {liger_status}")

    target_modules = resolve_target_modules(cfg.lora.target_modules)
    if target_modules == "all-linear" and is_multimodal(model):
        console.print("[yellow]multimodal checkpoint: replacing 'all-linear' with the language-model regex "
                      "so LoRA does not adapt the vision tower[/yellow]")
        target_modules = LANGUAGE_MODEL_LINEAR_RE

    if quantization_config is not None:
        prepare_kbit_bf16(model, use_gradient_checkpointing=cfg.gradient_checkpointing)

    peft_config = LoraConfig(
        r=cfg.lora.r,
        lora_alpha=cfg.lora.alpha,
        lora_dropout=cfg.lora.dropout,
        target_modules=target_modules,
        modules_to_save=cfg.lora.modules_to_save or None,
        bias="none",
        task_type="CAUSAL_LM",
    )
    model = get_peft_model(model, peft_config)

    trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
    total = sum(p.numel() for p in model.parameters())
    console.print(f"[bold]trainable {trainable:,} / total {total:,} = {100 * trainable / total:.3f}%[/bold]")
    adapted = sorted({name.rsplit(".lora_A", 1)[0].rsplit(".", 1)[-1]
                      for name, _ in model.named_parameters() if "lora_A" in name})
    console.print(f"adapted module kinds: {adapted}")
    return model, {"trainable_params": trainable, "total_params": total,
                   "trainable_pct": 100 * trainable / total, "adapted_modules": adapted,
                   "liger": liger_status}


def prepare_kbit_bf16(model, *, use_gradient_checkpointing: bool = True):
    """A bf16-preserving replacement for peft's `prepare_model_for_kbit_training`.

    peft's version freezes the base weights, turns on gradient checkpointing *and* upcasts every
    parameter that bitsandbytes did **not** quantise (layer norms, the embedding matrix and the
    output head) from bf16 to fp32. On Qwen3.8-27B that last step is fatal on a 24 GB card: the
    vocabulary is 248,320 tokens wide, so `embed_tokens` alone is 248320 x 5120 x 2 B = 2.4 GB in
    bf16 and 4.7 GB in fp32, and the un-tied `lm_head` is another one. The 4-bit body leaves about
    7 GB free, and the upcast wants ~10 GB of it — it OOMs before the first training step.

    We keep those tensors in bf16 instead. They are frozen anyway (LoRA never updates them), so
    the fp32 copy only ever feeds forward/backward maths that `bnb_4bit_compute_dtype=bfloat16`
    already does in bf16. The only real loss is a slightly less precise final softmax; measured
    training loss on the 4B was indistinguishable.
    """
    for param in model.parameters():
        param.requires_grad = False
    if use_gradient_checkpointing:
        # With every base weight frozen, the checkpointed blocks would have no input that requires
        # grad and autograd would silently skip recomputation — this hook fixes that.
        if hasattr(model, "enable_input_require_grads"):
            model.enable_input_require_grads()
        model.gradient_checkpointing_enable(gradient_checkpointing_kwargs={"use_reentrant": False})
    return model


def _maybe_apply_liger(model) -> str:
    """Optional: swap in Liger-Kernel's fused Triton kernels (notably fused linear+cross-entropy,
    which never materialises the full `[batch, seq, 248320]` logit tensor). Returns a status
    string that goes into metrics.json either way — this is a measurement, not a requirement."""
    try:
        from liger_kernel.transformers import _apply_liger_kernel_to_instance

        _apply_liger_kernel_to_instance(model=model)
        return "applied"
    except Exception as exc:  # pragma: no cover - GPU-only path
        return f"failed: {type(exc).__name__}: {exc}"


# ------------------------------------------------------------------------------ train


def train(cfg: FTConfig) -> dict:
    import torch
    from transformers import AutoTokenizer
    from trl import SFTConfig, SFTTrainer

    torch.manual_seed(cfg.seed)
    run_dir = cfg.run_dir
    run_dir.mkdir(parents=True, exist_ok=True)

    tokenizer = AutoTokenizer.from_pretrained(cfg.base)
    dataset, data_stats = build_dataset(cfg, tokenizer)
    model, param_stats = load_base(cfg)

    cuda = torch.cuda.is_available()
    steps_per_epoch = max(len(dataset) // (cfg.per_device_batch * cfg.grad_accum), 1)
    warmup_steps = max(round(cfg.warmup_ratio * steps_per_epoch * cfg.epochs), 1)

    args = SFTConfig(
        output_dir=str(run_dir / "checkpoints"),
        num_train_epochs=cfg.epochs,
        learning_rate=cfg.lr,
        lr_scheduler_type=cfg.schedule,
        warmup_steps=warmup_steps,
        per_device_train_batch_size=cfg.per_device_batch,
        gradient_accumulation_steps=cfg.grad_accum,
        gradient_checkpointing=cfg.gradient_checkpointing,
        gradient_checkpointing_kwargs={"use_reentrant": False} if cfg.gradient_checkpointing else None,
        bf16=(cuda and cfg.bf16),
        max_length=cfg.max_len,
        packing=False,
        completion_only_loss=True,
        logging_steps=10,
        save_strategy="epoch",
        save_total_limit=1,
        seed=cfg.seed,
        report_to="none",
        # TRL 1.12 defaults to `loss_type="chunked_nll"`: it computes the `lm_head` projection
        # itself, in token chunks, and upcasts the head to fp32 inside every chunk. On a 248,320-
        # token vocabulary that upcast is a ~4.7 GB transient, which is exactly what does not fit
        # next to a 4-bit 27B model. Liger-Kernel's fused linear+cross-entropy does the same job
        # without ever materialising the logits — but TRL only lets the model's own loss run when
        # `loss_type="nll"`. See the chapter's QLoRA memory section.
        # (`use_liger_kernel=True` flips TRL's default `loss_type` to plain `"nll"` and, just as
        # importantly, tells its metrics block not to touch `outputs.logits` — the fused kernel
        # returns `None` there.)
        **({"use_liger_kernel": True} if cfg.liger else {}),
    )

    trainer = SFTTrainer(model=model, args=args, train_dataset=dataset, processing_class=tokenizer)

    if cuda:
        torch.cuda.reset_peak_memory_stats()
    start = time.perf_counter()
    trainer.train()
    wall_seconds = time.perf_counter() - start
    peak_gb = torch.cuda.max_memory_allocated() / 1024**3 if cuda else 0.0

    trainer.model.save_pretrained(str(cfg.adapter_dir))
    tokenizer.save_pretrained(str(cfg.adapter_dir))
    console.print(f"wrote adapter to {cfg.adapter_dir}")

    log_history = trainer.state.log_history
    train_section = {
        **data_stats,
        **param_stats,
        "n_rows": len(dataset),
        "steps_per_epoch": steps_per_epoch,
        "log_history": log_history,
        "final_train_loss": next((r["loss"] for r in reversed(log_history) if "loss" in r), None),
    }
    write_metrics(
        run_dir,
        {
            "run_name": cfg.run_name,
            "model": str(cfg.adapter_dir),
            "base": cfg.base,
            "stage": "lora" if cfg.quant == "none" else "qlora",
            "config": json.loads(cfg.model_dump_json()),
            "train": train_section,
            "cost": {"wall_seconds": wall_seconds, "peak_gb": peak_gb},
        },
    )
    console.print(f"[bold]train done in {wall_seconds / 60:.1f} min, peak {peak_gb:.2f} GB[/bold]")
    _plot_loss(log_history, run_dir, cfg.run_name)
    return train_section


def _plot_loss(log_history: list[dict], run_dir: Path, title: str) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    points = [(r["step"], r["loss"]) for r in log_history if "loss" in r and "step" in r]
    if not points:
        return
    xs, ys = zip(*points)
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.plot(xs, ys, alpha=0.8)
    ax.set_xlabel("optimizer step")
    ax.set_ylabel("cross-entropy loss (completion tokens only)")
    ax.set_title(f"LoRA fine-tuning loss: {title}")
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(run_dir / "loss.png", dpi=120)
    console.print(f"wrote {run_dir / 'loss.png'}")


# ------------------------------------------------------------------------------ merge


def merge(run_name: str, out_dir: str | None = None, device_map: str = "cpu") -> Path | None:
    """`W + B·A` folded back into the base weights, giving an ordinary bf16 checkpoint that needs
    no peft at inference (and can be converted to GGUF for Ollama, chapter 07).

    The base must be reloaded in bf16 to merge — you cannot fold a bf16 adapter into 4-bit NF4
    weights without throwing away most of what was learned. For the 27B that means ~54 GB of
    weights in RAM; on a 62 GB box this is the step most likely to fail, so the failure is caught
    and reported instead of taking the whole run down with it.
    """
    import torch
    from peft import PeftModel
    from transformers import AutoModelForCausalLM, AutoTokenizer

    run_dir = Path("runs") / run_name
    metrics = json.loads((run_dir / "metrics.json").read_text())
    base = metrics["base"]
    adapter = run_dir / "adapter"
    out_path = Path(out_dir) if out_dir else Path("runs/models") / f"{run_name}-merged"

    try:
        model = AutoModelForCausalLM.from_pretrained(base, dtype=torch.bfloat16, device_map=device_map)
        model = PeftModel.from_pretrained(model, str(adapter), device_map=device_map)
        model = model.merge_and_unload()
        out_path.mkdir(parents=True, exist_ok=True)
        model.save_pretrained(str(out_path))
        AutoTokenizer.from_pretrained(str(adapter)).save_pretrained(str(out_path))
    except (RuntimeError, MemoryError, OSError) as exc:
        console.print(f"[red]merge failed ({type(exc).__name__}: {exc}) — keeping the adapter only[/red]")
        write_metrics(run_dir, {"merge": {"ok": False, "error": f"{type(exc).__name__}: {exc}"}})
        return None

    console.print(f"wrote merged bf16 checkpoint to {out_path}")
    write_metrics(run_dir, {"merge": {"ok": True, "path": str(out_path)}})
    return out_path


# ------------------------------------------------------------------------------ evaluate


def evaluate(
    run_name: str,
    domain_splits: tuple[str, ...] = ("2000",),
    general: bool | None = None,
    general_config: str | None = None,
) -> dict:
    """Domain accuracy (CyberMetric) + the chapter-08 general suite, both against `base+adapter`,
    merged into the run's own `metrics.json` so a run is comparable to a chapter-08 baseline."""
    from . import eval_domain, eval_general

    run_dir = Path("runs") / run_name
    metrics = json.loads((run_dir / "metrics.json").read_text())
    cfg = FTConfig.model_validate(metrics["config"])
    adapter = str(run_dir / "adapter")
    general = cfg.eval.general if general is None else general
    general_config = general_config or cfg.eval.general_config

    out: dict = {}
    start = time.perf_counter()
    # Each stage is written to metrics.json as soon as it finishes: the general suite is ~90
    # minutes on a GPU shared with Ollama and *can* be killed by an out-of-memory error halfway
    # through, and losing an already-paid-for domain measurement to that would be silly.
    for split in domain_splits:
        if not split:
            continue
        result = eval_domain.evaluate_hf(cfg.base, split=split, adapter=adapter,
                                         load_in_4bit=cfg.eval.load_in_4bit)
        console.print(f"CyberMetric-{split}: accuracy {result['accuracy']:.3f} ci95 {result['ci95']}")
        key = "domain" if split == domain_splits[0] else f"domain_{split}"
        out[key] = result
        write_metrics(run_dir, {key: result})
    if general:
        # `run_hf` shells out to `lm_eval`, which opens its own CUDA context: whatever this process
        # is still caching (the domain eval's model, or a whole training run when `ablate` calls us
        # in-process) is invisible to it and would simply be missing from its budget.
        free_gpu()
        summary = eval_general.run_hf(cfg.base, str(run_dir / "general"), config_path=general_config, adapter=adapter)
        out["general"] = summary["general"]
        out["general_mean"] = summary["general_mean"]
        write_metrics(run_dir, {"general": summary["general"], "general_mean": summary["general_mean"]})
    out["eval_wall_seconds"] = time.perf_counter() - start
    write_metrics(run_dir, {"eval_wall_seconds": out["eval_wall_seconds"]})
    return out


# ------------------------------------------------------------------------------ ablation


def ablate(config_path: str) -> dict:
    """Run every variant in `configs/ablation_4b.yaml` (train + a short domain eval, and the full
    general suite only for the variants that ask for it) and collect one row per variant."""
    raw = load_yaml(config_path)
    base_cfg = raw["base_config"]
    out_dir = Path(raw.get("out_dir", "runs/ablation_4b"))
    out_dir.mkdir(parents=True, exist_ok=True)
    summary_path = out_dir / "summary.json"
    rows: list[dict] = json.loads(summary_path.read_text())["rows"] if summary_path.exists() else []
    done = {row["name"] for row in rows}

    for variant in raw["variants"]:
        name = variant.pop("name") if "name" in variant else variant["run_name"]
        if name in done:
            console.print(f"[yellow]skip {name} (already in summary.json)[/yellow]")
            continue
        merged = _deep_merge(json.loads(json.dumps(base_cfg)), variant)
        merged["run_name"] = f"{raw.get('run_prefix', 'abl')}_{name}"
        cfg = FTConfig.model_validate(merged)
        console.rule(f"[bold]ablation variant: {name}")
        try:
            train(cfg)
            free_gpu()
            result = evaluate(cfg.run_name, domain_splits=(cfg.eval.domain_split,), general=cfg.eval.general)
        except Exception as exc:  # noqa: BLE001 — one bad variant must not lose the other eight
            console.print(f"[red]variant {name} failed: {type(exc).__name__}: {exc}[/red]")
            free_gpu()
            continue
        metrics = json.loads((cfg.run_dir / "metrics.json").read_text())
        rows.append(
            {
                "name": name,
                "run_name": cfg.run_name,
                "lr": cfg.lr,
                "r": cfg.lora.r,
                "epochs": cfg.epochs,
                "target_modules": cfg.lora.target_modules,
                "trainable_params": metrics["train"]["trainable_params"],
                "final_train_loss": metrics["train"]["final_train_loss"],
                "domain_accuracy": result["domain"]["accuracy"],
                "domain_ci95": result["domain"]["ci95"],
                "general_mean": result.get("general_mean"),
                "general": result.get("general"),
                "train_minutes": metrics["cost"]["wall_seconds"] / 60,
                "peak_gb": metrics["cost"]["peak_gb"],
            }
        )
        summary_path.write_text(json.dumps({"rows": rows}, indent=2))
        console.print(f"wrote {summary_path} ({len(rows)} rows)")

    _plot_ablation(rows, out_dir, raw.get("baseline", {}))
    _print_ablation(rows)
    return {"rows": rows}


def free_gpu() -> None:
    """Drop Python references we no longer hold and hand the CUDA caching allocator's blocks back.

    `ablate` trains and evaluates inside ONE process, and the general suite runs `lm_eval` as a
    *subprocess* — a second CUDA context that cannot see, let alone reuse, the ~12 GB our allocator
    is still caching from training. Without this call the first ablation variant that asks for the
    general suite dies with `CUDA out of memory ... Process <pid> has 16.84 GiB memory in use`,
    where the pid is our own.
    """
    import gc

    import torch

    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.reset_peak_memory_stats()


def _deep_merge(base: dict, override: dict) -> dict:
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(base.get(key), dict):
            base[key] = _deep_merge(base[key], value)
        else:
            base[key] = value
    return base


def _print_ablation(rows: list[dict]) -> None:
    table = Table(title="ablation (Qwen3.5-4B LoRA)")
    for column in ("variant", "lr", "r", "epochs", "targets", "trainable", "domain acc", "general_mean"):
        table.add_column(column)
    for row in rows:
        table.add_row(
            row["name"], f"{row['lr']:.0e}", str(row["r"]), str(row["epochs"]), str(row["target_modules"]),
            f"{row['trainable_params'] / 1e6:.1f}M", f"{row['domain_accuracy']:.3f}",
            f"{row['general_mean']:.3f}" if row.get("general_mean") is not None else "-",
        )
    console.print(table)


def _plot_ablation(rows: list[dict], out_dir: Path, baseline: dict) -> None:
    """Domain accuracy vs general_mean: the whole point of the chapter on one pair of axes.
    Variants without a general suite are drawn on a second panel against domain accuracy only."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, (ax_scatter, ax_bar) = plt.subplots(1, 2, figsize=(13, 5.5))

    scatter_rows = [r for r in rows if r.get("general_mean") is not None]
    for row in scatter_rows:
        ax_scatter.scatter(row["domain_accuracy"], row["general_mean"], s=70, zorder=3)
        ax_scatter.annotate(row["name"], (row["domain_accuracy"], row["general_mean"]),
                            textcoords="offset points", xytext=(6, 4), fontsize=8)
    if baseline.get("domain_accuracy") is not None and baseline.get("general_mean") is not None:
        ax_scatter.scatter(baseline["domain_accuracy"], baseline["general_mean"], s=110, marker="*",
                           color="black", zorder=4, label="base model (chapter 08)")
        ax_scatter.legend(fontsize=8)
    ax_scatter.set_xlabel("CyberMetric accuracy (domain)")
    ax_scatter.set_ylabel("general_mean (chapter-08 suite)")
    ax_scatter.set_title("specialise vs forget")
    ax_scatter.grid(alpha=0.3)

    names = [r["name"] for r in rows]
    ax_bar.barh(range(len(rows)), [r["domain_accuracy"] for r in rows], color="#4c78a8")
    ax_bar.set_yticks(range(len(rows)), names, fontsize=8)
    ax_bar.invert_yaxis()
    if baseline.get("domain_accuracy") is not None:
        ax_bar.axvline(baseline["domain_accuracy"], color="black", ls="--", lw=1, label="base model")
        ax_bar.legend(fontsize=8)
    ax_bar.set_xlabel("CyberMetric accuracy")
    ax_bar.set_title("domain accuracy per variant")
    ax_bar.grid(alpha=0.3, axis="x")

    fig.tight_layout()
    out_path = out_dir / "ablation.png"
    fig.savefig(out_path, dpi=120)
    console.print(f"wrote {out_path}")


# ------------------------------------------------------------------------------ samples

# 3 cybersecurity questions the fine-tune should help with, 3 general ones it must not break.
SAMPLE_PROMPTS = [
    ("cyber_1", "What is the difference between symmetric and asymmetric encryption, and when would you use each?"),
    ("cyber_2", "Explain what a SQL injection attack is and name two concrete defences."),
    ("cyber_3", "What does the principle of least privilege mean in access control?"),
    ("general_poem", "Write a four-line poem about a lighthouse in winter."),
    ("general_code", "Write a Python function that returns the n-th Fibonacci number iteratively."),
    ("general_history", "Why did the Western Roman Empire fall? Answer in three sentences."),
]


def samples(run_name: str, max_new_tokens: int = 220) -> Path:
    """Generate all 6 prompts with the untouched base and with base+adapter, side by side."""
    import torch
    from peft import PeftModel
    from transformers import AutoModelForCausalLM, AutoTokenizer

    from .chat import chat

    run_dir = Path("runs") / run_name
    metrics = json.loads((run_dir / "metrics.json").read_text())
    cfg = FTConfig.model_validate(metrics["config"])
    quant = None
    if cfg.quant == "nf4":
        from transformers import BitsAndBytesConfig

        quant = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4",
                                   bnb_4bit_compute_dtype=torch.bfloat16, bnb_4bit_use_double_quant=True)

    tokenizer = AutoTokenizer.from_pretrained(cfg.base)
    model = AutoModelForCausalLM.from_pretrained(cfg.base, dtype=torch.bfloat16,
                                                 quantization_config=quant, device_map={"": 0}).eval()

    before = {pid: chat(model, tokenizer, [{"role": "user", "content": text}],
                        max_new_tokens=max_new_tokens, temperature=0.0)
              for pid, text in SAMPLE_PROMPTS}

    model = PeftModel.from_pretrained(model, str(run_dir / "adapter")).eval()
    after = {pid: chat(model, tokenizer, [{"role": "user", "content": text}],
                       max_new_tokens=max_new_tokens, temperature=0.0)
             for pid, text in SAMPLE_PROMPTS}

    lines = [f"# Before / after — `{cfg.base}` vs `{run_name}` (LoRA adapter)", "",
             f"Greedy decoding, `max_new_tokens={max_new_tokens}`, `enable_thinking=False`.", ""]
    for pid, text in SAMPLE_PROMPTS:
        lines += [f"## {pid}", "", f"**Prompt:** {text}", "", "**Base:**", "", "```",
                  before[pid].strip(), "```", "", "**Fine-tuned:**", "", "```", after[pid].strip(), "```", ""]
    out_path = run_dir / "samples.md"
    out_path.write_text("\n".join(lines) + "\n")
    console.print(f"wrote {out_path}")
    return out_path


def judge_answers(run_name: str, judge_set: str = "configs/judge_set.yaml", max_new_tokens: int = 256) -> Path:
    """Answer chapter 08's judge questions with base+adapter, writing the `[{id, candidate}]`
    file `judge.py run` scores."""
    import torch
    from peft import PeftModel
    from transformers import AutoModelForCausalLM, AutoTokenizer

    from .chat import chat

    run_dir = Path("runs") / run_name
    cfg = FTConfig.model_validate(json.loads((run_dir / "metrics.json").read_text())["config"])
    with open(judge_set) as f:
        questions = yaml.safe_load(f)["questions"]

    tokenizer = AutoTokenizer.from_pretrained(cfg.base)
    model = AutoModelForCausalLM.from_pretrained(cfg.base, dtype=torch.bfloat16, device_map={"": 0})
    model = PeftModel.from_pretrained(model, str(run_dir / "adapter")).eval()

    answers = [{"id": q["id"],
                "candidate": chat(model, tokenizer, [{"role": "user", "content": q["question"]}],
                                  max_new_tokens=max_new_tokens, temperature=0.0)}
               for q in questions]
    out_path = run_dir / "judge_answers.json"
    out_path.write_text(json.dumps(answers, indent=2))
    console.print(f"wrote {out_path}")
    return out_path


# ------------------------------------------------------------------------------ CLI


@app.command("prepare-data")
def prepare_data_cmd(out_path: str = typer.Option(TRAIN_FILE)) -> None:
    prepare_train_file(out_path)


@app.command("distill")
def distill_cmd(
    base: str = typer.Option("Qwen/Qwen3.5-4B"),
    train_file: str = typer.Option(TRAIN_FILE),
    out_path: str = typer.Option(SELF_DISTILL_FILE),
    max_new_tokens: int = typer.Option(160),
    batch_size: int = typer.Option(32),
    n: int = typer.Option(None, help="only the first N questions (smoke test)"),
) -> None:
    """Chapter 10 — write the self-distilled training file with the base model's own answers."""
    distill(base, train_file, out_path, max_new_tokens, batch_size, n)


@app.command("train")
def train_cmd(config: str = typer.Argument(..., help="e.g. configs/ft_qwen35_4b_lora.yaml")) -> None:
    train(FTConfig.from_yaml(config))


@app.command("evaluate")
def evaluate_cmd(
    run_name: str = typer.Argument(...),
    splits: str = typer.Option("2000", help='comma-separated CyberMetric splits; "" to skip the domain eval'),
    general: bool = typer.Option(None, help="override the config's eval.general"),
    general_config: str = typer.Option(None),
) -> None:
    evaluate(run_name, tuple(splits.split(",")), general=general, general_config=general_config)


@app.command("merge")
def merge_cmd(run_name: str = typer.Argument(...), out_dir: str = typer.Option(None),
              device_map: str = typer.Option("cpu")) -> None:
    merge(run_name, out_dir, device_map)


@app.command("ablate")
def ablate_cmd(config: str = typer.Argument("configs/ablation_4b.yaml")) -> None:
    ablate(config)


@app.command("samples")
def samples_cmd(run_name: str = typer.Argument(...), max_new_tokens: int = typer.Option(220)) -> None:
    samples(run_name, max_new_tokens)


@app.command("judge-answers")
def judge_answers_cmd(run_name: str = typer.Argument(...), judge_set: str = typer.Option("configs/judge_set.yaml")) -> None:
    judge_answers(run_name, judge_set)


@app.command("base-domain")
def base_domain_cmd(
    model: str = typer.Argument("Qwen/Qwen3.5-4B"),
    split: str = typer.Option("500"),
    out_dir: str = typer.Option(None, help="default: runs/eval_baselines/<model basename>"),
    load_in_4bit: bool = typer.Option(False),
) -> None:
    """Domain accuracy for an untouched base model on ONE split, written under its own
    `domain_<split>` key. `eval_domain`'s own CLI always writes the `domain` key, which would
    overwrite the chapter-08 number for a different split; the ablation needs the base measured
    on the same CyberMetric-500 the variants use, so it gets its own key instead."""
    from . import eval_domain

    result = eval_domain.evaluate_hf(model, split=split, load_in_4bit=load_in_4bit)
    console.print(result)
    target = Path(out_dir) if out_dir else Path("runs/eval_baselines") / Path(model).name
    write_metrics(target, {f"domain_{split}": result})


@app.command("plot-ablation")
def plot_ablation_cmd(out_dir: str = typer.Option("runs/ablation_4b"), baseline_json: str = typer.Option(None)) -> None:
    rows = json.loads((Path(out_dir) / "summary.json").read_text())["rows"]
    baseline = json.loads(Path(baseline_json).read_text()) if baseline_json else {}
    _plot_ablation(rows, Path(out_dir), baseline)
    _print_ablation(rows)


if __name__ == "__main__":
    app()
