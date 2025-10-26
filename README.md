 # Morse Code GUI — guide d'utilisation

Ce dépôt contient une petite application Python qui convertit du texte en code Morse, permet d'écouter le résultat et d'enregistrer l'audio au format WAV.

Pourquoi WAV ?
- L'export MP3 a été volontairement retiré pour simplifier l'installation (pas de dépendance à ffmpeg). WAV est un format simple, sans compression, facile à générer et à lire.

Contenu du dépôt
- `MORSE.py` — dictionnaire Morse et utilitaires (conversion texte → Morse, fonctions de son basiques).
- `audio_utils.py` — génération du signal audio (numpy), lecture via le système (winsound / ffplay / afplay / aplay) et sauvegarde WAV.
- `gui_morse.py` — interface Tkinter : saisie, conversion, lecture et enregistrement WAV.
- `requirements.txt` — dépendances minimales (numpy).

Prérequis
- Python 3.8 ou supérieur (compatible avec Python 3.13).
- `numpy` (installer via `requirements.txt`).
- Sur Windows, la lecture fonctionne sans installation supplémentaire (utilise `winsound`).
- Sur macOS/Linux, la lecture tente d'utiliser `afplay` (macOS), `aplay` (Linux) ou `ffplay` (si ffmpeg est installé).

Installation
1. Ouvre PowerShell dans le dossier du projet (ex. `C:\Users\Dell\Desktop\DL\MORSE_CODE`).
2. Installe la dépendance :

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Lancer l'interface

```powershell
python gui_morse.py
```

Utilisation (interface)
- Saisis ton texte dans "Texte à convertir" puis clique `Convertir`.
- Clique `Jouer` pour écouter le Morse.
- Clique `Enregistrer WAV` pour sauvegarder le fichier `.wav` (aucun ffmpeg requis).

Générer un WAV depuis la ligne de commande

```powershell
python - <<'PY'
from audio_utils import morse_to_wave_array, save_wave_array_as_wav
from MORSE import text_to_morse

text = 'SOS'
morse = text_to_morse(text)
arr, sr = morse_to_wave_array(morse)
save_wave_array_as_wav('morse_output.wav', arr, sr)
print('morse_output.wav créé')
PY
```

Dépannage rapide
- `Jouer` ne donne rien sous Windows : assure-toi d'exécuter le script avec la même version de Python que celle où tu as installé `numpy`.
- Sur macOS/Linux : installe `ffmpeg` (pour `ffplay`) ou `alsa-utils` (pour `aplay`) si la lecture système n'est pas disponible.
- Pour tout message d'erreur lors de l'enregistrement, copie le message ici et je t'aide à diagnostiquer.

Améliorations possibles
- Réglages (fréquence, durée du point/tiret) dans l'UI.
- Ouvrir automatiquement le dossier contenant le fichier WAV après enregistrement.
- Réintégrer l'export MP3 (avec instructions d'installation de ffmpeg) si tu le souhaites.
