import requests
from bs4 import BeautifulSoup


def to_number(number: str) -> int:
    return int("".join([_ for _ in number if _.isnumeric()]))


url = "https://boligzonen.dk/lejeboliger/dejlig-lejlighed-pa-torvegade"
response = requests.get(url)
content = response.content
soup = BeautifulSoup(content, "html.parser")

number_of_rooms = int(
    soup.find(name="div", string="Antal værelser").find_next_sibling().contents[0]
)

area = to_number(
    soup.find(name="div", string="Størrelse").find_next_sibling().contents[0]
)
rent_price = to_number(
    soup.find(name="div", string="Husleje").find_next_sibling().contents[0][:-2]
)


print(number_of_rooms, area, rent_price)
