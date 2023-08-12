import pytest
import requests

from .seret_api import get_info

testData = [
    ("מריו", "האחים סופר מריו: הסרט", "https://www.seret.co.il/images/movies/Mario/Mario1.jpg"),
    ("סרט: האחים סופר מריו", "האחים סופר מריו: הסרט", "https://www.seret.co.il/images/movies/Mario/Mario1.jpg"),
    ("צעירים לנצח", "צעירים לנצח", "https://www.seret.co.il/images/movies/ForeverYoung/ForeverYoung1.jpg"),
    ("הכל בכל מקום בבת אחת", "הכל בכל מקום בבת אחת",
     "https://www.seret.co.il/images/movies/EverythingEverywhereAllAtOnce/EverythingEverywhereAllAtOnce1.jpg"),
    ("הסירו דאגה מלבכם", "הסירו דאגה מלבכם",
     "https://www.seret.co.il/images/movies/ShakeYourCaresAway/ShakeYourCaresAway1.jpg"),
    ("65", "65", "https://www.seret.co.il/images/movies/65/651.jpg"),
    ("החוזה", "החוזה", "https://www.seret.co.il/images/movies/TheCovenant/TheCovenant1.jpg"),
    ("העיר הזאת", "העיר הזאת", "https://www.seret.co.il/images/movies/TheCity/TheCity1.jpg"),
    ("ההילולה - שנות ה90 הסרט", "ההילולה", "https://www.seret.co.il/images/movies/ShnotHaTishim/ShnotHaTishim1.jpg"),
    ("משימה בלתי אפשרית: נקמת מוות-חלק ראשון", "משימה בלתי אפשרית: נקמת מוות – חלק ראשון",
     "https://www.seret.co.il/images/movies/MissionImpossible7/MissionImpossible71.jpg"),
    ("אחותי", "אחותי", "https://www.seret.co.il/images/movies/Rose/Rose1.jpg"),
]


@pytest.mark.parametrize("movie_name,expected_name,expected_image_url", testData)
def test_seret_url(movie_name, expected_name, expected_image_url):
    session = requests.Session()
    movie = get_info(session, movie_name)
    assert movie.name == expected_name
    assert movie.image_url == expected_image_url


def test_invalid_seret_url():
    session = requests.Session()
    movie = get_info(session, "מ")
    assert movie.name == "מ"
    assert movie.image_url == ""
    assert movie.rating is None
