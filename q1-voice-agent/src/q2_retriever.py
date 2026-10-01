from pathlib import Path
import importlib.util

CURRENT_DIR = Path(__file__).resolve().parent
ASSESSMENT_ROOT = CURRENT_DIR.parent.parent
Q2_ROOT = ASSESSMENT_ROOT / "q2-knowledge-base"

Q2_RETRIEVAL_FILE = Q2_ROOT / "src" / "retrieval.py"

if not Q2_RETRIEVAL_FILE.exists():
    raise FileNotFoundError(
        f"Q2 retrieval.py not found at: {Q2_RETRIEVAL_FILE}"
    )

spec = importlib.util.spec_from_file_location(
    "q2_retrieval",
    Q2_RETRIEVAL_FILE
)

q2_retrieval = importlib.util.module_from_spec(spec)
spec.loader.exec_module(q2_retrieval)

KnowledgeBaseRetriever = q2_retrieval.KnowledgeBaseRetriever


class Q2KnowledgeRetriever:
    def __init__(self):
        self.retriever = KnowledgeBaseRetriever()

    def search(self, query, top_k=5):
        if hasattr(self.retriever, "search"):
            return self.retriever.search(query, top_k=top_k)

        if hasattr(self.retriever, "retrieve"):
            return self.retriever.retrieve(query, top_k=top_k)

        raise AttributeError(
            "Q2 KnowledgeBaseRetriever must provide "
            "search() or retrieve()."
        )
