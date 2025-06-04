import sounddevice as sd
import numpy as np
import webrtcvad
import queue
import threading
import time

# Configuration
RATE = 16000  # 16 kHz
FRAME_DURATION = 30  # ms
FRAME_SIZE = int(RATE * FRAME_DURATION / 1000)  # échantillons par trame
vad = webrtcvad.Vad(2)  # niveau d'agressivité (0 à 3)
q = queue.Queue()

def audio_callback(indata, frames, time_info, status):
    if status:
        print(status)
    audio = indata[:, 0]  # canal mono
    pcm = (audio * 32768).astype(np.int16).tobytes()
    q.put(pcm)

def vad_loop():
    print("En écoute (Ctrl+C pour quitter)...")
    while True:
        try:
            frame = q.get()
            if vad.is_speech(frame, RATE):
                print("Voix détectée")
        except KeyboardInterrupt:
            break

try:
    # Lancement de l'enregistrement audio
    with sd.InputStream(channels=1, samplerate=RATE, blocksize=FRAME_SIZE,
                        dtype='float32', callback=audio_callback):
        vad_loop()

except KeyboardInterrupt:
    print("\nArrêté par l'utilisateur.")
except Exception as e:
    print(f"Erreur : {e}")
