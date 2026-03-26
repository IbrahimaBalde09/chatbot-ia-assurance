_pipeline = None

def get_chatbot_response(message):
    global _pipeline
    if _pipeline is None:
        from rag.rag_pipeline import RAGPipeline
        _pipeline = RAGPipeline()
    return _pipeline.run(message)