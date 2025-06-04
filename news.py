import requests
from bs4 import BeautifulSoup

actualites = "https://fr.news.yahoo.com/"
football = "https://fr.news.yahoo.com/sport/football/"
tennis = "https://fr.news.yahoo.com/sport/tennis/"
formule_1 = "https://fr.news.yahoo.com/sport/f1"
nba = "https://fr.news.yahoo.com/sport/nba"
cyclisme = "https://fr.news.yahoo.com/sport/cyclisme/"
rugby = "https://fr.news.yahoo.com/sport/rugby"

def news_function(url=actualites):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    news = ""
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")
        actualites = []

        # On cherche chaque bloc d'article
        articles = soup.find_all("li", class_="js-stream-content")
        for article in articles:
            titre_tag = article.find("h3", class_="stream-item-title")
            resume_tag = article.find("p", attrs={"data-test-locator": "stream-item-summary"})

            if titre_tag and titre_tag.a:
                titre = titre_tag.a.get_text(strip=True)
                resume = resume_tag.get_text(strip=True) if resume_tag else ""
                actualites.append({
                    "titre": titre,
                    "resume": resume
                })

        # Affichage sans les liens
        for i, act in enumerate(actualites, 1):
            news+=f"{i}. {act['titre']}: \n"
            if act['resume']:
                news+=f"   {act['resume']} \n\n"
        
    except requests.RequestException as e:
        print("Erreur réseau :", e)
        news+="Aucune information n'est trouvée comme actualités."
        
    return news

if __name__ == "__main__":
    news = news_function()
    print(news)
