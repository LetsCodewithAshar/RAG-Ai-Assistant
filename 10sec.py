import subprocess

command = [
    "ffmpeg",
    "-ss", "0",
    "-i", "audios/12 _Exercise 1 - Pure HTML Media Player.mp3",
    "-t", "10",
    "-c", "copy",
    "audios/sample.mp3"
]

subprocess.run(command, check=True)
