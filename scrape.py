import requests
from bs4 import BeautifulSoup

# test apartments
# url = "https://boligzonen.dk/lejeboliger/dejlig-lejlighed-pa-torvegade"
# url = "https://boligzonen.dk/lejeboliger/1-vaerelses-lejlighed-i-frederiksberg-0643ce75-2f8e-4311-9e2a-46ad9bfb3ad8"
url = "https://boligzonen.dk/lejeboliger/villalejlighed-frederiksberg-gratis-parkering-naer-metro"


def to_int(number: str) -> int:
    return int("".join([_ for _ in number if _.isnumeric()]))


def apartment_data(url: str) -> dict:
    # scrape
    response = requests.get(url)
    content = response.content
    soup = BeautifulSoup(content, "html.parser")

    # find and parse
    address = soup.find(name="p", class_="address-line").contents
    street = address[0].strip(" ,")
    zip_code = int(address[-1].split()[0])
    rooms = int(
        soup.find(name="div", string="Antal værelser").find_next_sibling().contents[0]
    )
    area = to_int(
        soup.find(name="div", string="Størrelse").find_next_sibling().contents[0]
    )
    rent = to_int(
        soup.find(name="div", string="Husleje").find_next_sibling().contents[0][:-2]
    )
    location = soup.find(class_="bg-map")
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


print(apartment_data(url))
