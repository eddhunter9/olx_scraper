import requests
from bs4 import BeautifulSoup
import time

headers = {
    "User-Agent": "Mozilla/5.0"
}

def get_offer_count_from_store(store_url):
    try:
        response = requests.get(store_url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        text_elements = soup.find_all(string=lambda s: "ogłoszeń" in s.lower())
        for text in text_elements:
            digits = ''.join(filter(str.isdigit, text))
            if digits.isdigit():
                return int(digits)
    except Exception as e:
        print(f"Błąd przy {store_url}: {e}")
    return 0

def extract_store_links_from_category_page(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    # Szukamy linków do ogłoszeń
    ad_links = soup.find_all("a", href=True)
    store_urls = set()
    for link in ad_links:
        href = link['href']
        if "-oferta.olx.pl" in href:
            # Normalizacja
            href = href.split("?")[0].split("#")[0]
            if href.endswith("/"):
                href = href
            else:
                href += "/"
            base_url = href.split("/")[2].split("-")[0]  # np. multigenus
            full_url = f"https://{base_url}-oferta.olx.pl/"
            store_urls.add(full_url)

    return list(store_urls)

def scrape_stores_with_more_than_400_ads(category_url, max_pages=5):
    found_stores = {}

    for page in range(1, max_pages + 1):
        print(f"🔍 Przeszukuję stronę {page}")
        url = f"{category_url}?page={page}"
        stores = extract_store_links_from_category_page(url)

        for store_url in stores:
            if store_url in found_stores:
                continue  # pomiń duplikaty

            count = get_offer_count_from_store(store_url)
            time.sleep(1)  # aby nie zablokowali

            if count > 8:
                name = store_url.split("//")[1].split("-")[0]
                found_stores[store_url] = (name, count)
                print(f"✅ {name}: {count} ogłoszeń")

    return found_stores

# 🔧 Przykład użycia – np. samochody osobowe
category_url = "https://www.olx.pl/motoryzacja/samochody"
results = scrape_stores_with_more_than_400_ads(category_url)

print("\n📊 Sklepy z ponad 400 ogłoszeniami:")
for url, (name, count) in results.items():
    print(f"{name} ({count}) → {url}")