# Whisper krestan.sk transcribing service

This is a Python implementation of the [Whisper](https://openai.com/blog/whisper/) transcribing service. it transcribes audio files from krestan.sk media service.
### Setup

First, install the dependencies.

```
pip install -r requirements.txt
```

Install [`ffmpeg`](https://ffmpeg.org/):

```
# on macOS using Homebrew (https://brew.sh/)
brew install ffmpeg
```

### Run

Start service with:

```
python worker.py
```

Service waits for certain conditions (computer is idle, running on adapter, CPU more than 30% available) and then starts transcribing. Transcribing is done in 3 steps:

1. Get the next job from krestan.sk
2. Download audio file from media source
3. Transcribe audio file
4. Update transcription to krestan.sk media service

When done, if conditions met, repeat until manually stopped or no jobs available.