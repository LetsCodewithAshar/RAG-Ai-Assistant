import whisper
import json

model = whisper.load_model("small")

result=model.transcribe("audios/sample.mp3",
                        language="hi",
                        task="translate",
                        word_timestamps=False)
chunks=[]
for segments in result["segments"]:
    chunks.append({"start":segments["start"],"end":segments["end"],"text":segments["text"]})
    print(chunks)
with open("output.json","w") as f:
    json.dump(chunks,f)
print("Model loaded successfully")
