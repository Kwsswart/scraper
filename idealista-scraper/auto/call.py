from random import randint
from scraper import Scraper
from time import sleep


def main():

    url = "https://www.idealista.com/alquiler-viviendas/santa-cruz-de-tenerife/centro-ifara/centro/"
    a = Scraper(url)
    for i in range(len(a.links)):
        a.get_page()
        print(len(a.links))
        print(len(a.data))
        sleep((randint(1,10) + 10) * 60)
    a.to_json()
    a.to_csv()
    a.to_text()


if __name__ == "__main__":
    main()