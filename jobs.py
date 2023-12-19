import os
import requests
from dotenv import load_dotenv

load_dotenv() 
api_key = os.environ.get("API_KEY")
api_url = os.environ.get("API_URL")

def pick_job():
    print(api_key)
    res = requests.get(api_url, headers={
        "x-api-key": api_key,
    })
    return res.json()
