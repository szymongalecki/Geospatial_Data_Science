import requests
from bs4 import BeautifulSoup

# test apartments
# url = "https://boligzonen.dk/lejeboliger/dejlig-lejlighed-pa-torvegade"
# url = "https://boligzonen.dk/lejeboliger/1-vaerelses-lejlighed-i-frederiksberg-0643ce75-2f8e-4311-9e2a-46ad9bfb3ad8"
url = "https://boligzonen.dk/lejeboliger/villalejlighed-frederiksberg-gratis-parkering-naer-metro"


def to_int(number: str) -> int:
    return int("".join([_ for _ in number if _.isnumeric()]))


def soup(url: str) -> BeautifulSoup:
    response = requests.get(url)
    content = response.content
    return BeautifulSoup(content, "html.parser")


def page_of_apartments():
    links = links_to_apartments()
    for l in links:
        print(apartment_data(soup(l)))


def links_to_apartments() -> list:
    root = "https://boligzonen.dk"
    s = soup("https://boligzonen.dk/lejebolig/kobenhavn-kommune")
    apartments = s.find("div", class_="row small-gutters properties").find_all(
        "a", class_="property-partial"
    )
    links = [root + a["href"] for a in apartments]
    return links


def apartment_data(s: BeautifulSoup) -> dict:
    # find and parse
    address = s.find(name="p", class_="address-line").contents
    street = address[0].strip(" ,")
    zip_code = int(address[-1].split()[0])
    rooms = int(s.find("div", string="Antal værelser").find_next_sibling().contents[0])
    area = to_int(s.find("div", string="Størrelse").find_next_sibling().contents[0])
    rent = to_int(s.find("div", string="Husleje").find_next_sibling().contents[0][:-2])
    location = s.find(class_="bg-map")
    latitude = float(location["data-lat"])
    longitude = float(location["data-lng"])

    # return apartment data
    return {
        "rooms": rooms,
        "area": area,
        "rent": rent,
        "street": street,
        "zip_code": zip_code,
        "latitude": latitude,
        "longitude": longitude,
    }


page_of_apartments()
