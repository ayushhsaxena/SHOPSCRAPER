import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus

BASE_URL = "https://www.flipkart.com"

HEADERS = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}

session = requests.Session()


def deal_find(query):

    url = f"https://www.flipkart.com/search?q={quote_plus(query)}"

    try:
        response = session.get(
            url,
            headers=HEADERS,
            timeout=15
        )

        response.raise_for_status()

    except requests.RequestException as e:
        print(e)
        return []

    soup = BeautifulSoup(response.text, "lxml")

    products = []

    cards = soup.select("div[data-id]")

    for card in cards:

        title = card.select_one("div.KzDlHZ")

        if title is None:
            title = card.select_one("a.IRpwTa")

        price = card.select_one("div.Nx9bqj")

        rating = card.select_one("div.XQDdHH")

        image = card.select_one("img")

        link = card.select_one("a.CGtC98, a._1fQZEK")

        if title and price:

            products.append({

                "title": title.get_text(strip=True),

                "price": price.get_text(strip=True),

                "rating": rating.get_text(strip=True) if rating else "N/A",

                "image": image["src"] if image else "",

                "link": BASE_URL + link["href"] if link else "#"

            })

    return products