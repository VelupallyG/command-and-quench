# Command & Quench

#### Whisper + Gemini Voice-Activated Drink Dispenser

This project enables a hands-free, voice-activated drink dispensing pipeline using:

- Whisper for live speech-to-text transcription.
- Gemini for intelligent intent detection.
- Arduino/WebSocket for hardware dispensing control.
- Watcher and auto-termination pipeline to prevent repeated triggers.

##

## Video Demo:

---

## Project Structure

```
/drink
    mic_transcribe.py          # Records audio, transcribes, appends to transcriptions.txt
    watcher.py                 # Watches transcriptions.txt for valid requests, triggers main.py
    main.py                    # Calls Gemini for intent analysis, triggers drink dispensing
    tool_definitions.py        # Handles hardware (Arduino/WebSocket) control for dispensing
    server.py                  # (Optional) WebSocket test server
    uno.ino                    # Arduino sketch for hardware dispensing
    requirements.txt           # Python dependencies
    .env                       # API keys and environment variables
    /transcriptions
        transcriptions.txt     # Stores transcription logs
    /logs
        mic_transcribe.log
        watcher.log
```

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone <repo_url>
cd drink
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file:

```
API_KEY=<YOUR_GEMINI_API_KEY>
```

### 4. Set up your Arduino (optional)

- Flash `uno.ino` to your Arduino if using direct serial dispensing.
- Confirm the correct `SERIAL_PORT` in `tool_definitions.py`.

---

## Usage

### One-command pipeline

Run each in separate terminals:

```bash
python mic_transcribe.py
```

```bash
python watcher.py
```

The pipeline will:

- Transcribe live audio to `transcriptions/transcriptions.txt`.
- `watcher.py` will detect drink-related requests and trigger `main.py`.
- `main.py` will call Gemini to verify intent and execute `dispense_drink` if appropriate.
- After a successful dispense, a `dispense_done.flag` will prevent further triggers until manually reset.

---

## Features

- Voice-triggered dispensing using Whisper and Gemini.
- Prevents repeated triggers after a successful dispense.
- Handles hardware dispensing via Arduino or WebSocket.
- Auto-terminates transcription on dispense completion.
- Pre-filtering keywords and context-based Gemini verification.

---

## Future Improvements

- Define more tools
- Transition from PySerial to WebSocket

---

## Contributions

Feel free to fork, improve, and contribute to this open-source, voice-activated drink dispenser pipeline.

---

## License

MIT License
