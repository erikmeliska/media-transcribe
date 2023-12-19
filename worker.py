from check import can_perform_task
from jobs import pick_job
import process_url
import time
import os
from dotenv import load_dotenv
import sys

load_dotenv() 
api_key = os.environ.get("API_KEY")
api_url = os.environ.get("API_URL")
sleep_time = int(os.environ.get("SLEEP_TIME"))
say = (os.environ.get("SAY") == "True") or False

task_in_progress = False

# Function to check and create directory
def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# Ensure ./audio and ./text directories exist
ensure_directory_exists('./audio')
ensure_directory_exists('./text')

while True:
    if not task_in_progress:
        if can_perform_task():
            print("Conditions met to perform the task")
            
            print("Starting the task")
            if (say): os.system("say 'Spúšťam úlohu'")
            task_in_progress = True
            job = pick_job()
            if not job.get('sourceUrl'):
                print("No job found")
                if (say): os.system("say 'Nie je čo robiť'")
                task_in_progress = False
                sleep_time = sleep_time * 2
                time.sleep(sleep_time)
                # continue
                sys.exit("Exiting: No more tasks to perform.")

            print(job.get('sourceUrl'))
            if process_url.main(job.get('sourceUrl')):
                print("Task completed")
                task_in_progress = False
                if (say): os.system("say 'Úloha bola dokončená'")
            else:
                print("Task failed")
                task_in_progress = False
                if (say): os.system("say 'Úloha zlyhala'")
        else:
            print("Conditions not met to perform the task")
            # os.system("say 'Nemôžem vykonať úlohu'")
    else:
        print("Task in progress...")
        
    time.sleep(sleep_time)
