import yt_dlp
import whisper
import os
import json
from datetime import datetime

class IngestionService:
    def __init__(self):
        self.model = whisper.load_model("large-v2")
        self.download_path = "data/videos"
        self.audio_path = "data/audios"
        os.makedirs(self.download_path, exist_ok=True)
        os.makedirs(self.audio_path, exist_ok=True)

    def download_video(self, url: str):
        ydl_opts = {
            "outtmpl": f"{self.download_path}/%(id)s.%(ext)s",
            "format": "bestvideo+bestaudio/best",
            "merge_output_format": "mp4",
            "noplaylist": True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            return filename, info.get("title"), info.get("id")

    def transcribe_video(self, video_path: str, video_id: str):
        # Extract audio first using ffmpeg logic if needed, but whisper can handle video files directly often
        # However, for better performance, extracting audio is good. 
        # For simplicity, let's pass the video file to whisper directly or assume audio extraction.
        # existing code used ffmpeg to extract mp3. Let's do that.
        
        audio_filename = f"{self.audio_path}/{video_id}.mp3"
        if not os.path.exists(audio_filename):
            # Simple ffmpeg command wrapper
            import subprocess
            subprocess.run(["ffmpeg", "-i", video_path, "-q:a", "0", "-map", "a", audio_filename, "-y"])
        
        result = self.model.transcribe(audio_filename, language="hi", task="translate") # Assuming Hindi based on existing code
        
        chunks = []
        for segment in result["segments"]:
            chunks.append({
                "text": segment["text"],
                "start": segment["start"],
                "end": segment["end"],
                "video_id": video_id
            })
            
        return chunks, result["text"]
