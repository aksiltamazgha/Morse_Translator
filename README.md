## Morse Translator — Guide (English)

This is a small Python application that converts text to Morse code, plays the resulting audio, and saves the audio as a WAV file.

Principles and choices
- The project generates and saves WAV files (a simple format that avoids external encoding dependencies). MP3 export was intentionally removed to avoid requiring ffmpeg.

Repository contents
- `MORSE.py` — Morse dictionary and utility functions: text → Morse conversion and a simple beep-based playback.
- `audio_utils.py` — audio signal generation using `numpy`, system playback backends (winsound/ffplay/afplay/aplay) and WAV saving.
- `gui_morse.py` — Tkinter GUI: text input, conversion, playback and WAV export.
- `requirements.txt` — minimal dependencies (at least `numpy`).

Prerequisites
- Python 3.8 or newer.
- Install dependencies: `numpy`.
- On Windows the playback uses `winsound` (included with Python). On macOS/Linux the application attempts to use `afplay`/`aplay` or `ffplay` (from ffmpeg) if available.

Installation (PowerShell)

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Run the GUI

```powershell
python gui_morse.py
```

Usage examples

- Convert text and play in the UI: open `gui_morse.py`, enter text, click "Convert" then "Play".
- Save a WAV from the UI: after conversion click "Save WAV" and choose a path.
- Generate a WAV from the command line:

```powershell
python - <<'PY'
from MORSE import text_to_morse
from audio_utils import morse_to_wave_array, save_wave_array_as_wav

text = 'SOS'
morse = text_to_morse(text)
arr, sr = morse_to_wave_array(morse)
save_wave_array_as_wav('morse_output.wav', arr, sr)
print('morse_output.wav created')
PY
```

Quick troubleshooting
- If playback does not work on Windows: make sure you are running the script with the same Python installation where `numpy` is installed.
- On macOS/Linux: install `ffmpeg` (for `ffplay`) or `alsa-utils` (for `aplay`) if system playback is not available.
- If you get an error while saving the WAV file, copy the error message and I will help diagnose it.

Cleanup and best practices
- The `__pycache__` folder contains Python bytecode files and does not need to be tracked in version control. Consider adding it to a `.gitignore` file.
- The code was checked for syntax errors using `py_compile`. To find unused imports or style issues, run a linter such as `flake8`, `pylint` or `ruff`.

Possible next improvements
- Add UI options to adjust frequency and dot/dash duration.
- Add simple unit tests (text→Morse conversion and audio array generation).
- Re-enable MP3 export with instructions for installing `ffmpeg`, if desired.

Contact / Support
If you'd like, I can:
- add a basic `.gitignore`
- add a small test script and CI hooks
- add a command-line interface (CLI) option

Tell me which next step you prefer and I'll implement it.
