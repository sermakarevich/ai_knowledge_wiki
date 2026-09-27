"""Throwaway: prove adapter + each LC retriever path works on the REAL index (no network)."""
from __future__ import annotations

from langchain_core.documents import Document as LCDocument
from langchain_core.language_models.chat_models import BaseLanguageModel
from langchain_core.retrievers import BaseRetriever
from langchain_core.stores import InMemoryStore
from langchain_core.vectorstores import VectorStore

from rag_tutorial.baseline import COLLECTION_NAME
from rag_tutorial.llm import ollama
from rag_tutorial.stores import ChromaStore


class A(VectorStore):
    def __init__(self, store: ChromaStore):
        self._store = store
        self.embedding = ollama

    @classmethod
    def from_texts(cls, *args, **kw) -> "A":
        raise NotImplementedError

    def similarity_search(self, query: str, k: int = 4, **kw) -> list[LCDocument]:  # kw: search kwargs from search_kwargs
        emb = ollama.embed_query(query)
        return [
            LCDocument(
                page_content=c.text,
                metadata={"id": c.id, "paper": c.paper, "section": c.section,
                          "parent_ref": f"{c.paper}::{c.section}", "score": s},
            )
            for c, s in self._store.query(emb, k=k)
        ]


store = ChromaStore(COLLECTION_NAME)
ad = A(store)
print("count:", store.count())

# 1. as_retriever
r = ad.as_retriever(search_kwargs={"k": 4})
print("as_retriever ->", len(r.invoke("how do transformers work?")), "docs")

# 2. Parent — store parent_refs for exactly the chunks the invoke will surface
from langchain_classic.retrievers import ParentDocumentRetriever

PQ = "transformers work"
ds = InMemoryStore()
for d in ad.similarity_search(PQ, k=3):
    pr_id = d.metadata["parent_ref"]
    ds.mset([(pr_id, LCDocument(page_content="PARENT [" + d.metadata["paper"] + "] " + d.page_content, metadata={"id": pr_id, "paper": d.metadata["paper"], "section": d.metadata["section"]})),])
from langchain_text_splitters import RecursiveCharacterTextSplitter
sp = RecursiveCharacterTextSplitter(chunk_size=400)
pr = ParentDocumentRetriever(vectorstore=ad, docstore=ds, id_key="parent_ref", search_kwargs={"k": 3}, child_splitter=sp, parent_splitter=sp)
res = pr.invoke(PQ)
print("parent ->", len(res), "docs; first page starts:", res[0].page_content[:40])

# 3. MultiQuery (constructor + from_llm wiring; no invoke to avoid network)
from langchain_classic.retrievers import MultiQueryRetriever
from langchain_core.language_models.fake_chat_models import FakeListChatModel
fake = FakeListChatModel(responses=["q1\nq2"])
mq = MultiQueryRetriever.from_llm(ad.as_retriever(search_kwargs={"k": 2}), llm=fake)
res = mq.invoke("how do transformers work?")
print("multiquery ->", len(res), "docs")

# 4. Ensemble (dense + bm25)
from langchain_community.retrievers import BM25Retriever
dense = ad.as_retriever(search_kwargs={"k": 4})
texts = [c.text for c, _ in store.query(ollama.embed_query("transformers"), k=30)]
metas = [{"id": f"b{i}"} for i in range(len(texts))]
bm25 = BM25Retriever.from_texts(texts, metadatas=metas, k=4)
from langchain_classic.retrievers import EnsembleRetriever
en = EnsembleRetriever(retrievers=[dense, bm25], weights=(0.7, 0.3), id_key="id")
res = en.invoke("how do transformers work?")
print("ensemble ->", len(res), "docs; sliced to 4:", len(res[:4]))

# 5. Reranker (constructor only — loading bge model)
from langchain_classic.retrievers.document_compressors.cross_encoder_rerank import CrossEncoderReranker
from langchain_community.cross_encoders import HuggingFaceCrossEncoder
hf = HuggingFaceCrossEncoder(model_name="BAAI/bge-reranker-v2-m3")
rec = CrossEncoderReranker(model=hf, top_n=3)
docs = [LCDocument(page_content=t, metadata={"id": f"i{i}"}) for i, t in enumerate(texts[:6])]
rr = rec.compress_documents(docs, "transformers")
print("reranker ->", len(rr), "from 6")

# 6. ContextualCompressionRetriever
from langchain_classic.retrievers.contextual_compression import ContextualCompressionRetriever
ccr = ContextualCompressionRetriever(base_compressor=rec, base_retriever=dense)
res = ccr.invoke("transformers")
print("ctx-comp ->", len(res), "docs")

print("\nALL PROBES OK")
