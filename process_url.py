import sys
import time
import os
import requests
import urllib3
from urllib3.exceptions import InsecureRequestWarning
import whisper
import json
from dotenv import load_dotenv

load_dotenv() 
api_key = os.environ.get("API_KEY")
api_url = os.environ.get("API_URL")

# Disable SSL warnings
urllib3.disable_warnings(InsecureRequestWarning)

def remove_keys_from_segments(segments):
    keys_to_remove = ["tokens", "seek", "temperature", "avg_logprob", "compression_ratio", "no_speech_prob"]
    for segment in segments:
        for key in keys_to_remove:
            segment.pop(key, None)


# 1. downloads file, saves to audio folder
def download_file(url):
    # Split the URL by slashes and use only the parts after the domain
    parts = url.split('/')[3:]
    # Rejoin the remaining parts using underscores
    local_filename = '_'.join(parts)
    local_filepath = os.path.join('./audio', local_filename)

    # Check if the file already exists
    if os.path.exists(local_filepath):
        print(f"The file '{local_filename}' already exists. Skipping download.")
        return local_filename
    
    with requests.get(url, stream=True, verify=False) as r:
        r.raise_for_status()
        with open(local_filepath, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return local_filename

# 2. transcribe
def transcribe(file_name, model):
    text_file_name = file_name.split('.')[0] + '.txt'
    if os.path.exists(os.path.join('./text', model + '_' + text_file_name)):
        print(f"The file '{model}_{file_name}' already exists. Skipping transcription.")
        # read file and return content
        with open(os.path.join('./text', model + '_' + text_file_name), 'r') as f:
            return json.load(f)
    
    transcribed = whisper.transcribe(
        audio=os.path.join('./audio', file_name),
        model=model,
        verbose=True,
        )
    return transcribed

def save_text(transcribed, file_name, model):
    text_file_name = file_name.split('.')[0] + '.txt'
    with open(os.path.join('./text', model + '_' + text_file_name), 'w') as f:
        if isinstance(transcribed, dict):
            remove_keys_from_segments(transcribed["segments"])

            json.dump(transcribed, f, indent=4)
        else:
            f.write(transcribed)
    return text_file_name

    
# 4. upload to server (callback to API)
def upload_text(transcribed, model, process_time, url):
    # Remove tokens before saving
    remove_keys_from_segments(transcribed["segments"])
        
    res = requests.post(api_url, json={
        "text": transcribed['text'],
        "segments": transcribed['segments'],
        "language": transcribed['language'],
        "model": model,
        "process_time": process_time,
        "url": url,
        "api_key": api_key,
    })
    return res
    
def main(url, model="large"):
    start_time = time.time()
    print("Downloading file... " + url)
    file_name = download_file(url)
    transcribed = transcribe(file_name, model)
    save_text(transcribed, file_name, model)

    end_time = time.time()
    process_time = end_time - start_time

    response = upload_text(transcribed, model, process_time, url)
    return True

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "-url":
        url = sys.argv[2]
        main(url)
    else:
        print("Please provide a URL")