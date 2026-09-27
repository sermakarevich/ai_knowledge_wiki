"""Offline tests for chapter 10 (fw_haystack + fw_dspy). No network.

Haystack: the query pipeline builds and runs end-to-end against an
in-memory store with a fake embedder + fake generator (no Ollama, no
bge download — rerank off in the run test, ranker component covered
separately as a pure mapping check).
DSPy: `RAG` runs under `dspy.utils.DummyLM` (verified name) with a stub
retriever; metric + split helpers covered directly.
"""

from __future__ import annotations

import pytest

haystack = pytest.importorskip("haystack")
dspy = pytest.importorskip("dspy")

from haystack import Document, component
from haystack.dataclasses import ChatMessage

import rag_tutorial.fw_haystack as hs
from rag_tutorial.schema import chunk_id


# ---------------------------------------------------------------------------
# Haystack fakes
# ---------------------------------------------------------------------------


@component
class _FakeTextEmbedder:
    @component.output_types(embedding=list[float])
    def run(self, text: str):
        return {"embedding": [1.0, 0.0]}


@component
class _FakeDocEmbedder:
    @component.output_types(documents=list[Document])
    def run(self, documents: list[Document]):
        from dataclasses import replace

        return {"documents": [replace(d, embedding=[1.0, 0.0]) for d in documents]}


@component
class _FakeGenerator:
    def __init__(self, reply: str = "FAKE-ANSWER"):
        self.reply = reply

    @component.output_types(replies=list[ChatMessage])
    def run(self, messages: list[ChatMessage]):
        return {"replies": [ChatMessage.from_assistant(self.reply)]}


def _tiny_store():
    from dataclasses import replace

    from haystack.document_stores.in_memory import InMemoryDocumentStore

    store = InMemoryDocumentStore()
    docs = [
        Document(content="RAGAS evaluates retrieval augmented generation.", meta={"paper": "p1"}),
        Document(content="BM25 is a keyword retrieval function.", meta={"paper": "p2"}),
    ]
    store.write_documents([replace(d, embedding=[1.0, 0.0]) for d in docs])
    return store


# ---------------------------------------------------------------------------
# Haystack tests
# ---------------------------------------------------------------------------


def test_hs_doc_to_chunk_uses_split_meta() -> None:
    doc = Document(content="hello world", meta={"paper": "p", "split_id": 3, "split_idx_start": 10})
    chunk = hs.hs_doc_to_chunk(doc)
    assert chunk.id == chunk_id("p", 10, 10 + len("hello world"))
    assert chunk.paper == "p"
    assert chunk.meta["split_id"] == 3


def test_indexing_pipeline_runs_with_fake_embedder() -> None:
    from haystack.dataclasses import ByteStream

    from haystack.document_stores.in_memory import InMemoryDocumentStore

    store = InMemoryDocumentStore()
    pipe = hs.build_indexing_pipeline(store, document_embedder=_FakeDocEmbedder())
    pipe.run({
        "converter": {
            "sources": [ByteStream.from_string("# T\n\nhello world this is a test")],
            "meta": [{"paper": "p"}],
        }
    })
    assert store.count_documents() >= 1
    chunk = hs.hs_doc_to_chunk(store.filter_documents()[0])
    assert chunk.paper == "p"


def test_query_pipeline_builds_and_runs_with_fakes() -> None:
    store = _tiny_store()
    pipe = hs.build_query_pipeline(
        use_rerank=False,
        k=2,
        k_each=10,
        text_embedder=_FakeTextEmbedder(),
        generator=_FakeGenerator("ANSWER-OK"),
        store=store,
    )
    out = pipe.run(hs._pipeline_inputs("what evaluates RAG", False))
    answers = out["answer_builder"]["answers"]
    assert len(answers) == 1
    assert answers[0].data == "ANSWER-OK"
    assert answers[0].documents, "expected retrieved documents on the answer"


def test_query_pipeline_dict_has_rrf_joiner() -> None:
    store = _tiny_store()
    pipe = hs.build_query_pipeline(
        use_rerank=False, text_embedder=_FakeTextEmbedder(),
        generator=_FakeGenerator(), store=store,
    )
    d = pipe.to_dict()
    assert d["components"]["joiner"]["init_parameters"]["join_mode"] == "reciprocal_rank_fusion"


