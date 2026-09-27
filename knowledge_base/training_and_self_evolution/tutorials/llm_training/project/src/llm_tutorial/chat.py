"""Chapter 05 — the chat template: turning a list of `{"role", "content"}` messages into the
single string a causal-LM actually trains and generates on, and marking which tokens of that
string are the assistant's (so training can mask the rest out of the loss).

`CHAT_TEMPLATE` is a ChatML-style template (the format Qwen, and most open chat models, use):
each turn is wrapped in `<|im_start|><role>\\n...<|im_end|>\\n`. The two tokens `<|im_start|>`
and `<|im_end|>` already exist in our tokenizer (chapter 02, `SPECIAL_TOKENS`); this module only
teaches the tokenizer how to *arrange* them. The `{% generation %}...{% endgeneration %}` Jinja
tags around the assistant's turn are not decoration — `apply_chat_template(...,
return_assistant_tokens_mask=True)` (and, on top of that, TRL's `assistant_only_loss=True`) both
require these tags to know which tokens are "assistant" tokens; without them either call raises.
"""

import torch
import typer
from rich.console import Console
from transformers import PreTrainedModel, PreTrainedTokenizerBase

app = typer.Typer(add_completion=False, help=__doc__)
console = Console()

DEFAULT_SYSTEM = "You are a helpful assistant."

# Jinja whitespace control (`{%-`/`-%}`) strips the newlines *around* the tags that the template
# source needs for readability, so the rendered string has exactly the tokens shown in the chapter
# and nothing else.
CHAT_TEMPLATE = (
    "{%- set default_system = default_system if default_system is defined"
    " else 'You are a helpful assistant.' -%}\n"
    "{%- if messages[0]['role'] != 'system' -%}\n"
    "{{ '<|im_start|>system\\n' + default_system + '<|im_end|>\\n' }}\n"
    "{%- endif -%}\n"
    "{%- for message in messages -%}\n"
    "{%- if message['role'] == 'assistant' -%}\n"
    "{{ '<|im_start|>assistant\\n' }}"
    "{% generation %}{{ message['content'] + '<|im_end|>\\n' }}{% endgeneration %}\n"
    "{%- else -%}\n"
    "{{ '<|im_start|>' + message['role'] + '\\n' + message['content'] + '<|im_end|>\\n' }}\n"
    "{%- endif -%}\n"
    "{%- endfor -%}\n"
    "{%- if add_generation_prompt -%}\n"
    "{{ '<|im_start|>assistant\\n' }}\n"
    "{%- endif -%}"
)


def attach_chat_template(tokenizer: PreTrainedTokenizerBase) -> PreTrainedTokenizerBase:
    """Set `tokenizer.chat_template` to `CHAT_TEMPLATE` and make the tokenizer a chat tokenizer.

    `<|im_start|>`/`<|im_end|>` were already added as special tokens when the tokenizer was
    trained (chapter 02) — this only asserts that and fails loudly if an older tokenizer is
    passed in by mistake. The one real change is `eos_token`: during pre-training, EOS is
    `<|endoftext|>` (the boundary between unrelated documents); during and after SFT, EOS is
    `<|im_end|>` (the boundary between conversation turns) so `generate()` stops at the end of
    the assistant's turn instead of running on into a hallucinated next turn. The training loss
    keeps teaching the model to emit `<|im_end|>`, because it is inside the `{% generation %}`
    span, so this is not just relabeling — the model is actually trained to produce this token.
    """
    special = set(tokenizer.all_special_tokens or [])
    missing = {"<|im_start|>", "<|im_end|>"} - special
    if missing:
        raise ValueError(
            f"tokenizer is missing {sorted(missing)} as special tokens; "
            "train it with chapter 02's tokenizer.py (SPECIAL_TOKENS already includes them)"
        )
    tokenizer.chat_template = CHAT_TEMPLATE
    tokenizer.eos_token = "<|im_end|>"
    return tokenizer


def render(
    messages: list[dict[str, str]],
    tokenizer: PreTrainedTokenizerBase,
    add_generation_prompt: bool = True,
    default_system: str = DEFAULT_SYSTEM,
    enable_thinking: bool = False,
) -> str:
    """Messages -> the exact string the model sees, using `tokenizer.chat_template`.

    `enable_thinking=False` is forwarded to the Jinja template context; our own ChatML template
    ignores it, but Qwen's official chat templates (e.g. Qwen3.5-4B) branch on it and, left at
    their own default (True), emit a `<think>...</think>` block before the actual answer — fatal
    for short-`max_new_tokens` generation (e.g. the CyberMetric letter-only prompt), since the
    budget is spent on reasoning tokens and the answer never appears.
    """
    return tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=add_generation_prompt,
        default_system=default_system,
        enable_thinking=enable_thinking,
    )


def chat(
    model: PreTrainedModel,
    tokenizer: PreTrainedTokenizerBase,
    messages: list[dict[str, str]],
    max_new_tokens: int = 128,
    temperature: float = 0.7,
    enable_thinking: bool = False,
) -> str:
    """Render `messages`, generate a continuation, and return only the new assistant turn
    (stopping at `<|im_end|>`, decoded without special tokens)."""
    prompt = render(messages, tokenizer, add_generation_prompt=True, enable_thinking=enable_thinking)
    device = next(model.parameters()).device
    inputs = tokenizer(prompt, return_tensors="pt", add_special_tokens=False).to(device)
    im_end_id = tokenizer.convert_tokens_to_ids("<|im_end|>")
    with torch.no_grad():
        generated = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=temperature > 0,
            temperature=temperature if temperature > 0 else None,
            top_p=0.95 if temperature > 0 else None,
            eos_token_id=im_end_id,
            pad_token_id=tokenizer.pad_token_id or im_end_id,
        )
    new_tokens = generated[0, inputs["input_ids"].shape[1] :]
    return tokenizer.decode(new_tokens, skip_special_tokens=True)


@app.command()
def show(
    tokenizer_dir: str = typer.Argument(..., help="tokenizer dir or HF repo id"),
    user: str = typer.Option("What is the capital of France?", help="user turn to render"),
) -> None:
    """Print the rendered ChatML string for one user turn (debugging aid)."""
    from transformers import AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(tokenizer_dir)
    if tokenizer.chat_template is None:
        attach_chat_template(tokenizer)
    rendered = render([{"role": "user", "content": user}], tokenizer)
    console.print(rendered)


@app.command()
def generate(
    model_dir: str = typer.Argument(..., help="a saved model dir, e.g. runs/models/tiny-qwen35-110m-sft"),
    prompt: str = typer.Option(..., "--prompt", help="the user's message"),
    max_new_tokens: int = typer.Option(128),
    temperature: float = typer.Option(0.7),
) -> None:
    """Load a saved model + tokenizer and print its reply to one user prompt."""
    from transformers import AutoModelForCausalLM, AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(model_dir)
    if tokenizer.chat_template is None:
        attach_chat_template(tokenizer)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = AutoModelForCausalLM.from_pretrained(model_dir).to(device)
    reply = chat(
        model, tokenizer, [{"role": "user", "content": prompt}],
        max_new_tokens=max_new_tokens, temperature=temperature,
    )
    console.print(reply)


if __name__ == "__main__":
    app()
