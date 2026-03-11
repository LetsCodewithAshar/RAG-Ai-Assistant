# Video Course RAG Assistant

A Retrieval-Augmented Generation (RAG) based AI assistant that allows
users to ask questions about a collection of video lectures. The system
searches lecture transcripts, retrieves relevant sections, and generates
answers pointing to exact timestamps.

------------------------------------------------------------------------

## Overview

This project converts video lectures into a searchable knowledge base
using transcripts and embeddings. Users can ask natural language
questions and get answers grounded in the lecture content.

------------------------------------------------------------------------

## Pipeline

1.  Video → Audio (`video-mp3.py`)
2.  Audio → Transcript JSON (`mp3-json.py`)
3.  Chunk Processing (`merge_chunks.py`)
4.  Embedding Creation (`embeddings_creation.py`)
5.  Query + Retrieval + Answer (`process_incoming.py`)

------------------------------------------------------------------------

## Technologies

Python\
pandas\
numpy\
scikit-learn\
joblib\
requests\
openai-whisper\
yt-dlp\
torch

Models: - bge-m3 (embeddings) - mistral (generation)

------------------------------------------------------------------------

## Run

``` bash
pip install -r requirements.txt
python process_incoming.py
```

Then ask a question in the terminal.

