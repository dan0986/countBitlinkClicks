import os
import argparse
import requests
from dotenv import load_dotenv

BITLY_TOKEN = os.getenv("BITLY_TOKEN")
BITLY_BASE_URL = "https://api-ssl.bitly.com/v4/{}"
HEADERS = {
    "Authorization": BITLY_TOKEN
    }

def get_shorten_link(token, url):
    """ Return shorten link from url via bit.ly"""
    payload = {
      "long_url": url,
      "title": "create shorten_link"
    }
    response = requests.post(BITLY_BASE_URL.format("bitlinks"), headers=HEADERS, json=payload)
    response.raise_for_status()
    shorten_link = response.json()["id"]
    return shorten_link

def get_count_clicks(token, link):
    """ Return clicks count for bitlink"""
    payload = {
      "units": "-1",
      "unit": "day"
    }
    url = BITLY_BASE_URL.format("bitlinks") + "/{}/clicks/summary".format(link)
    response = requests.get(url, headers=HEADERS, params=payload)
    response.raise_for_status()
    count_clicks = response.json()["total_clicks"]
    return count_clicks
    
def main():
    parser = argparse.ArgumentParser(description="""Скрипт для генерации короткой ссылки (bitlink) 
                                    \nи подсчета кол-ва перехода по ней при помощи сервиса BITLY."""
    )
    parser.add_argument("url", help="URL для создания короткой ссылки")
    args = parser.parse_args()
    if args.url.startswith("bit.ly"):
        try:
            print("По Вашей ссылке перешли ", get_count_clicks(BITLY_TOKEN, args.url), " раз(а)")
        except requests.exceptions.HTTPError:
            print("Упс!!! Что-то пошло не так.")
    else:
        try:
            bitlink = get_shorten_link(BITLY_TOKEN, args.url)
            print("Короткая ссылка", bitlink)
            print("По вашей ссылке перешли ", get_count_clicks(BITLY_TOKEN, bitlink), " раз(а)")
        except requests.exceptions.HTTPError:
            print("Упс!!! Вы ввели неверную ссылку. Проверьте ее и попробуйте еще раз...")

if __name__ == "__main__":
    load_dotenv()
    main()
