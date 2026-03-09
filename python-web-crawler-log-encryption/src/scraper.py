import requests
from bs4 import BeautifulSoup
import time

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def get_title(url):
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        if soup.title:
            title = soup.title.string.strip()
        else:
            title = "No Title"

        time.sleep(2)

        return title

    except Exception as e:
        print("Error saat mengambil title:", e)
        return None