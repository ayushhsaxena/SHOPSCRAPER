import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus

BASE_URL = "https://www.amazon.com"

session = requests.Session()

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/137.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}


def deal_find(search_query):
    url = f"{BASE_URL}/s?k={quote_plus(search_query)}"

    try:
        response = session.get(
            url,
            headers=HEADERS,
            timeout=10
        )
        response.raise_for_status()

    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return []

    soup = BeautifulSoup(response.text, "lxml")

    offers = []
    seen = set()

    for product in soup.select("div[data-component-type='s-search-result']"):

        title = product.select_one("h2 span")
        price = product.select_one("span.a-price span.a-offscreen")
        link = product.select_one("h2 a")

        if not (title and price and link):
            continue

        product_link = BASE_URL + link["href"]

        if product_link in seen:
            continue

        seen.add(product_link)

        offers.append({
            "title": title.get_text(strip=True),
            "price": price.get_text(strip=True),
            "link": product_link
        })

    return offers


if __name__ == "__main__":
    query = input("Search Product: ")

    deals = deal_find(query)

    if not deals:
        print("No products found.")
    else:
        for i, deal in enumerate(deals, 1):
            print(f"\nProduct {i}")
            print("-" * 60)
            print("Title :", deal["title"])
            print("Price :", deal["price"])
            print("Link  :", deal["link"])
