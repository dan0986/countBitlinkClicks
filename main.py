"""This script is designed to generate a short url link and count the number of
clicks on it.
"""
import os
import argparse
import requests
from dotenv import load_dotenv


def get_shorten_link(long_url, service_url, headers):
    """Return shorten link from url via bit.ly."""
    payload = {"long_url": long_url, "title": "create shorten_link"}
    response = requests.post(
        service_url.format("bitlinks"), headers=headers, json=payload
    )
    response.raise_for_status()
    shorten_link = response.json()["id"]
    return shorten_link


def get_count_clicks(link, service_url, headers):
    """Return clicks count for bitlink."""
    payload = {"units": "-1", "unit": "day"}
    url = service_url.format("bitlinks") + "/{}/clicks/summary".format(link)
    response = requests.get(url, headers=headers, params=payload)
    response.raise_for_status()
    count_clicks = response.json()["total_clicks"]
    return count_clicks


def main():
    """Main script entry"""
    parser = argparse.ArgumentParser(description=SCRIPT_DESCRIPTION)
    parser.add_argument("url", help="URL для создания короткой ссылки")
    args = parser.parse_args()
    if args.url.startswith("bit.ly"):
        try:
            print(
                "По Вашей ссылке перешли ",
                get_count_clicks(args.url, BITLY_BASE_URL, HEADER),
                " раз(а)",
            )
        except requests.exceptions.HTTPError:
            print(SCRIPT_ERROR_MESSAGE)
    else:
        try:
            bitlink = get_shorten_link(args.url, BITLY_BASE_URL, HEADER)
            print("Короткая ссылка", bitlink)
            print(
                "По вашей ссылке перешли ",
                get_count_clicks(bitlink, BITLY_BASE_URL, HEADER),
                " раз(а)",
            )
        except requests.exceptions.HTTPError:
            print(SCRIPT_WARN_MESSAGE)


if __name__ == "__main__":
    load_dotenv()
    BITLY_TOKEN = os.getenv("BITLY_TOKEN")
    BITLY_BASE_URL = "https://api-ssl.bitly.com/v4/{}"
    HEADER = {"Authorization": BITLY_TOKEN}
    SCRIPT_DESCRIPTION = """Скрипт для генерации короткой ссылки (bitlink)
    и подсчета кол-ва перехода по ней при помощи сервиса BITLY."""
    SCRIPT_WARN_MESSAGE = """Упс!!! Вы ввели неверную ссылку. Проверьте ее
    и попробуйте еще раз..."""
    SCRIPT_ERROR_MESSAGE = """Упс!!! Что-то пошло не так."""
    main()

