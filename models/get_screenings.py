from typing import Callable, List, Dict

from requests import Session

from cinemas import yes_planet, rav_hen, hot_cinema, cinema_city, lev, movieland
from models import Screening

GetScreeningCallable = Callable[[str, str, str, Session], List[Screening]]

cinemas_get_screenings: Dict[str, GetScreeningCallable] = {
    "hot cinema": hot_cinema.get_screenings,
    "yes planet": yes_planet.get_screenings,
    "rav hen": rav_hen.get_screenings,
    "cinema city": cinema_city.get_screenings,
    "lev": lev.get_screenings,
    "movieland": movieland.get_screenings
}
