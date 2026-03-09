import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time

# header supaya terlihat seperti browser
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def get_links(url):
    links = set()

    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        for a in soup.find_all("a", href=True):
            link = urljoin(url, a["href"])

            parsed = urlparse(link)

            # hanya ambil domain upj.ac.id
            if "upj.ac.id" in parsed.netloc:
                links.add(link)

        # delay
        time.sleep(2)

    except Exception as e:
        print("Error saat mengambil link:", e)

    return links