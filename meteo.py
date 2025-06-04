import requests
from bs4 import BeautifulSoup
import re

def corriger_texte_meteo(texte):
    # Convertir les points décimaux en virgules
    texte = re.sub(r'(\d+)\.(\d+)', r'\1,\2', texte)

    # Ajouter une espace insécable avant °C et km/h
    texte = re.sub(r'\s?°C', '\u00a0degré Celsius', texte)
    texte = re.sub(r'\s?km/h', '\u00a0kilomètre heure', texte)
    # Nettoyage espace avant la ponctuation
    texte = re.sub(r'\s+([.,!?])', r'\1', texte)
    return texte

def scraper_meteo(url="https://fr.news.yahoo.com/meteo/22664536"):
    resultat = ""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
                }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Température actuelle
        temp_span = soup.find("span", class_="Va(t) D(n) celsius celsius_D(b)")
        temperature = temp_span.get_text(strip=True) if temp_span else "N/A"

        # Texte météo
        details_div = soup.find("div", id="module-weather-details")
        paragraphs = details_div.find_all("p") if details_div else []
        texte_meteo = "\n\n".join(p.get_text(strip=True) for p in paragraphs)

        # Correction automatique
        texte_corrige = corriger_texte_meteo(texte_meteo)

        resultat += f"Température actuelle : {temperature} degré Celsius.\n\n" + "Prévision météo :\n" + texte_corrige

    except requests.RequestException as e:
        print("Erreur réseau :", e)
        resultat += "Aucune information n'est trouvée pour la météo."

    return resultat

if __name__ == "__main__":
    resultat = scraper_meteo()
    print(resultat)