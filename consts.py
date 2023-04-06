from enum import Enum

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
}


class MovieType(Enum):
    unknown = -1
    m_2D = 1
    m_3D = 2
    m_IMAX = 3
    m_VIP = 4
    m_SCREENX = 5
    m_4DX = 6


class LanguageType(Enum):
    UNKNOWN = -1
    DUBBED = 1
    SUBBED = 2


class Districts(Enum):
    DAN = ("גוש דן", 0)
    SHARON = ("השרון", 1)
    JERUSALEM = ("ירושלים", 2)
    ZAFON = ("הצפון", 3)
    DAROM = ("הדרום", 4)


movies = []
