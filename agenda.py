import json
import datetime
import json
import time


AGENDA_FILE = "path_to_agenda.json"

# Charger l'agenda depuis un fichier
def charger_agenda():
    try:
        with open(AGENDA_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Sauvegarder l'agenda dans un fichier
def sauvegarder_agenda(agenda):
    with open(AGENDA_FILE, "w") as f:
        json.dump(agenda, f, indent=2)

# Ajouter un événement
def ajouter_evenement(agenda):
    titre = input("Titre de l'événement : ")
    date_str = input("Date (YYYY-MM-DD) : ")
    heure_str = input("Heure (HH:MM) : ")
    
    try:
        datetime.datetime.strptime(f"{date_str} {heure_str}", "%Y-%m-%d %H:%M")
    except ValueError:
        print("Date ou heure invalide.")
        return

    evenement = {
        "titre": titre,
        "date": date_str,
        "heure": heure_str
    }
    agenda.append(evenement)
    print("Événement ajouté.")

def supprimer_evenement(agenda):
    if not agenda:
        print("Aucun événement à supprimer.")
        return

    print("\n📅 Événements existants :")
    for i, e in enumerate(agenda):
        print(f"{i+1}. {e['date']} à {e['heure']} : {e['titre']}")

    try:
        choix = int(input("Numéro de l'événement à supprimer : "))
        if 1 <= choix <= len(agenda):
            evenement_supprime = agenda.pop(choix - 1)
            print(f"Événement supprimé : {evenement_supprime['titre']}")
        else:
            print("Numéro invalide.")
    except ValueError:
        print("Veuillez entrer un nombre.")


# Afficher les événements
def afficher_agenda(agenda):
    if not agenda:
        print("Aucun événement prévu.")
        return

    print("\nÉvénements à venir :")
    agenda_tries = sorted(agenda, key=lambda e: f"{e['date']} {e['heure']}")
    for e in agenda_tries:
        print(f" - {e['date']} à {e['heure']} : {e['titre']}")

# Menu principal
def agenda_function():
    agenda = charger_agenda()
    while True:
        print("\n=== AGENDA ===")
        print("1. Voir les événements")
        print("2. Ajouter un événement")
        print("3. Supprimer un événement")
        print("4. Quitter")

        choix = input("Choix : ")

        if choix == "1":
            afficher_agenda(agenda)
        elif choix == "2":
            ajouter_evenement(agenda)
            sauvegarder_agenda(agenda)
        elif choix == "3":
            supprimer_evenement(agenda)
            sauvegarder_agenda(agenda)
        elif choix == "4":
            sauvegarder_agenda(agenda)
            print("Au revoir !")
            break
        else:
            print("Choix invalide.")

if __name__ == "__main__":
    agenda_function()
