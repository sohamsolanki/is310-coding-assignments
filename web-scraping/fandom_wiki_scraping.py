# Wiki: https://marvels-spider-man.fandom.com/wiki/Marvel%27s_Spider-Man_Wiki:Main_Page
# robots.txt: https://marvels-spider-man.fandom.com/robots.txt

import cloudscraper
from bs4 import BeautifulSoup
import csv
import json
import time

scraper = cloudscraper.create_scraper()

# Source: https://marvels-spider-man.fandom.com/wiki/Category:Characters_in_Marvel%27s_Spider-Man
characters = [
    "Peter_Parker",
    "Miles_Morales",
    "Mary_Jane_Watson",
    "Harry_Osborn",
    "Otto_Octavius",
    "Wilson_Fisk",
    "Yuriko_Watanabe",
    "Felicia_Hardy",
    "Martin_Li",
    "May_Parker",
    "Ben_Parker",
    "Jefferson_Davis",
    "J._Jonah_Jameson",
    "Norman_Osborn",
    "Adrian_Toomes",
    "Aleksei_Sytsevich",
    "Herman_Schultz",
    "Mac_Gargan",
    "Max_Dillon",
    "Lonnie_Lincoln",
]

def get_infobox_value(soup, field_name):
    item = soup.find(attrs={"data-source": field_name})
    if item:
        value = item.find(class_="pi-data-value")
        if value:
            return value.get_text(separator=" ").strip()
    return ""

def get_bio(soup):
    content = soup.find("div", class_="mw-parser-output")
    if content:
        for p in content.find_all("p", recursive=False):
            text = p.get_text().strip()
            if len(text) > 60:
                return text
    return ""

characters_data = []

for slug in characters:
    url = "https://marvels-spider-man.fandom.com/wiki/" + slug
    print("Scraping:", url)

    response = scraper.get(url, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")

    character = {
        "name": slug.replace("_", " "),
        "url": url,
        "alias": get_infobox_value(soup, "alias"),
        "status": get_infobox_value(soup, "status"),
        "gender": get_infobox_value(soup, "gender"),
        "affiliation": get_infobox_value(soup, "affiliation"),
        "first_appearance": get_infobox_value(soup, "first appearance"),
        "voice_actor": get_infobox_value(soup, "voice actor"),
        "bio": get_bio(soup),
    }

    characters_data.append(character)
    print("Done:", character["name"])

    time.sleep(2)

# CSV
with open("/Users/sohamsolanki/Desktop/is310-coding-assignments/web-scraping/spider_man_characters.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=characters_data[0].keys())
    writer.writeheader()
    for character in characters_data:
        writer.writerow(character)

print("Saved CSV!")

# JSON
with open("/Users/sohamsolanki/Desktop/is310-coding-assignments/web-scraping/spider_man_characters.json", "w", encoding="utf-8") as f:
    json.dump(characters_data, f, indent=2)

print("Saved JSON!")
print("Done! Scraped", len(characters_data), "characters.")