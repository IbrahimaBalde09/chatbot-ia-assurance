from core.retriever import Retriever
from core.generator import ResponseGenerator


class RAGPipeline:
    def __init__(self):
        self.retriever = Retriever()
        self.generator = ResponseGenerator()

    def run(self, query: str) -> dict:
        retrieved_docs = self.retriever.search(query)
        answer = self.generator.generate(query=query, contexts=retrieved_docs)

        return {
            "query": query,
            "answer": answer,
            "sources": retrieved_docs,
        }