def test_pipeline_dumps_loads_round_trip() -> None:
    store = _tiny_store()
    pipe = hs.build_query_pipeline(
        use_rerank=False, text_embedder=_FakeTextEmbedder(),
        generator=_FakeGenerator(), store=store,
    )
    yaml_text = pipe.dumps()
    assert "reciprocal_rank_fusion" in yaml_text
    from haystack import Pipeline

    # unsafe=True: test-local fake components are not on Haystack's
    # deserialization allowlist (same reason production reloads of the
    # custom rerank component need explicit trust — see dump-pipeline).
    reloaded = Pipeline.loads(yaml_text, unsafe=True)
    assert sorted(reloaded.to_dict()["components"]) == sorted(pipe.to_dict()["components"])
    assert "graph TD" in hs.draw_mermaid(pipe)


# ---------------------------------------------------------------------------
# DSPy tests (DummyLM — verified current name in dspy.utils)
# ---------------------------------------------------------------------------

import rag_tutorial.fw_dspy as fw_dspy  # noqa: E402


def test_dspy_module_runs_with_dummy_lm(monkeypatch) -> None:
    from dspy.utils import DummyLM

    monkeypatch.setattr(fw_dspy, "retrieve_texts", lambda q, k=5: ["[p] some context"])
    monkeypatch.setattr(fw_dspy, "retrieve_chunks", lambda q, k=5: [])
    dspy.configure(lm=DummyLM([{"reasoning": "r", "answer": "CANNED"}]))
    prog = fw_dspy.RAG()
    pred = prog(question="what is ragas?")
    assert pred.answer == "CANNED"


def test_dspy_harness_answer_fn_uses_program(monkeypatch) -> None:
    from dspy.utils import DummyLM

    monkeypatch.setattr(fw_dspy, "retrieve_texts", lambda q, k=5: ["[p] ctx"])
    monkeypatch.setattr(
        fw_dspy, "retrieve_chunks",
        lambda q, k=5: [__import__("rag_tutorial.schema", fromlist=["Chunk"]).Chunk(
            id="a" * 16, paper="p", section="s", text="ctx", start=0, end=3, meta={})],
    )
    dspy.configure(lm=DummyLM([{"reasoning": "r", "answer": "HARNESS-OK"}]))
    prog = fw_dspy.RAG()
    retrieve_fn, answer_fn = fw_dspy._harness(prog)
    item = {"question": "q"}
    retrieved = retrieve_fn(item)
    assert len(retrieved) == 1
    answer, contexts, n = answer_fn(item, retrieved)
    assert answer == "HARNESS-OK"
    assert contexts == ["[p] ctx"]
    assert n == 1


def test_token_f1_metric() -> None:
    assert fw_dspy.token_f1("the cat sat", "the cat sat") == pytest.approx(1.0)
    assert fw_dspy.token_f1("completely different words", "nothing shared here") == 0.0
    mid = fw_dspy.token_f1("the cat sat", "the cat stood")
    assert 0.0 < mid < 1.0


def test_dspy_metric_wraps_token_f1() -> None:
    ex = dspy.Example(question="q", answer="the cat sat").with_inputs("question")
    good = dspy.Prediction(answer="the cat sat")
    bad = dspy.Prediction(answer="unrelated words here")
    assert fw_dspy.dspy_metric(ex, good) > fw_dspy.dspy_metric(ex, bad)


def test_load_dspy_split_reads_committed_golden() -> None:
    dev = fw_dspy.load_dspy_split("dev")
    test = fw_dspy.load_dspy_split("test")
    assert len(dev) >= 5 and len(test) >= 20
    assert all("question" in ex.toDict() for ex in dev)


def test_dspy_program_save_load_round_trip(tmp_path, monkeypatch) -> None:
    from dspy.utils import DummyLM

    monkeypatch.setattr(fw_dspy, "retrieve_texts", lambda q, k=5: ["[p] ctx"])
    dspy.configure(lm=DummyLM([{"reasoning": "r", "answer": "X"}]))
    prog = fw_dspy.RAG()
    path = tmp_path / "prog.json"
    prog.save(str(path))
    assert path.exists()
    prog2 = fw_dspy.RAG()
    prog2.load(str(path))
    dspy.configure(lm=DummyLM([{"reasoning": "r", "answer": "Y"}]))
    assert prog2(question="q").answer == "Y"
