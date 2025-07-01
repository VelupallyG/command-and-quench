# Whisper + Gemini Drink Dispenser Pipeline

This project creates a **hands-free, AI-powered drink dispenser** by:

✅ Using **Whisper** (`mic_transcribe.py`) to transcribe **live speech**.  
✅ Writing transcriptions to `transcriptions/transcriptions.txt`.  
✅ Watching for **new lines** with `watcher.py` and triggering `main.py`.  
✅ Using **Gemini** to analyze the transcription for drink requests.  
✅ Automatically calling your **physical drink dispenser** if needed.

---

## Project Structure

```
/DRINK
    /logs
        mic_transcribe.log
        watcher.log
    /transcriptions
        transcriptions.txt
    launch_demo.sh
    main.py
    mic_transcribe.py
    watcher.py
    tool_definitions.py
    README.md
    requirements.txt
    .env
    .gitignore
```

---

## Setup

### Clone the repository:
```bash
git clone <repo_url>
cd DRINK
```

### Install dependencies:
```bash
pip install -r requirements.txt
```
Ensure you also have:
- `whisper`
- `watchdog`
- `google-generativeai`
- `pyserial` (if using physical hardware)

### Configure your environment:
- Create a `.env` file:
    ```
    API_KEY=<Your_Gemini_API_Key>
    ```
- Confirm your hardware serial port in `tool_definitions.py`:
    ```python
    SERIAL_PORT = '/dev/tty.usbmodemXXXX'
    ```

---

## Usage

### 🚦 One-command demo pipeline:
Run:
```bash
./launch_demo.sh
```
This will:
✅ Start **`mic_transcribe.py`** for live speech-to-text.  
✅ Start **`watcher.py`** to auto-trigger **`main.py`** on new lines.  
✅ Automatically process requests and **dispense drinks when requested.**

### Logs:
- `logs/mic_transcribe.log` – Live transcriptions.
- `logs/watcher.log` – Gemini pipeline triggers and decisions.

---

## Individual Scripts

- **`mic_transcribe.py`** – Live mic → Whisper → `transcriptions.txt`.
- **`watcher.py`** – Watches `transcriptions.txt` for updates, triggers `main.py`.
- **`main.py`** – Uses Gemini to analyze if the user requested a drink.
- **`tool_definitions.py`** – Handles actual drink dispensing (via microcontroller/WebSocket).

---

## Features

✅ Fully automated **speech-to-action pipeline**.  
✅ Uses **Google Gemini** to interpret intent.  
✅ Auto-triggers **hardware action** on valid requests.  
✅ Cross-platform with **`watchdog`** for instant updates.  
✅ Clear logs for debugging and demos.

---

## Testing Without Hardware

If you do not have your microcontroller connected:
- Use the WebSocket simulator in `tool_definitions.py`.
- Or replace `dispense_drink` with a simple print statement for simulation.

---

## Future Improvements

✅ Slack/Discord notifications when a drink is dispensed.  
✅ Real-time dashboard for monitoring requests and actions.  
✅ Voice-controlled multi-action pipeline (e.g., lights, music).  
✅ Debounce and advanced transcript filtering for stability.

---

## Contributions
Feel free to fork, improve, and contribute to this hands-free AI automation pipeline.

---

## License
MIT License

---

**Enjoy your fully automated Whisper + Gemini voice-triggered drink dispenser pipeline!** 
