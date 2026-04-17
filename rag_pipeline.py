from vector_store import VectorStore
from config import TOP_K

# Optional: replace with OpenAI later
def simple_llm_response(query, context):
    return f"""
Answer based on context:

Context:
{context}

Question:
{query}

Answer:
"""

class RAGPipeline:
    def __init__(self):
        self.vector_store = VectorStore()

    def build(self, chunks):
        self.vector_store.build_index(chunks)

    def query(self, question):
        docs = self.vector_store.search(question, TOP_K)

        context = "\n\n".join(docs)
        answer = simple_llm_response(question, context)

        return answer, docs