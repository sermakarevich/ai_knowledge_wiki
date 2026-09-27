"""Offline tests for chapter 08 (fw_langchain): the LangChain/LangGraph glue.

No Ollama, no Chroma on disk, no network. We test the *wiring* of the two pieces
that are novel here:

- the LangChain LCEL chain (retrieve → prompt → LLM → parse) built over langchain's
  own `InMemoryVectorStore` + `FakeEmbeddings`/`FakeListChatModel` fakes;
- the LangGraph CRAG loop in `fw_langchain.pipeline_crag`, run with the module's
  model/store singletons monkey-patched to fakes so the real `chroma_store` is
  never opened and `with_structured_output` (which fakes cannot do) is never touched.

The `id → Chunk` mapping helper (`_to_chunk`) is covered directly, since every
retriever pipeline relies on it to turn a LangChain `Document` back into our schema.
"""

from __future__ import annotations

import pytest

pytest.importorskip("langchain_community")
pytest.importorskip("langchain_core")

from langchain_community.embeddings import FakeEmbeddings
from langchain_community.vectorstores import InMemoryVectorStore
from langchain_core.documents import Document as LCDocument
from langchain_core.language_models import BaseChatModel
from langchain_core.language_models.fake_chat_models import FakeListChatModel
from langchain_core.messages import AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.outputs import ChatGeneration, ChatResult
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

import rag_tutorial.fw_langchain as fw
from rag_tutorial.schema import Chunk, chunk_id


class CountingChatModel(BaseChatModel):
    """Canned, sequence-based chat model used to drive the CRAG graph offline.

    Attaches `fw._counter` as a LangChain callback (mirroring production
    `chat_model()` wiring) so `make_answer`'s `n_llm_calls` delta reports the
    real call count — `FakeListChatModel` does not fire callbacks and `fw`
    only counts via callbacks.
    """

    responses: list[str] = []
    _idx: int = 0

    def __init__(self, responses: list[str]):
        super().__init__(responses=list(responses), callbacks=[fw._counter])

    @property
    def _llm_type(self) -> str:  # required by `BaseChatModel` ABC
        return "counting-chat"

    def _generate(self, messages, stop=None, run_manager=None, **kw):
        resp = self.responses[self._idx % len(self.responses)]
        self._idx += 1
        return ChatResult(generations=[ChatGeneration(message=AIMessage(content=resp))])

    async def _agenerate(self, messages, stop=None, run_manager=None, **kw):  # pragma: no cover - not used
        return self._generate(messages, stop, run_manager, **kw)


# -- LCEL chain (pure langchain, no module fakes) ----------------------------------------


def _texts_to_store() -> InMemoryVectorStore:
    emb = FakeEmbeddings(size=8)
    return InMemoryVectorStore.from_texts(
        [
            "ragas is a framework for evaluating retrieval augmented generation",
            "bm25 is a keyword based information retrieval model",
            "mmr re-ranks to prefer diverse passages over near duplicates",
        ],
        embedding=emb,
    )


def test_lcel_chain_retrieve_prompt_llm_parse():
    store = _texts_to_store()
    retriever = store.as_retriever(search_kwargs={"k": 2})
    llm = FakeListChatModel(responses=["ANSWER-OK"])
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "Answer using only the context below.\nContext: {context}"),
            ("human", "{question}"),
        ]
    )
    chain = (
        {
            "question": RunnablePassthrough(),
            "context": retriever | (lambda docs: "\n".join(d.page_content for d in docs)),
        }
        | prompt
        | llm
        | StrOutputParser()
    )
    assert chain.invoke("what is ragas") == "ANSWER-OK"


def test_lcel_chain_empty_context_still_runs():
    retriever = InMemoryVectorStore.from_texts([], embedding=FakeEmbeddings(size=4)).as_retriever(search_kwargs={"k": 3})
    llm = FakeListChatModel(responses=["NO-ANSWER"])
    prompt = ChatPromptTemplate.from_messages([("human", "q:{question} ctx:{context}")])
    chain = (
        {"question": RunnablePassthrough(), "context": retriever | (lambda docs: "\n".join(d.page_content for d in docs))}
        | prompt
        | llm
        | StrOutputParser()
    )
    assert chain.invoke("whatever") == "NO-ANSWER"


# -- LangGraph CRAG with fakes -------------------------------------------------------------


class _FakeStore:
    def query(self, embedding: list[float], k: int = 5, where: dict | None = None) -> list[tuple[Chunk, float]]:
        return [(c, 1.0) for c in self._chunks[:k]]

    def __init__(self, chunks: list[Chunk]):
        self._chunks = chunks


