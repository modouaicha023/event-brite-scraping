from bs4 import BeautifulSoup
import requests
import csv

eventsData = set()
count = 0
page = 1

while len(eventsData) < 30:
    html_text = requests.get(f"https://www.eventbrite.com/d/online/hackathon/?page={page}").text
    soup = BeautifulSoup(html_text, 'lxml')
    events = soup.find_all("section", class_="event-card-details")
    print(f"https://www.eventbrite.com/d//hackathon/?page={page}")
    print(f"Page : {page}")
    count += 1
    print(f"Nombre d'événements récupérés : {len(events)}")

    for event in events:
        event_name_tag = event.find('h3', class_='Typography_root__487rx')
        event_date_tag = event.find('p', class_='Typography_root__487rx')
        if event_name_tag and event_date_tag:
            event_name = event_name_tag.text.strip()
            event_date = event_date_tag.text.strip()
            eventsData.add((event_name, event_date))
    page += 1
eventsData = sorted(eventsData)

with open('event-brite.csv', 'w', newline='', encoding='utf-8', errors='ignore') as file:
    writer = csv.writer(file)
    writer.writerow(['Name', 'Date'])
    writer.writerows(eventsData)

print(f"Nombre final d'événements uniques enregistrés : {len(eventsData)}")
print(count)
