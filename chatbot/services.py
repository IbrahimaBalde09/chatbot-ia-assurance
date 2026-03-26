from rag.rag_pipeline import RAGPipeline

pipeline = RAGPipeline()


def get_chatbot_response(question: str) -> dict:
    return pipeline.run(question)