from TTS.api import TTS
import sounddevice as sd
import soundfile as sf
import numpy as np

# Charger le modèle
tts = TTS(model_name="tts_models/multilingual/multi-dataset/your_tts", progress_bar=False, gpu=False)

# Synthèse vocale avec clonage
def answer(texte):
    # Clonage vocal 
    audio = tts.tts_to_file(
        text=texte,
        speaker_wav="jassen.wav", #Ce fichier jassen.wav peut etre remplacé, si on veut changer de voix
        language="fr-fr",
        file_path="output.wav"
    )
    #audio_array = np.frombuffer(audio, dtype=np.int16)
    data, sample_rate = sf.read("output.wav")
    sd.play(data, sample_rate)
    sd.wait()
    