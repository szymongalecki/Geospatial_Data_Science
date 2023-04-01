import re
import requests
from bs4 import BeautifulSoup

# test apartments
# url = "https://boligzonen.dk/lejeboliger/villalejlighed-frederiksberg-gratis-parkering-naer-metro"
url = "https://boligzonen.dk/lejebolig/kobenhavn-kommune"


def to_int(number: str) -> int:
    """custom int parser"""
    return int("".join([_ for _ in number if _.isnumeric()]))


def soup(url: str) -> BeautifulSoup:
    """creates soup for given url"""
    response = requests.get(url)
    content = response.content
    return BeautifulSoup(content, "html.parser")


def page_of_apartments(links: list) -> None:
    """prints out data for every apartment"""
    for l in links:
        print(apartment_data(soup(l)))


def apartments_on_page(s: BeautifulSoup) -> list:
    """returns links for all the apartments on page"""
    root = "https://boligzonen.dk"
    apartments = s.find("div", class_="row small-gutters properties").find_all(
        "a", class_="property-partial"
    )
    links = [root + a["href"] for a in apartments]
    return links


def last_page(s: BeautifulSoup) -> int:
    """returns the number of the last page for given search soup"""
    rel = s.find("span", class_="last").find("a", href=True)["href"]
    last = int(re.search("page=[0-9]+", rel).group().strip("page="))
    return last


def next_page(url: str, page: int) -> str:
    """constructs url for the next page of a given search"""
    link = f"{url}?page={page}"
    return link


def apartment_data(s: BeautifulSoup) -> dict:
    """finds, parses and returns desired data of a single apartment"""
    address = s.find(name="p", class_="address-line").contents
    street = address[0].strip(" ,")
    zip_code = int(address[-1].split()[0])
    rooms = int(s.find("div", string="Antal værelser").find_next_sibling().contents[0])
    area = to_int(s.find("div", string="Størrelse").find_next_sibling().contents[0])
    rent = to_int(s.find("div", string="Husleje").find_next_sibling().contents[0][:-2])
    location = s.find(class_="bg-map")
    latitude = float(location["data-lat"])
    longitude = float(location["data-lng"])

    return {
        "rooms": rooms,
        "area": area,
        "rent": rent,
        "street": street,
        "zip_code": zip_code,
        "latitude": latitude,
        "longitude": longitude,
    }


def scrape_all(url: str) -> None:
    """scrapes all pages of boligzonen.dk for given search"""
    s = soup(url)
    last = last_page(s)
    for i in range(1, last + 1):
        page_of_apartments(apartments_on_page(soup(next_page(url, i))))


if __name__ == "__main__":
    scrape_all(url)
