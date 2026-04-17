from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

class VectorStore:
    def __init__(self):
        self.texts = []
        self.index = None

    def build_index(self, chunks):
        embeddings = model.encode(chunks)

        self.texts = chunks
        dim = embeddings.shape[1]

        self.index = faiss.IndexFlatL2(dim)
        self.index.add(np.array(embeddings))

    def search(self, query, top_k=3):
        query_embedding = model.encode([query])
        distances, indices = self.index.search(query_embedding, top_k)

        results = [self.texts[i] for i in indices[0]]
        return results