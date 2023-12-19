import whisper
import time
import json

start_time = time.time()

model = "large"

file = "./audio/barkoci.m4a"

transcribed = whisper.transcribe(
    audio=file,
    model=model,
    verbose=True,
    )

end_time = time.time()
total_time = end_time - start_time
print("Total processing time:", total_time, "seconds")

# save json to file
output_file = "./json/" + file.split('.')[0] + ".json"

# Remove tokens before saving
for segment in transcribed["segments"]:
    del segment["tokens"]

with open(output_file, 'w') as f:
    json.dump(transcribed, f, indent=4)