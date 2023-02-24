import json

import consts

THREE_D = ["3D", "תלת מימד", "תלת-מימד"]
IMAX = "IMAX"
VIP = "VIP"
REDUNDANT_IN_TITLE = ["דו מימד", "דו-מימד"]


def type_from_title(title: str, movie_type: consts.MovieType):
    if movie_type == consts.MovieType.unknown:
        movie_type = consts.MovieType.m_2D
    for keyword in THREE_D:
        if keyword in title:
            movie_type = consts.MovieType.m_3D
            title = title.replace(keyword, "")
    if IMAX in title:
        title = title.replace(IMAX, "")
        movie_type = consts.MovieType.m_IMAX
    if VIP in title.upper():
        title = title.replace(VIP, "")
        movie_type = consts.MovieType.m_VIP

    title = title.strip().strip("-").strip()
    return clear_title(title), movie_type


def clear_title(title: str):
    for keyword in REDUNDANT_IN_TITLE:
        title = title.replace(keyword, "")
    return title.strip().strip("-").strip()


class Screening:
    def __init__(self, date: str, cinema: str, location: str, district: consts.Districts, title: str,
                 screening_type: consts.MovieType, time: str, link: str, coords: tuple):
        title, screening_type = type_from_title(title, screening_type)
        self.m_date = date
        self.m_cinema = cinema
        self.m_location = location
        self.m_district = district
        self.m_title = title
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
                "coords": self.m_coords
            }
        )

    def __str__(self):
        return f"{self.m_date} \n\t {self.m_cinema} \n\t\t {self.m_location} \n\t\t {self.m_district.value[0]}\n\t\t\t " \
               f"{self.m_title} \n\t\t\t\t {self.m_type.name.replace('m_', '')} \n\t\t\t\t {self.m_time} \n\t\t\t\t " \
               f"{self.m_link} \n\t\t\t\t {self.m_coords} "
