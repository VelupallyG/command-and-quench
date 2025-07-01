# watcher.py
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess
import os

# Paths
TRANSCRIPT_PATH = os.path.join(os.getcwd(), "transcriptions", "transcriptions.txt")
TRANSCRIPT_DIR = os.path.dirname(TRANSCRIPT_PATH)
FLAG_PATH = os.path.join(os.getcwd(), "dispense_done.flag")

class TranscriptHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if os.path.abspath(event.src_path) == os.path.abspath(TRANSCRIPT_PATH):
            # ✅ Check for dispense_done.flag before triggering
            if os.path.exists(FLAG_PATH):
                print("🚫 Dispense done flag detected. Skipping Gemini pipeline trigger.")
                return

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
            time.sleep(0.2)  # Faster polling for responsiveness
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
