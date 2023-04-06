import json
import re

from consts import MovieType, LanguageType, Districts

THREE_D = ["3D", "תלת מימד", "תלת-מימד"]
DUBBED_TITLE = ["מדובב", "עברית"]
IMAX = "IMAX"
VIP = "VIP"
REDUNDANT_IN_TITLE = ["דו מימד", "דו-מימד", IMAX, VIP, *THREE_D, *DUBBED_TITLE, "אנגלית"]


def type_from_title(title: str, movie_type: MovieType):
    if movie_type == MovieType.unknown:
        movie_type = MovieType.m_2D
    for keyword in THREE_D:
        if keyword in title:
            movie_type = MovieType.m_3D
    if IMAX in title:
        movie_type = MovieType.m_IMAX
    if VIP in title.upper():
        movie_type = MovieType.m_VIP

    return movie_type


def dubbed_from_title(title: str, lang_type: LanguageType):
    if lang_type == LanguageType.UNKNOWN:
        if any(keyword in title for keyword in DUBBED_TITLE):
            return LanguageType.DUBBED
        return LanguageType.SUBBED
    return lang_type


def clear_title(title: str):
    for keyword in REDUNDANT_IN_TITLE:
        title = title.split(keyword)[0]
    return re.sub(r"\W*$", "", title)


class Screening:
    def __init__(self, date: str, cinema: str, location: str, district: Districts, title: str,
                 screening_type: MovieType, time: str, link: str, coords: tuple,
                 dubbed: LanguageType):
        screening_type = type_from_title(title, screening_type)
        self.m_dubbed = dubbed_from_title(title, dubbed)
        self.m_title = clear_title(title)
        self.m_date = date
        self.m_cinema = cinema
        self.m_location = location
        self.m_district = district
        self.m_type = screening_type
        self.m_time = time
        self.m_link = link
        self.m_coords = coords

    def json(self):
        return json.dumps(
            {
                "date": self.m_date,
                "cinema": self.m_cinema,
                "location": self.m_location,
                "district": self.m_district.value[0],
                "title": self.m_title,
                "type": self.m_type.name.replace("m_", ""),
                "time": self.m_time,
                "link": self.m_link,
                "coords": self.m_coords,
                "dubbed": self.m_dubbed == LanguageType.DUBBED,
            }
            , ensure_ascii=False)

    def __str__(self):
        return f"{self.m_date} \n\t {self.m_cinema} \n\t\t {self.m_location} \n\t\t {self.m_district.value[0]}\n\t\t\t " \
               f"{self.m_title} \n\t\t\t\t {self.m_type.name.replace('m_', '')} \n\t\t\t\t {self.m_time} \n\t\t\t\t " \
               f"{self.m_link} \n\t\t\t\t {self.m_coords} \n\t\t\t\t {self.m_dubbed.name}"
