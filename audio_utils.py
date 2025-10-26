import wave
import subprocess
import tempfile
from typing import Tuple

import numpy as np
import platform
import shutil
import os

# We import playback backends lazily when needed to avoid forcing optional
# dependencies at import time.


def _sine_wave(frequency: int, duration_ms: int, sample_rate: int = 44100, amplitude: float = 0.3):
    """Return a numpy int16 array containing a sine wave of given duration."""
    t = np.linspace(0, duration_ms / 1000.0, int(sample_rate * duration_ms / 1000.0), False)
    wave = amplitude * np.sin(2 * np.pi * frequency * t)
    # Convert to 16-bit PCM
    audio = (wave * 32767).astype(np.int16)
    return audio


def morse_to_wave_array(morse_code: str,
                        freq: int = 1000,
                        dot_ms: int = 100,
                        dash_ms: int = 300,
                        intra_symbol_gap_ms: int = 100,
                        inter_char_gap_ms: int = 300,
                        inter_word_gap_ms: int = 700,
                        sample_rate: int = 44100) -> Tuple[np.ndarray, int]:
    """Generate a mono int16 numpy array and sample_rate for the given morse code."""
    parts = []
    silence_intra = np.zeros(int(sample_rate * intra_symbol_gap_ms / 1000.0), dtype=np.int16)
    silence_char = np.zeros(int(sample_rate * inter_char_gap_ms / 1000.0), dtype=np.int16)
    silence_word = np.zeros(int(sample_rate * inter_word_gap_ms / 1000.0), dtype=np.int16)

    for symbol in morse_code:
        if symbol == '.':
            parts.append(_sine_wave(freq, dot_ms, sample_rate))
            parts.append(silence_intra)
        elif symbol == '-':
            parts.append(_sine_wave(freq, dash_ms, sample_rate))
            parts.append(silence_intra)
        elif symbol == ' ':
            parts.append(silence_char)
        elif symbol == '/':
            parts.append(silence_word)
        else:
            parts.append(silence_intra)

    if parts:
        arr = np.concatenate(parts)
    else:
        arr = np.zeros(0, dtype=np.int16)

    return arr, sample_rate


def play_wave_array(arr: np.ndarray, sample_rate: int):
    """Play the given int16 numpy array using available system backends.

    Strategy:
    - Windows: winsound
    - ffplay (ffmpeg) if available
    - macOS: afplay
    - Linux: aplay
    If none available, raises RuntimeError.
    """
    if arr.size == 0:
        return
    # On Windows prefer winsound which is included with Python (no install).
    if platform.system() == 'Windows':
        import winsound
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp:
            tmpname = tmp.name
        try:
            save_wave_array_as_wav(tmpname, arr, sample_rate)
            winsound.PlaySound(tmpname, winsound.SND_FILENAME)
        finally:
            try:
                import os
                os.remove(tmpname)
            except Exception:
                pass
        return

    # Try ffplay (part of ffmpeg) if available
    ffplay_path = shutil.which('ffplay')
    if ffplay_path:
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp:
            tmpname = tmp.name
        try:
            save_wave_array_as_wav(tmpname, arr, sample_rate)
            subprocess.run([ffplay_path, '-nodisp', '-autoexit', '-loglevel', 'error', tmpname], check=False)
        finally:
            try:
                os.remove(tmpname)
            except Exception:
                pass
        return

    # macOS: afplay
    if platform.system() == 'Darwin' and shutil.which('afplay'):
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp:
            tmpname = tmp.name
        try:
            save_wave_array_as_wav(tmpname, arr, sample_rate)
            subprocess.run(['afplay', tmpname], check=False)
        finally:
            try:
                os.remove(tmpname)
            except Exception:
                pass
        return

    # Linux: aplay
    if shutil.which('aplay'):
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp:
            tmpname = tmp.name
        try:
            save_wave_array_as_wav(tmpname, arr, sample_rate)
            subprocess.run(['aplay', tmpname], check=False)
        finally:
            try:
                os.remove(tmpname)
            except Exception:
                pass
        return

    raise RuntimeError('No audio playback backend available. Install ffmpeg (ffplay) or ensure your OS has aplay/afplay; on Windows playback should work via winsound.')


def save_wave_array_as_wav(filename: str, arr: np.ndarray, sample_rate: int):
    """Save numpy int16 array to a WAV file."""
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(arr.tobytes())



def morse_to_play_and_save(morse_code: str, play_sound: bool = True, save_path: str = None, **kwargs):
    """Helper: generate wave array for morse, optionally play and/or save as WAV.

    Returns tuple (arr, sample_rate)
    """
    arr, sr = morse_to_wave_array(morse_code, **kwargs)
    if play_sound:
        play_wave_array(arr, sr)
    if save_path:
        # Always save as WAV to avoid external dependencies
        save_wave_array_as_wav(save_path, arr, sr)
    return arr, sr
