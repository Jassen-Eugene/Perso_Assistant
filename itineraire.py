import time
from PIL import Image
import cv2
import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

url = "https://fr.mappy.com/itineraire/paris/evry"
image_path = "path_to_itineraire.png"

def download_image(url=url,image_path=image_path):
    # Configuration
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=options)
    
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 30)
    
        # Attendre que le document soit entièrement chargé
        wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
    
        # Cliquer sur "Afficher la suite" si présent
        try:
            afficher_suite = driver.find_element("xpath", "//*[contains(text(), 'Afficher la suite')]")
            afficher_suite.click()
            time.sleep(1)
        except:
            print("Aucun 'Afficher la suite' détecté ou nécessaire.")
    
        # Scroll en bas pour forcer le chargement de tous les contenus
        last_height = driver.execute_script("return document.body.scrollHeight")
        for _ in range(20):  # max 20 scrolls
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(0.3)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
    
        # Redimensionner à la taille complète de la page
        width = driver.execute_script("return document.body.scrollWidth")
        height = driver.execute_script("return document.body.scrollHeight")
        driver.set_window_size(width, height)
        time.sleep(1)  # attendre le rendu
    
        # Capture complète de la page
        driver.save_screenshot(image_path)
    
    except Exception as e:
        print("Erreur :", e)
    
    finally:
        driver.quit()

def crop_head(image_path):
    # Charger l'image complète
    image = Image.open(image_path)
    
    # Modifier ces valeurs selon la zone souhaitée (gauche, haut, droite, bas)
    crop_area = (500, 1250, 1900, 5000)  
    
    # Rogner et sauvegarder
    cropped = image.crop(crop_area)
    cropped.save(image_path)

def crop_tail(image_path):
    image = cv2.imread(image_path)
    h, w = image.shape[:2]
    
    #  Convertir en HSV pour filtrer le vert 
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_green = np.array([35, 40, 40])
    upper_green = np.array([85, 255, 255])
    mask = cv2.inRange(hsv, lower_green, upper_green)
    
    #  Nettoyage du masque 
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    
    #  Détection de contours 
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if contours:
        # Trouver la plus grande ellipse
        largest_contour = max(contours, key=cv2.contourArea)
    
        if len(largest_contour) >= 5:
            ellipse = cv2.fitEllipse(largest_contour)
            (x, y), (MA, ma), angle = ellipse
    
            #  Calcul de la hauteur à rogner 
            # y est le centre de l'ellipse, on calcule le sommet supérieur
            top_of_ellipse = int(y - ma / 2)
    
            # S'assurer que la valeur est dans l'image
            top_of_ellipse = max(0, top_of_ellipse)
    
            #  Rogner avec Pillow 
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(image_rgb)
            cropped = pil_image.crop((0, 0, w, top_of_ellipse))  # (left, upper, right, lower)
    
            #  Sauvegarde 
            cropped.save(image_path)
            cropped.show()
            print(f"Image enregistrée à : {image_path}")
        else:
            print("Contour trop petit pour ellipse.")
    else:
        print("Aucune ellipse verte détectée.")


def get_itinerary(url=url, image_path=image_path):
    download_image(url=url,image_path=image_path)
    crop_head(image_path)
    crop_tail(image_path)

if __name__ == "__main__":
    url = "https://fr.mappy.com/itineraire/transports-en-commun/75000-paris/77000-melun"
    image_path = "path_to_itineraire.png"
    get_itinerary(url=url, image_path=image_path)