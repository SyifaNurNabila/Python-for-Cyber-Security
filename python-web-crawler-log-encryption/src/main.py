from crawler import get_links
from scraper import get_title

start_url = "https://www.upj.ac.id"

links = get_links(start_url)

with open("outputs/results.log", "w", encoding="utf-8") as file:
    for link in links:
        title = get_title(link)

        if title:
            line = title + " | " + link
            print(line)
            file.write(line + "\n")