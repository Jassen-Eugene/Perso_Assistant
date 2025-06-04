from datetime import datetime

def hour_function():
    # Obtenir l'heure actuelle
    heure_actuelle = datetime.now().strftime("%H heure %M")

    # Afficher l'heure
    return f"Il est actuellement {heure_actuelle}."