class _FakeEmbedder:
    def embed_query(self, text: str) -> list[float]:
        return [1.0, 0.0, 0.0, 0.0]


def _install_fakes(monkeypatch: pytest.MonkeyPatch, responses: list[str]) -> None:
    """Patch the module's singletons with fakes so `pipeline_crag` runs offline.

    `responses` are the canned text replies the fake LLM emits in order, driving
    the graph: `SUFFICIENT`/`INSUFFICIENT` for grading, `QUERY: ...` for the
    rewrite. `fw._counter` is reset first so `make_answer`'s `n_llm_calls` delta
    reflects only this test's calls."""
    chunks = [
        Chunk(id=chunk_id("p", i, i + 1), paper="p", section="s", text=f"passage {i}", start=i, end=i + 1)
        for i in range(3)
    ]
    fw._counter.count = 0
    shared_llm = CountingChatModel(responses)
    monkeypatch.setattr(fw, "_k_global", 2)
    monkeypatch.setattr(fw, "chat_model", lambda: shared_llm)
    monkeypatch.setattr(fw, "embed_model", lambda: _FakeEmbedder())
    monkeypatch.setattr(fw, "chroma_store", lambda: _FakeStore(chunks))


def test_crag_graph_sufficient_path(monkeypatch: pytest.MonkeyPatch) -> None:
    # canned replies: grade → SUFFICIENT, then the answer → ANSWER-OK
    _install_fakes(monkeypatch, ["SUFFICIENT", "ANSWER-OK"])
    retrieve_fn, answer_fn = fw.pipeline_crag()
    item = {"question": "what is ragas", "evidence": []}

    retrieved = retrieve_fn(item)
    assert [c.text for c in retrieved] == ["passage 0", "passage 1"]  # sliced to k=2
    # exactly one generator call so far (the grade)
    assert fw._counter.count == 1

    # the answer is computed exactly once by `answer_fn`, reported as n_llm_calls
    answer, contexts, n_llm_calls = answer_fn(item, retrieved)
    assert answer == "ANSWER-OK"
    assert len(contexts) == 2
    assert n_llm_calls == 1
    assert fw._counter.count == 2


def test_crag_graph_insufficient_path_rerewrites_once(monkeypatch: pytest.MonkeyPatch) -> None:
    # canned replies: grade → INSUFFICIENT, rewrite → QUERY: ..., then the answer
    _install_fakes(monkeypatch, ["INSUFFICIENT", "QUERY: better search rewrite", "ANSWER-OK"])
    retrieve_fn, answer_fn = fw.pipeline_crag()
    item = {"question": "what is ragas", "evidence": []}

    # runs to a terminal state (grade → rewrite → re-retrieve → grade → END)
    # without raising, still producing the deferred answer
    retrieved = retrieve_fn(item)
    assert retrieved and len(retrieved) <= 2
    # the INSUFFICIENT grade AND the rewrite both fired (the rewrite path is
    # proven by the counter having advanced by exactly two)
    assert fw._counter.count == 2

    answer, contexts, n_llm_calls = answer_fn(item, retrieved)
    assert answer == "ANSWER-OK"
    assert n_llm_calls == 1
    assert fw._counter.count == 3


# -- id → Chunk mapping helper (shared by every retriever pipeline) --------------------------


def _doc(id_: str, paper: str, text: str) -> LCDocument:
    return LCDocument(page_content=text, metadata={"id": id_, "paper": paper, "section": "s", "start": 0, "end": 5})


def test_to_chunk_round_trips_identity_fields():
    doc = _doc("deadbeef00112233", "2401.05856", "some passage text")
    chunk = fw._to_chunk(doc)
    assert isinstance(chunk, Chunk)
    assert chunk.id == "deadbeef00112233"
    assert chunk.paper == "2401.05856"
    assert chunk.text == "some passage text"
    assert chunk.start == 0 and chunk.end == 5


def test_to_chunk_tolerates_missing_section_and_offsets():
    doc = LCDocument(page_content="t", metadata={"id": "abc", "paper": "p"})
    chunk = fw._to_chunk(doc)
    assert chunk.section == ""
    assert chunk.start == 0 and chunk.end == 0


def test_retrievals_dedup_by_chunk_id_via_adapter_docs():
    # Two LangChain docs that map to the SAME chunk id must collapse to one chunk,
    # the exact behaviour the ensemble/parent pipelines implement with a `seen` set.
    by_id: dict[str, Chunk] = {}
    for d in [_doc("id1", "p", "a"), _doc("id1", "p", "a"), _doc("id2", "p", "b")]:
        c = fw._to_chunk(d)
        by_id[c.id] = c
    assert set(by_id) == {"id1", "id2"}
    assert by_id["id2"].text == "b"
