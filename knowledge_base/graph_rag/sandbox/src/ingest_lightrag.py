import asyncio
from pathlib import Path

from lightrag import LightRAG, QueryParam
from lightrag.llm.ollama import ollama_model_complete, ollama_embed
from lightrag.utils import EmbeddingFunc
from lightrag.kg.shared_storage import initialize_pipeline_status

BASE = Path("/Users/sergii/git/ai_knowledge_wiki/knowledge_base/graph_rag")
WORKDIR = BASE / "sandbox" / "data" / "lightrag"
OLLAMA_HOST = "http://localhost:11435"
LLM_MODEL = "qwen3.8:27b"
EMBED_MODEL = "nomic-embed-text"


def corpus_files() -> list[Path]:
    files = [BASE / "graph_rag.md", BASE / "GraphRAGTop10Materials" / "index.md"]
    for d in sorted(BASE.glob("Arxiv*")):
        for name in ("summary.md", "digest.md", "explainer.md"):
            p = d / name
            if p.exists():
                files.append(p)
    return files


async def main() -> None:
    WORKDIR.mkdir(parents=True, exist_ok=True)
    rag = LightRAG(
        working_dir=str(WORKDIR),
        llm_model_func=ollama_model_complete,
        llm_model_name=LLM_MODEL,
        llm_model_max_async=2,
        llm_model_kwargs={"host": OLLAMA_HOST, "options": {"num_ctx": 16384}},
        embedding_func=EmbeddingFunc(
            embedding_dim=768,
            max_token_size=8192,
            func=lambda texts: ollama_embed.func(
                texts, embed_model=EMBED_MODEL, host=OLLAMA_HOST
            ),
        ),
    )
    await rag.initialize_storages()
    await initialize_pipeline_status()

    files = corpus_files()
    texts = [f.read_text() for f in files]
    paths = [str(f.relative_to(BASE)).replace("/", "_") for f in files]
    print(f"inserting {len(files)} documents ...")
    await rag.ainsert(texts, file_paths=paths)

    answer = await rag.aquery(
        "What is LightRAG and how does it differ from Microsoft GraphRAG?",
        param=QueryParam(mode="hybrid"),
    )
    print("TEST QUERY ANSWER:\n", answer[:600])


if __name__ == "__main__":
    asyncio.run(main())
