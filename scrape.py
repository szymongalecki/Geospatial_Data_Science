from datetime import date
import re
import requests
import pandas as pd
from bs4 import BeautifulSoup


"""
This script scrapes apartment data from boligzonen.dl for search in area of kobenhavn-kommune
Data is saved in batches of a page size in csv titled with scraping date
"""

url = "https://boligzonen.dk/lejebolig/kobenhavn-kommune"


def to_int(number: str) -> int:
    """custom int parser"""
    return int("".join([_ for _ in number if _.isnumeric()]))


def soup(url: str) -> BeautifulSoup:
    """creates soup for given url"""
    response = requests.get(url)
    content = response.content
    return BeautifulSoup(content, "html.parser")


def page_of_apartments(links: list) -> list:
    """returns data for every apartment on the page"""
    data = []
    for l in links:
        data.append(apartment_data(soup(l)))
    return data


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
    id = (
        s.find("div", class_="reference-number").contents[0].replace("Sagsnummer: ", "")
    )
    address = s.find(name="p", class_="address-line").contents
    street = address[0].strip(" ,")
    zip_code = int(address[-1].split()[0])
    rooms = int(s.find("div", string="Antal værelser").find_next_sibling().contents[0])
    area = to_int(s.find("div", string="Størrelse").find_next_sibling().contents[0])
    rent = to_int(s.find("div", string="Husleje").find_next_sibling().contents[0][:-2])
    try:
        location = s.find(class_="bg-map")
        latitude = float(location["data-lat"])
        longitude = float(location["data-lng"])
    except Exception as e:
        latitude = None
        longitude = None

    return {
        "id": id,
        "rooms": rooms,
        "area": area,
        "rent": rent,
        "street": street,
        "zip_code": zip_code,
        "latitude": latitude,
        "longitude": longitude,
    }


def scrape_all(url: str) -> None:
    """scrapes all pages of boligzonen.dk for given search and saves it in csv file"""
    s = soup(url)
    last = last_page(s)
    today = date.today().strftime("%d-%m-%y")

    with open(f"{today}.csv", "w") as f:
        f.write("id, rooms, area, rent, street, zip_code, latitude, longitude\n")

    for i in range(1, last + 1):
        page = page_of_apartments(apartments_on_page(soup(next_page(url, i))))
        with open(f"{today}.csv", "a") as f:
            pd.DataFrame(page).to_csv(f, header=False, index=False)


if __name__ == "__main__":
    scrape_all(url)
