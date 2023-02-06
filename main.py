from bs4 import BeautifulSoup
from pprint import pprint
import requests, json


DEBUG = True

url = "https://www.kinopoisk.ru/film/5078983/"

def get_page(url):
    page = requests.get(url)
    return BeautifulSoup(page.content, 'html.parser')



if DEBUG:
    with open("kino1.html", "r") as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
else:
    soup = get_page(url)


with open("produsser.html", "r") as f:
    prod = BeautifulSoup(f.read(), 'html.parser')

def get_produsser():
    produssers = []
    data_produsser = prod.find("div", class_="block_left").find_all("div")
    for i in data_produsser[1::3]:
        produsser = i.find("div", class_="name")
        if produsser:
            i = produsser.find("a").text.strip()
            produssers.append(i)
    return produssers



def get_data(name):
    divs = soup.find_all("div", class_="styles_titleLight__HIbfT styles_title__b1HVo")
    for div in divs:
        if div.text == name:
            parent_div = div.parent
            break
    i = parent_div.find_all("a")
    return map(lambda x: x.text.strip(), i)


def get_time_sec():
    time = soup.find_all('div', class_="styles_valueLight__nAaO3 styles_value__g6yP4")[15].text
    time_split = time.split(" ")
    time_in_minutes = int(time_split[0])
    time_in_seconds = time_in_minutes * 60
    return time_in_seconds


def get_film_data(soup):
    data: dict = dict()
    data["title"] = soup.title.text.strip()
    data["description"] = soup.find("p", class_="styles_root__aZJRN").text.strip()
    data["year"] = list(get_data("Год производства"))
    data["country"] = list(get_data("Страна"))
    data["genre"] = list(get_data("Жанр"))
    data["director"] = list(get_data("Режиссер"))
    data["producer"] = get_produsser()
    data["score"] = soup.find('span', class_="styles_ratingPositive__dzFSI").text.strip()
    data["ratings"] = soup.find('span', class_="styles_count__iOIwD").text.strip()
    data["age limit"] = soup.find("span", class_="styles_ageRate__340KC").text.strip()
    data["starring"] = list(map(lambda x: x.text.strip(), soup.find('ul', class_="styles_list___ufg4").find_all('li')))
    data["top 10"] = soup.find('div', class_="styles_listPosition__zA9OU").text.strip()
    data["platform"] = list(get_data("Платформа"))
    data["time"] = get_time_sec()
    data["image"] = "https:" + soup.find('img', class_="film-poster")['src']
    data["scenariy"] = list(get_data("Сценарий"))
    data["scenario"] = list(get_data("Оператор"))
    data["digital release"] = list(get_data("Цифровой релиз"))
    pprint(data)
    return data




def save_json(data):
    with open("data.json", "w") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
        
def main():
    data = get_film_data(soup)
    save_json(data)

    
if __name__ == "__main__":
    main()