import asyncio
import json
from pathlib import Path

import neo4j
from neo4j_graphrag.embeddings import OllamaEmbeddings
from neo4j_graphrag.experimental.pipeline.kg_builder import SimpleKGPipeline
from neo4j_graphrag.llm import OllamaLLM

BASE = Path("/Users/sergii/git/ai_knowledge_wiki/knowledge_base/graph_rag")
STATE_FILE = BASE / "sandbox" / "data" / "neo4j_ingested.json"
OLLAMA_HOST = "http://localhost:11435"
NEO4J_URI = "bolt://localhost:7687"
NEO4J_AUTH = ("neo4j", "graphrag123")


def corpus_files() -> list[Path]:
    files = [BASE / "graph_rag.md", BASE / "GraphRAGTop10Materials" / "index.md"]
    for d in sorted(BASE.glob("Arxiv*")):
        for name in ("summary.md", "digest.md", "explainer.md"):
            p = d / name
            if p.exists():
                files.append(p)
    return files


async def main() -> None:
    done: set[str] = set(json.loads(STATE_FILE.read_text())) if STATE_FILE.exists() else set()

    driver = neo4j.GraphDatabase.driver(NEO4J_URI, auth=NEO4J_AUTH)
    llm = OllamaLLM(
        model_name="qwen3.8:27b",
        model_params={"temperature": 0, "options": {"num_ctx": 16384}},
        host=OLLAMA_HOST,
    )
    embedder = OllamaEmbeddings(model="nomic-embed-text", host=OLLAMA_HOST)
    kg = SimpleKGPipeline(
        llm=llm, driver=driver, embedder=embedder, from_pdf=False, on_error="IGNORE"
    )

    files = corpus_files()
    for f in files:
        rel = str(f.relative_to(BASE))
        if rel in done:
            print(f"skip (done): {rel}")
            continue
        print(f"ingesting: {rel}")
        await kg.run_async(text=f.read_text())
        done.add(rel)
        STATE_FILE.write_text(json.dumps(sorted(done)))

    with driver.session() as s:
        nodes = s.run("MATCH (n) RETURN count(n) AS c").single()["c"]
        rels = s.run("MATCH ()-[r]->() RETURN count(r) AS c").single()["c"]
    print(f"NEO4J RESULT: nodes={nodes} relationships={rels}")
    driver.close()


if __name__ == "__main__":
    asyncio.run(main())
