import time
import json
import os
from datetime import datetime
import dateparser
import pyttsx3
from plyer import notification

JSON_FILE = "rappels.json"

def refine_date_string(date_str):
    date_str = date_str.lower()
    date_str = date_str.replace("matin", "à 08:00")
    date_str = date_str.replace("soir", "à 19:00")
    date_str = date_str.replace("après-midi", "à 15:00")
    date_str = date_str.replace("après midi", "à 15:00")
    date_str = date_str.replace("dans l'après-midi", "à 15:00")
    date_str = date_str.replace("dans l'après midi", "à 15:00")
    date_str = date_str.replace("midi", "à 12:00")
    return date_str

# Nettoyer et convertir les rappels une seule fois
def preprocess_reminders():
    if not os.path.exists(JSON_FILE):
        with open(JSON_FILE, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=2)
        return []

    with open(JSON_FILE, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    future_reminders = []
    for r in raw_data:
        refined = refine_date_string(r["date"])
        parsed_time = dateparser.parse(refined, settings={"PREFER_DATES_FROM": "future"})
        if parsed_time and parsed_time > datetime.now():
            future_reminders.append({
                "date": parsed_time.strftime("%Y-%m-%d %H:%M"),
                "event": r["event"]
            })

    # Réécrire uniquement les futurs rappels une seule fois
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(future_reminders, f, ensure_ascii=False, indent=2)

    return future_reminders

# Boucle de surveillance
def reminder_loop():
    engine = pyttsx3.init()
    triggered = set()

    reminders = preprocess_reminders()  # Lire et convertir une fois

    while True:
        now = datetime.now()
        for r in reminders:
            due_time = datetime.strptime(r["date"], "%Y-%m-%d %H:%M")
            key = f"{r['event']} {due_time}"

            if now >= due_time and key not in triggered:
                print(f" Rappel : {r['event']} ({due_time})")
                engine.say(f"Rappel : {r['event']}")
                engine.runAndWait()
                notification.notify(
                    title=" Rappel",
                    message=r["event"],
                    timeout=10
                )
                triggered.add(key)

        time.sleep(30)

def add_reminder():
    date_str = input(" Entre la date (ex: demain à midi, dans 2 jours à 14h, etc) : ")
    event = input(" Entre l'événement : ")

    if not os.path.exists(JSON_FILE):
        reminders = []
    else:
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            reminders = json.load(f)

    reminders.append({"date": date_str, "event": event})

    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(reminders, f, ensure_ascii=False, indent=2)

    print(" Rappel ajouté avec succès.")

# Menu principal
if __name__ == "__main__":
    while True:
        print("\n Menu :\n1. Démarrer les rappels\n2. Ajouter un rappel")
        choix = input(" Choix (1 ou 2) : ")

        if choix == "1":
            reminder_loop()
        elif choix == "2":
            add_reminder()
        else:
            print("Choix invalide.")
        time.sleep(10)
