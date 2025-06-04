import pyaudio
import wave
import numpy as np

def record_voice(output_filename="enregistrement_silence.wav"):
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    CHUNK = 1024
    SILENCE_THRESHOLD = 50
    SILENCE_DURATION = 2  # secondes

    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print(" Enregistrement en cours... Parlez !")

    frames = []
    silent_chunks = 0
    max_silent_chunks = int(SILENCE_DURATION * RATE / CHUNK)

    while True:
        data = stream.read(CHUNK, exception_on_overflow=False)
        frames.append(data)

        # Analyse du volume
        amplitude = np.abs(np.frombuffer(data, dtype=np.int16)).mean()
        silent_chunks = silent_chunks + 1 if amplitude < SILENCE_THRESHOLD else 0

        if silent_chunks > max_silent_chunks:
            #print("Silence détecté. Fin de l'enregistrement.")
            break

    stream.stop_stream()
    stream.close()
    p.terminate()

    with wave.open(output_filename, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

    print(f" Fichier sauvegardé : {output_filename}")
    return b''.join(frames)

