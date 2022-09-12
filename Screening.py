import json

import consts


class Screening:
    def __init__(self, m_date: str, m_cinema: str, m_location: str, m_district: consts.Districts, m_title: str,
                 m_type: consts.MovieType, m_time: str, m_link: str, coords: tuple):
        self.m_date = m_date
        self.m_cinema = m_cinema
        self.m_location = m_location
        self.m_district = m_district
        self.m_title = m_title
        self.m_type = m_type
        self.m_time = m_time
        self.m_link = m_link
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
