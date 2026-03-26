from rag.retriever import Retriever
from rag.generator import ResponseGenerator
from rag.router import DomainRouter
from rag.config import MIN_RELEVANCE_SCORE


class RAGPipeline:
    def __init__(self):
        self.router = DomainRouter()
        self.retriever = Retriever()
        self.generator = ResponseGenerator()

    def run(self, query: str) -> dict:
        domain = self.router.detect_domain(query)
        retrieved_docs = self.retriever.search(query=query, domain=domain)

        if retrieved_docs:
            best_score = retrieved_docs[0]["score"]
        else:
            best_score = 0.0

        if retrieved_docs and best_score >= MIN_RELEVANCE_SCORE:
            answer = self.generator.generate_with_context(
                query=query,
                contexts=retrieved_docs,
                domain=domain
            )
        else:
            answer = self.generator.generate_general(
                query=query,
                domain=domain
            )

        return {
            "query": query,
            "domain": domain,
            "answer": answer,
            "sources": retrieved_docs,
        }