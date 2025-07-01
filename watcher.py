# watcher.py
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess
import os

# Paths
BASE_DIR = os.getcwd()
TRANSCRIPT_PATH = os.path.join(BASE_DIR, "transcriptions", "transcriptions.txt")
TRANSCRIPT_DIR = os.path.dirname(TRANSCRIPT_PATH)
FLAG_PATH = os.path.join(BASE_DIR, "dispense_done.flag")

def get_last_line(file_path):
    """
    Returns the last non-empty line from the specified file.
    """
    with open(file_path, 'r') as file:
        lines = [line.strip() for line in file if line.strip()]
        if lines:
            return lines[-1].lower()
    return ""

class TranscriptHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if os.path.abspath(event.src_path) == os.path.abspath(TRANSCRIPT_PATH):
            # ✅ Check for dispense_done.flag before triggering
            if os.path.exists(FLAG_PATH):
                print("🚫 Dispense done flag detected. Skipping Gemini pipeline trigger.")
                return

            # ✅ Check the last line for drink-related keywords before triggering
            last_line = get_last_line(TRANSCRIPT_PATH)
            keywords = ["drink", "thirsty", "water", "beverage"]

            if any(keyword in last_line for keyword in keywords):
                print(f"✅ Valid request detected in transcription: '{last_line}'")
                print(f"Detected change in {event.src_path}, triggering Gemini pipeline...")
                subprocess.run(["python", "main.py"])
            else:
                print(f"⚠️ Ignored line: '{last_line}' (No drink-related keywords detected)")

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
