import yt_dlp
import os

# ==== CONFIG ====
PLAYLIST_URL = "https://www.youtube.com/playlist?list=PLu0W_9lII9agq5TrH9XLIKQvv0iaF2X3w"
DOWNLOAD_PATH = os.path.join(os.getcwd(), "downloads")
# =================

# Create folder if not exists
os.makedirs(DOWNLOAD_PATH, exist_ok=True)

ydl_opts = {
    "outtmpl": f"{DOWNLOAD_PATH}/%(playlist_index)02d - %(title)s.%(ext)s",
    "format": "bestvideo+bestaudio/best",
    "merge_output_format": "mp4",
    "ignoreerrors": True,
    "playlist_items": "1-20",  # Only the first 20 videos
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([PLAYLIST_URL])

print("✅ First 30 videos downloaded successfully!")
