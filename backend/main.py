from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os

app = FastAPI(title="RAG AI Assistant API")

# CORS configuration to allow frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development; restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "RAG AI Assistant Backend is running"}


from services.ingestion_service import IngestionService
from services.rag_service import RAGService
from pydantic import BaseModel

ingestion_service = IngestionService()
rag_service = RAGService()

class VideoRequest(BaseModel):
    url: str

class QueryRequest(BaseModel):
    query: str

@app.post("/ingest")
def ingest_video(request: VideoRequest):
    # 1. Download
    file_path, title, video_id = ingestion_service.download_video(request.url)
    # 2. Transcribe
    chunks, full_text = ingestion_service.transcribe_video(file_path, video_id)
    # 3. Store in RAG
    rag_service.add_chunks(chunks, title)
    return {"status": "success", "video_id": video_id, "chunks_count": len(chunks)}

@app.post("/query")
def query_rag(request: QueryRequest):
    results = rag_service.query(request.query)
    return {"results": results}

@app.on_event("startup")
async def startup_event():
    # Ensure necessary directories exist
    os.makedirs("data/videos", exist_ok=True)
    os.makedirs("data/audios", exist_ok=True)
    os.makedirs("data/db", exist_ok=True)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
