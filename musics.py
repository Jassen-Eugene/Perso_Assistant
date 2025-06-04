import yt_dlp
import pygame
import moviepy as mp
import os

base_path = "mp3_downloaded"

def clean_repository(base_path):
    music_basepath = os.listdir(base_path)
    for elem in music_basepath:
        os.remove(os.path.join(base_path,elem))

def telecharger_musique(url, dossier_sortie=base_path):
    clean_repository(base_path)
    options = {
        'format': 'bestaudio/best',
        'outtmpl': f'{dossier_sortie}/my_music.mp3',
        'postprocessors': [],
        'quiet': False,
        'noplaylist': True,
    }

    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download([url])

def play_music(title_search):
    print("****"*10)
    url = f"ytsearch:{title_search}"
    telecharger_musique(url)

    music_basepath = os.listdir(base_path)[0]
    music = os.path.join(base_path,music_basepath)

    # Charger un fichier webm en tant qu'audio
    audio_clip = mp.AudioFileClip(music)
    # Enregistrer en .wav 
    audio_clip.write_audiofile(music.split(".")[0]+'.wav')

    os.remove(music)

    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(music.split(".")[0]+".wav")
    pygame.mixer.music.play()

    # Attendre la fin de la musique 
    while pygame.mixer.music.get_busy():
        continue

def play_music_(title_search, stop_event):
    print("****" * 10)
    url = f"ytsearch:{title_search}"
    telecharger_musique(url)

    music_basepath = os.listdir(base_path)[0]
    music = os.path.join(base_path, music_basepath)

    audio_clip = mp.AudioFileClip(music)
    audio_clip.write_audiofile(music.split(".")[0] + '.wav')
    os.remove(music)

    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(music.split(".")[0] + ".wav")
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        if stop_event.is_set():
            print("[play_music] Arrêt demandé.")
            pygame.mixer.music.stop()
            break
    os.remove(music.split(".")[0] + ".wav")
