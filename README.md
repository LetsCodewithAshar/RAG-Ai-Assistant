# RAG AI Assistant - Video Processing Pipeline

This project provides a pipeline to download YouTube videos, extract audio, and transcribe/chunk the content for use in a Retrieval-Augmented Generation (RAG) AI assistant.

## Workflow

The project consists of several scripts that run in a sequence:

1.  **Download Videos (`downloading videos using python.py`)**:
    -   Downloads videos from a specified YouTube playlist using `yt-dlp`.
    -   Saves videos to a `downloads` folder (though `process_videos.py` expects them in a `videos` folder currently - *Note: You may need to move downloaded files or update the script paths*).

2.  **Extract Audio (`process_videos.py`)**:
    -   Iterates through the `videos/` directory.
    -   Uses `ffmpeg` to extract the audio track from each video.
    -   Saves `.mp3` files to the `audios/` directory with standardized naming.

3.  **Transcribe & Chunk (`create_chunks.py`)**:
    -   Uses OpenAI's `whisper` model (specifically `large-v2`) to transcribe the audio files in `audios/`.
    -   Splits the transcription into segments/chunks.
    -   Saves the chunks along with metadata (start time, end time, text) to JSON files in the `jsons/` directory.

### Utility Scripts

-   **`mp3-text.py`**: A simpler script to transcribe a single file (`audios/sample.mp3`) using the `small` model. Useful for quick testing.
-   **`10sec.py`**: Extracts a 10-second clip from a specific audio file. Useful for testing on smaller files.

## Prerequisites

### 1. Python Libraries

Install the required Python packages:

```bash
pip install yt-dlp openai-whisper
```

*Note: You may also need `setuptools-rust` if you encounter issues installing Whisper.*

### 2. FFmpeg

This project requires **FFmpeg** to be installed and added to your system's PATH.
-   **Windows**: Download from [ffmpeg.org](https://ffmpeg.org/download.html), extract, and add the `bin` folder to your System Environment Variables.
-   **Mac**: `brew install ffmpeg`
-   **Linux**: `sudo apt install ffmpeg`

## Directory Structure

Ensure your project directory looks like this for the scripts to work correctly:

```
project_root/
├── audios/            # Created automatically or manually for MP3s
├── jsons/             # Output folder for transcription JSONs
├── videos/            # Source folder for video files
├── downloads/         # Default download location for yt-dlp script
├── create_chunks.py
├── process_videos.py
└── ...
```

## Usage

1.  Run `downloading videos using python.py` to get content.
2.  Ensure videos are in the `videos` folder.
3.  Run `process_videos.py` to extract audio.
4.  Run `create_chunks.py` to generate the JSON dataset for your RAG.
