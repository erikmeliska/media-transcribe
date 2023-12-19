import whisper
import time
import logging

# https://audio.samsely.sk/P_Hanes/Duch%20Svaty/01%20Tajomna%20osoba%20Ducha%20Svateho.mp3

start_time = time.time()

model = "tiny"

file = "./audio/19.mp3"

text = whisper.transcribe(
    audio=file,
    model=model,
    )['text']

end_time = time.time()
total_time = end_time - start_time
print("Total processing time:", total_time, "seconds")

# save text to file
with open(file.split('/'), 'w') as f:
    f.write(text)
