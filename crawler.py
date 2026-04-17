import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

visited = set()

def crawl_website(url, max_pages=10):
    to_visit = [url]
    all_text = ""

    while to_visit and len(visited) < max_pages:
        current_url = to_visit.pop(0)

        if current_url in visited:
            continue

        try:
            response = requests.get(current_url, timeout=5)
            soup = BeautifulSoup(response.text, "html.parser")

            visited.add(current_url)

            # Extract text
            text = soup.get_text(separator=" ", strip=True)
            all_text += f"\n\nSOURCE: {current_url}\n{text}"

            # Extract links
            for link in soup.find_all("a", href=True):
                full_url = urljoin(current_url, link["href"])

                if urlparse(full_url).netloc == urlparse(url).netloc:
                    to_visit.append(full_url)

        except:
            continue

    return all_text