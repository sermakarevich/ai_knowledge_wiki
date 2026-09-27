"""Optional Langfuse tracing — env-guarded, no-op unless configured.

`is_live()` / `observe()` wrap `helpdesk.answer` (see `helpdesk.py`): if
`LANGFUSE_HOST` + `LANGFUSE_PUBLIC_KEY` are set in `project/.env`, every
`answer(...)` call becomes an observation on that project; otherwise the
function is returned unchanged and nothing is imported or sent. The guard is
evaluated at import time so there is a single, deterministic live/no-op state
per process.
"""

from __future__ import annotations

import functools
from typing import Callable

from evals_tutorial.config import settings

_LIVE = bool(settings.langfuse_host and settings.langfuse_public_key)


def is_live() -> bool:
    """True once LANGFUSE_HOST + LANGFUSE_PUBLIC_KEY are set in .env."""
    return _LIVE


def observe(fn: Callable) -> Callable:
    """`@observe` when Langfuse is configured, identity wrapper otherwise.

    Eagerly instantiates our client so it becomes the SDK's registered
    singleton: the decorator resolves its client via
    `get_client(public_key=None)` (OS env has no keys — they live in our
    `.env`), and with exactly one registered client that call returns ours.
    """
    if not _LIVE:
        return fn

    client()  # register as the SDK singleton before the decorator runs

    from langfuse import observe as _langfuse_observe

    decorated = _langfuse_observe(name=fn.__name__, as_type="span")(fn)
    functools.update_wrapper(decorated, fn)
    return decorated


_client_instance = None


def client():
    """Configured Langfuse client (only call this when `is_live()`).

    One shared instance per process: passing it into the SDK's
    `set_current_langfuse` also makes `@observe`-decorated functions route
    through the same client (the SDK's auto-client reads OS env, not our
    `.env`, so an explicit key-injected client is the reliable path).
    """
    global _client_instance
    if _client_instance is None:
        from langfuse import Langfuse

        _client_instance = Langfuse(
            public_key=settings.langfuse_public_key,
            secret_key=settings.langfuse_secret_key,
            host=settings.langfuse_host,
            flush_at=50,
        )
    return _client_instance
