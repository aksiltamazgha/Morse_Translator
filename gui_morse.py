import tkinter as tk
from tkinter import messagebox, filedialog

from MORSE import text_to_morse
from audio_utils import morse_to_wave_array, play_wave_array, save_wave_array_as_wav


class MorseApp:
    def __init__(self, root):
        self.root = root
        root.title("Morse Code GUI")
        # Input
        tk.Label(root, text="Text to convert:").grid(row=0, column=0, sticky="w")
        self.input_entry = tk.Entry(root, width=60)
        self.input_entry.grid(row=0, column=1, padx=6, pady=6)

        # Convert button
        self.convert_btn = tk.Button(root, text="Convert", command=self.convert)
        self.convert_btn.grid(row=0, column=2, padx=6)

        # Morse output
        tk.Label(root, text="Morse:").grid(row=1, column=0, sticky="nw")
        self.morse_text = tk.Text(root, width=60, height=6)
        self.morse_text.grid(row=1, column=1, columnspan=2, padx=6, pady=6)

        # Control buttons
        self.play_btn = tk.Button(root, text="Play", command=self.play)
        self.play_btn.grid(row=2, column=0, pady=6)

        # WAV export button (no ffmpeg required)
        self.save_wav_btn = tk.Button(root, text="Save WAV", command=self.save_wav)
        self.save_wav_btn.grid(row=2, column=1, pady=6, sticky="w")

        self.quit_btn = tk.Button(root, text="Quit", command=root.quit)
        self.quit_btn.grid(row=2, column=2, pady=6)

        self.current_morse = ""

    def convert(self):
        text = self.input_entry.get().strip()
        if not text:
            messagebox.showinfo("Info", "Please enter text to convert.")
            return
        morse = text_to_morse(text)
        self.current_morse = morse
        self.morse_text.delete(1.0, tk.END)
        self.morse_text.insert(tk.END, morse)

    def play(self):
        if not self.current_morse:
            messagebox.showinfo("Info", "Please convert text to Morse first.")
            return
        try:
            arr, sr = morse_to_wave_array(self.current_morse)
            play_wave_array(arr, sr)
        except Exception as e:
            messagebox.showerror("Error", f"Unable to play audio: {e}")
    

    def save_wav(self):
        if not self.current_morse:
            messagebox.showinfo("Info", "Please convert text to Morse first.")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".wav",
                                                 filetypes=[("WAV files", "*.wav")])
        if not file_path:
            return
        try:
            arr, sr = morse_to_wave_array(self.current_morse)
            save_wave_array_as_wav(file_path, arr, sr)
            messagebox.showinfo("Success", f"WAV file saved:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Unable to save WAV: {e}")


def main():
    root = tk.Tk()
    app = MorseApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()
