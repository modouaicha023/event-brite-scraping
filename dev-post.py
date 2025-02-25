from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import csv
import time

options = Options()
options.headless = True

# Assurez-vous d'avoir le driver Chrome installé et accessible dans votre PATH
driver = webdriver.Chrome(options=options)

# Charger la page
driver.get("https://devpost.com/hackathons")

# Attendre quelques secondes pour laisser le temps au JS de charger le contenu (ajustez ce délai si besoin)
time.sleep(5)

# Récupérer le code source après exécution du JS
html = driver.page_source
soup = BeautifulSoup(html, 'lxml')

# Rechercher les div avec la classe "hackathon-tile"
events = soup.find_all("div", class_="hackathon-tile")
print(f"Nombre d'événements récupérés : {len(events)}")

# Extraire les données souhaitées
eventsData = set()
while len(events) < 100:
    for event in events:
        event_name_tag = event.find('h3', class_='mb-4')
        event_date_tag = event.find('div', class_='submission-period')
        event_prize_tag = event.find('span', class_='prize-amount')
        event_location_tag = event.find('div', class_='info')
        event_host_tag = event.find('span', class_='label round host-label')
        event_status_tag = event.find('div', class_='status-label')
        if event_name_tag and event_date_tag:
            event_name = event_name_tag.text.strip()
            event_date = event_date_tag.text.strip()
            event_prize = event_prize_tag.text.strip()
            event_locaton = event_location_tag.text.strip()
            event_host = event_host_tag.text.strip()
            event_status = event_status_tag.text.strip()
            eventsData.add((event_name, event_date,event_prize,event_locaton, event_host, event_status))

# Enregistrer les données dans un fichier CSV
with open('hackathons-devpost.csv', 'w', newline='', encoding='utf-8', errors='ignore') as file:
    writer = csv.writer(file)
    writer.writerow(['Nom', 'Date', "Prix", "Location", "Organisateur", "Statut"])
    writer.writerows(eventsData)

print(f"Nombre final d'événements uniques enregistrés : {len(eventsData)}")

# Fermer le navigateur
driver.quit()
