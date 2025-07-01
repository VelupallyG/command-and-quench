# watcher.py
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess
import os

# Absolute path to your transcriptions.txt
TRANSCRIPT_PATH = os.path.join(os.getcwd(), "transcriptions", "transcriptions.txt")
TRANSCRIPT_DIR = os.path.dirname(TRANSCRIPT_PATH)

class TranscriptHandler(FileSystemEventHandler):
    def on_modified(self, event):
        # Use absolute path comparison for reliability
        if os.path.abspath(event.src_path) == os.path.abspath(TRANSCRIPT_PATH):
            print(f"Detected change in {event.src_path}, triggering Gemini pipeline...")
            subprocess.run(["python", "main.py"])

if __name__ == "__main__":
    event_handler = TranscriptHandler()
    observer = Observer()

    print(f"👀 Watching for changes in {TRANSCRIPT_PATH}...")
    observer.schedule(event_handler, path=TRANSCRIPT_DIR, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
