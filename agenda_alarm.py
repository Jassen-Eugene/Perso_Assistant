import json
import datetime
import time
import os
import platform
import numpy as np

# Déclencher une alarme
def alarme(event):
    print(f"\n ALARME : {event['titre']} commence maintenant ({event['date']} {event['heure']}) !")
    
    # Faire du bruit (fonctionne selon le système d'exploitation)
    if platform.system() == "Windows":
        import winsound
        duration = 1000  # ms
        freq = 1000      # Hz
        for _ in range(5):
            winsound.Beep(freq, duration)
    else:
        for _ in range(5):
            os.system('printf "\a"')  # bip ASCII
            time.sleep(1)

#  Charger les événements
def charger_evenements(fichier='agenda.json'):
    try:
        with open(fichier, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Obtenir événements futurs
def get_evenements_a_venir(evenements):
    maintenant = datetime.datetime.now().replace(second=0, microsecond=0)
    evenements_futurs = []

    for e in evenements:
        try:
            event_time = datetime.datetime.strptime(f"{e['date']} {e['heure']}", "%Y-%m-%d %H:%M")
            if event_time >= maintenant:
                evenements_futurs.append((event_time, e))
        except ValueError as err:
            print(f"Erreur dans l'événement '{e.get('titre', 'inconnu')}': {err}")
            continue

    return sorted(evenements_futurs, key=lambda x: x[0])

# Surveiller les événements
def agenda_alarm_function(fichier=r"path_to_agenda.json"):
    sec = str(datetime.datetime.now()).split(':')[-1]
    print(datetime.datetime.now())
    print(sec)
    if sec != "00":
        time.sleep(60-np.float32(sec))
    print(datetime.datetime.now())

    print("Surveillance des événements futurs (à la minute près)...")
    deja_declenches = set()

    while True:
        evenements = get_evenements_a_venir(charger_evenements(fichier))
        maintenant = datetime.datetime.now().replace(second=0, microsecond=0)
        
        for event_time, event in evenements:
            print(maintenant,event_time)
            identifiant = f"{event['date']} {event['heure']} - {event['titre']}"
            if event_time == maintenant and identifiant not in deja_declenches:
                alarme(event)
                deja_declenches.add(identifiant)

        time.sleep(60)  # Vérifie chaque minute

# Lancer
if __name__ == "__main__":
    agenda_alarm_function()
