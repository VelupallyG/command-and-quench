import whisper
import pyaudio
import wave
import datetime
import os
import time

# Config
MODEL_SIZE = "base"
OUTPUT_DIR = "transcriptions"
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 3

os.makedirs(OUTPUT_DIR, exist_ok=True)
model = whisper.load_model(MODEL_SIZE)
p = pyaudio.PyAudio()

print("[INFO] Starting mic transcription. Press CTRL+C to stop.")

try:
    while True:
        # ✅ Check if dispense_done.flag exists, terminate if so
        if os.path.exists("dispense_done.flag"):
            print("[INFO] Dispense completed. Stopping transcription.")
            break

        print("[INFO] Opening stream...")
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

        print(f"[INFO] Recording for {RECORD_SECONDS} seconds...")
        frames = []
        for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK, exception_on_overflow=False)
            frames.append(data)

        stream.stop_stream()
        stream.close()

        filename = "temp.wav"
        wf = wave.open(filename, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()

        print("[INFO] Transcribing...")
        try:
            result = model.transcribe(filename)
            text = result["text"].strip()
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{timestamp}] {text}")

            with open(os.path.join(OUTPUT_DIR, "transcriptions.txt"), "a") as f:
                f.write(f"[{timestamp}] {text}\n")

        except Exception as e:
            print(f"[ERROR] Transcription failed: {e}")

        time.sleep(1)  # Shorter pause for responsiveness

except KeyboardInterrupt:
    print("\n[INFO] Stopped by user.")

p.terminate()
if os.path.exists("temp.wav"):
    os.remove("temp.wav")
