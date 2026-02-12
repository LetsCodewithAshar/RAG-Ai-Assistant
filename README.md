# RAG AI Assistant

A full-stack AI assistant that lets you chat with your videos using RAG (Retrieval-Augmented Generation).

## 🚀 Setup Instructions

### 1. Backend (Python)
The backend handles video downloading, transcription, and the RAG logic.

1.  **Install Dependencies**:
    ```bash
    pip install -r backend/requirements.txt
    ```
    *Note: If you don't have `ffmpeg` installed on your system, you need it for audio processing. Download it from [ffmpeg.org](https://ffmpeg.org).*

2.  **Run Server**:
    ```bash
    cd backend
    python main.py
    ```
    The server runs on `http://localhost:8000`.

### 2. Frontend (Next.js)
The frontend provides a modern UI for uploading and chatting.

**⚠️ Prerequisite**: You must install [Node.js](https://nodejs.org) (LTS version).

1.  **Install Dependencies**:
    ```bash
    cd frontend
    npm install
    ```

2.  **Run Development Server**:
    ```bash
    npm run dev
    ```
    Open `http://localhost:3000` to use the app.

## Features
- **Ingest**: Paste a YouTube URL to download and transcribe it.
- **RAG**: The system chunks the transcript and stores embeddings locally using ChromaDB.
- **Chat**: Ask questions about the video content.

## Architecture
- **Backend**: FastAPI, Whisper (Transcription), ChromaDB (Vector Store), SentenceTransformers (Embeddings).
- **Frontend**: Next.js 14, TailwindCSS, Lucide Icons.
