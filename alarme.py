import time
import datetime
import os
import platform

def alarm_function(heure_alarme="12:00"):
    # Définir l'heure de l'alarme (format 24h : HH:MM)

    def sonner_alarme():
        print("ALARME ! Il est l'heure ! ")
        
        # Faire du bruit (fonctionne selon le système d'exploitation)
        if platform.system() == "Windows":
            import winsound
            duration = 1000  # en millisecondes
            freq = 1000      # en hertz
            for _ in range(5):
                winsound.Beep(freq, duration)
        else:
            # Sur Mac/Linux 
            for _ in range(5):
                os.system('printf "\a"')  # bip ASCII
                time.sleep(1)

    # Boucle d'attente
    print(f"Attente de l'heure d'alarme ({heure_alarme})...")
    while True:
        heure_actuelle = datetime.datetime.now().strftime("%H:%M")
        if heure_actuelle == heure_alarme:
            sonner_alarme()
            break
        time.sleep(20)  # Vérifie toutes les 20 secondes
