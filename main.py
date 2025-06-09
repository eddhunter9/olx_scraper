import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0"
}

# def get_user_data(user_url):
#     response = requests.get(user_url, headers=headers)
#     soup = BeautifulSoup(response.text, 'html.parser')
#
#     # Szukamy liczby ogłoszeń
#     listing_info = soup.find("div", string=lambda text: text and "ogłoszeń użytkownika" in text.lower())
#     if listing_info:
#         count = int(''.join(filter(str.isdigit, listing_info.text)))
#         if count > 400:
#             print(f"{user_url} -> {count} ogłoszeń")
#             return user_url, count
#     else:
#         print("blad")

def get_offer_count_from_store(url):
    response = requests.get(url, headers=headers)
    print("🧾 Odpowiedź z OLX (pierwsze 500 znaków):\n", response.text[:500])

    soup = BeautifulSoup(response.text, "html.parser")

    # HTML sklepów wygląda inaczej — tu przykład elementu z liczbą ogłoszeń
    # Zazwyczaj znajdziesz to w nagłówku strony lub po frazie "ogłoszeń"
    text_elements = soup.find_all(string=lambda s: "ogłoszeń" in s.lower())

    for text in text_elements:
        digits = ''.join(filter(str.isdigit, text))
        if digits.isdigit():
            count = int(digits)
            print(f"{url} -> {count} ogłoszeń")
            return count
    return 0

# Test dla sklepu multigenus:
store_url = "https://multigenus-oferta.olx.pl/home/"
store2="https://audiblask.olx.pl/home/"

store3="https://skotniki.olx.pl/home/" #<400

store_from_repo="https://mokced.olx.pl/home/"

get_offer_count_from_store(store3)

#nie czyta:
#https://emotomax.otomoto.pl/inventory
#https://www.olx.pl/oferty/uzytkownik/1E6FOg/

# Przykład działania na jednej stronie użytkownika:
pattern_url="https://www.olx.pl/oferty/uzytkownik/Rafal/"

#test 1 user-ciąg liczb
user1=pattern_url
#get_offer_count_from_store(user1)
