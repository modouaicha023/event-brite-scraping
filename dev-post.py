from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import csv
import time

# Configuration Selenium en mode headless
options = Options()
options.headless = True
driver = webdriver.Chrome(options=options)

# Charger la page
driver.get("https://devpost.com/hackathons")

# Attendre que la première série d'événements charge
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.CLASS_NAME, "hackathon-tile")))

# Scroller jusqu'à obtenir au moins 100 événements
eventsData = set()
scroll_attempts = 0
MAX_SCROLLS = 50  # Augmenté pour mieux capturer les données
previous_count = 0  # Suivi du nombre d'événements pour vérifier l'apparition de nouveaux

while len(eventsData) < 200 and scroll_attempts < MAX_SCROLLS:
    # Récupérer la liste actuelle des événements
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    events = soup.find_all("div", class_="hackathon-tile")

    for event in events:
        event_name_tag = event.find('h3', class_='mb-4')
        event_date_tag = event.find('div', class_='submission-period')
        event_prize_tag = event.find('span', class_='prize-amount')
        event_location_tag = event.find('div', class_='info')
        event_host_tag = event.find('span', class_='label round host-label')
        event_status_tag = event.find('div', class_='status-label')
        event_themes_tag = event.find('div', class_='themes')
        event_number_participants_tag = event.find('div', class_='participants')

        event_name = event_name_tag.text.strip() if event_name_tag else "Non spécifié"
        event_date = event_date_tag.text.strip() if event_date_tag else "Non spécifié"
        event_prize = event_prize_tag.text.strip() if event_prize_tag else "Non spécifié"
        event_location = event_location_tag.text.strip() if event_location_tag else "Non spécifié"
        event_host = event_host_tag.text.strip() if event_host_tag else "Non spécifié"
        event_status = event_status_tag.text.strip() if event_status_tag else "Non spécifié"
        event_themes = event_themes_tag.text.strip() if event_themes_tag else "Non spécifié"
        event_number_participants = event_number_participants_tag.text.strip() if event_number_participants_tag else "Non spécifié"

        eventsData.add((event_name, event_date, event_prize, event_location, event_host, event_status, event_themes, event_number_participants))

    print(f"Nombre d'événements uniques actuellement récupérés : {len(eventsData)}")

    # Vérifier si de nouveaux événements ont été ajoutés
    if len(eventsData) == previous_count:
        print("Aucun nouvel événement chargé, attente plus longue...")
        time.sleep(5)  # Attendre plus longtemps si aucun nouveau hackathon n'apparaît

    previous_count = len(eventsData)

    # Scroller lentement en petites étapes
    for i in range(3):  # Trois petits scrolls au lieu d'un seul grand
        driver.execute_script("window.scrollBy(0, 500);")  # Scroll de 500px
        time.sleep(2)  # Pause pour permettre le chargement

    scroll_attempts += 1  # Incrémenter le nombre de tentatives de scroll

# Enregistrer les données dans un fichier CSV
with open('hackathons-devpost.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Nom', 'Date', "Prix", "Location", "Organisateur", "Statut", 'Thèmes','Nombres de Participants'])
    writer.writerows(eventsData)

print(f"Nombre final d'événements uniques enregistrés : {len(eventsData)}")

# Fermer le navigateur
driver.quit()
