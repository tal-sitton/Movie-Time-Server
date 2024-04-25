import logging

from bs4 import BeautifulSoup

from seret.movie_info import SeretMovieInfo


def find_canonical_url(soup: BeautifulSoup) -> str:
    return soup.find("link", {"rel": "canonical"})['href']


def get_seret_movie_info(soup: BeautifulSoup) -> SeretMovieInfo:
    name = soup.find("meta", {"property": "og:title"})['content']
    english_name = soup.find("span", {"itemprop": "alternatename"}).text
    description = soup.find("span", {"itemprop": "description"})
    image_url = soup.find("meta", {"property": "og:image"})['content']

    raw_year = soup.find("span", {"itemprop": "dateCreated"})
    if raw_year and raw_year.text.isdigit():
        year = int(raw_year.text)
    else:
        logging.warning(f"Failed to get year for {name}")
        year = None

    return SeretMovieInfo(english_name, name, description, image_url, year)
