import pytest
import requests

from .seret_api import get_info

testData = [
    ("סרט: האחים סופר מריו", "סרט: האחים סופר מריו", "האחים סופר מריו: הסרט",
     "https://www.seret.co.il/images/movies/Mario/Mario1.jpg"),
    ("צעירים לנצח", "צעירים לנצח", "צעירים לנצח",
     "https://www.seret.co.il/images/movies/ForeverYoung/ForeverYoung1.jpg"),
    ("הכל בכל מקום בבת אחת", "הכל בכל מקום בבת אחת", "הכל בכל מקום בבת אחת",
     "https://www.seret.co.il/images/movies/EverythingEverywhereAllAtOnce/EverythingEverywhereAllAtOnce1.jpg"),
    ("הסירו דאגה מלבכם", "הסירו דאגה מלבכם", "הסירו דאגה מלבכם",
     "https://www.seret.co.il/images/movies/ShakeYourCaresAway/ShakeYourCaresAway1.jpg"),
    ("65", "65", "65", "https://www.seret.co.il/images/movies/65/651.jpg"),
    ("החוזה", "החוזה", "החוזה", "https://www.seret.co.il/images/movies/TheCovenant/TheCovenant1.jpg"),
    ("העיר הזאת", "העיר הזאת", "העיר הזאת", "https://www.seret.co.il/images/movies/TheCity/TheCity1.jpg"),
    ("ההילולה - שנות ה90 הסרט", "ההילולה - שנות ה90 הסרט", "ההילולה",
     "https://www.seret.co.il/images/movies/ShnotHaTishim/ShnotHaTishim1.jpg"),
    ("משימה בלתי אפשרית: נקמת מוות-חלק ראשון", "משימה בלתי אפשרית: נקמת מוות-חלק ראשון",
     "משימה בלתי אפשרית: נקמת מוות – חלק ראשון",
     "https://www.seret.co.il/images/movies/MissionImpossible7/MissionImpossible71.jpg"),
    ("אחותי", "אחותי", "אחותי", "https://www.seret.co.il/images/movies/Rose/Rose1.jpg"),
    ("Seven Blessings", "7 ברכות", "7 ברכות",
     "https://www.seret.co.il/images/movies/SevenBlessings/SevenBlessings1.jpg"),
    ("Puppy Love", "אהבה עד העצם", "אהבה עד העצם", "https://www.seret.co.il/images/movies/PuppyLove/PuppyLove1.jpg"),
]


@pytest.mark.parametrize("movie_name,wanted_movie_name,expected_name,expected_image_url", testData)
def test_seret_url(movie_name, wanted_movie_name, expected_name, expected_image_url):
    session = requests.Session()
    movie = get_info(session, movie_name, wanted_movie_name)
    assert movie.name == expected_name
    assert movie.image_url == expected_image_url


def test_cant_find_movie():
    session = requests.Session()
    movie = get_info(session, "Miraculous: Le Film", "המופלאה: הרפתקאות ליידי באג וחתול שחור")
    assert movie is None
