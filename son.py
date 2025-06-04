import pyaudio
import wave
import time

def record_from_all_mics(duration=5):
    p = pyaudio.PyAudio()
    
    for i in range(p.get_device_count()):
        info = p.get_device_info_by_index(i)
        if info["maxInputChannels"] > 0:
            print(f"Enregistrement depuis : {info['name']} (index {i})")

            try:
                stream = p.open(format=pyaudio.paInt16,
                                channels=1,
                                rate=16000,
                                input=True,
                                input_device_index=i,
                                frames_per_buffer=1024)
                
                frames = []
                for _ in range(0, int(16000 / 1024 * duration)):
                    data = stream.read(1024)
                    frames.append(data)

                stream.stop_stream()
                stream.close()

                filename = f"mic_{i}_{info['name'].replace(' ', '_').replace('/', '_')}.wav"
                with wave.open(filename, 'wb') as wf:
                    wf.setnchannels(1)
                    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
                    wf.setframerate(16000)
                    wf.writeframes(b''.join(frames))

                print(f" Fichier enregistré : {filename}")

            except Exception as e:
                print(f" Erreur pour {info['name']} (index {i}): {e}")

    p.terminate()

record_from_all_mics()
