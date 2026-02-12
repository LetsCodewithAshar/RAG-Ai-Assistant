import chromadb
from sentence_transformers import SentenceTransformer
import uuid

class RAGService:
    def __init__(self):
        self.client = chromadb.PersistentClient(path="data/db")
        self.collection = self.client.get_or_create_collection(name="video_rag")
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')

    def add_chunks(self, chunks, video_title):
        ids = [str(uuid.uuid4()) for _ in chunks]
        documents = [chunk["text"] for chunk in chunks]
        metadatas = [{"start": chunk["start"], "end": chunk["end"], "video_id": chunk["video_id"], "title": video_title} for chunk in chunks]
        embeddings = self.embedder.encode(documents).tolist()

        self.collection.add(
            ids=ids,
            documents=documents,
            metadatas=metadatas,
            embeddings=embeddings
        )

    def query(self, query_text, n_results=5):
        query_embedding = self.embedder.encode([query_text]).tolist()
        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=n_results
        )
        return results
