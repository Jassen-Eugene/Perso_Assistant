from datasets import load_dataset
from transformers import pipeline
import torch
from datasets import Dataset
import torchaudio
from record import record_voice

def voice_to_text(output="enregistrement_silence.wav"):
    _ = record_voice(output_filename=output)
    pipe = pipeline("automatic-speech-recognition",
                    model="openai/whisper-base",
                    device=0)
    # Charger et convertir le fichier en float32
    audio, rate = torchaudio.load(output)
    audio = torchaudio.transforms.Resample(rate, 16000)(audio).mean(dim=0).numpy()

    # Coupe l'audio en segments de 30 secondes
    chunk_size = 30 * 16000  # 30 secondes
    chunks = [audio[i:i + chunk_size] for i in range(0, len(audio), chunk_size)]

    transcriptions = []
    for i, chunk in enumerate(chunks):
        print(f"Transcribing chunk {i + 1}/{len(chunks)}")
        out = pipe(chunk,
                generate_kwargs={"language": "french"},
                return_timestamps=True)
        transcriptions.append(out["text"])

    print("\n".join(transcriptions))
    return "\n".join(transcriptions)
