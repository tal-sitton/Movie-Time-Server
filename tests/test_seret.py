import pytest
import requests

from seret.info_fetcher import fetch_info, create_movie_info_fetcher

# scheme: (movie_name, wanted_movie_name, expected_name, expected_image_url)
testData: list[tuple[str, str, str, str]] = [
    ("Forever Young", "צעירים לנצח", "צעירים לנצח",
     "https://www.seret.co.il/images/movies/ForeverYoung/ForeverYoung1.jpg"),

    ("Everything Everywhere All At Once", "הכל בכל מקום בבת אחת", "הכל בכל מקום בבת אחת",
     "https://www.seret.co.il/images/movies/EverythingEverywhereAllAtOnce/EverythingEverywhereAllAtOnce1.jpg"),

    ("הסירו דאגה מלבכם", "הסירו דאגה מלבכם", "הסירו דאגה מלבכם",
     "https://www.seret.co.il/images/movies/ShakeYourCaresAway/ShakeYourCaresAway1.jpg"),

    ("65", "65", "65", "https://www.seret.co.il/images/movies/65/651.jpg"),

    ("The Covenant", "החוזה", "החוזה", "https://www.seret.co.il/images/movies/TheCovenant/TheCovenant1.jpg"),

    ("העיר הזאת", "העיר הזאת", "העיר הזאת", "https://www.seret.co.il/images/movies/TheCity/TheCity1.jpg"),

    ("ההילולה - שנות ה90 הסרט", "ההילולה - שנות ה90 הסרט", "ההילולה",
     "https://www.seret.co.il/images/movies/ShnotHaTishim/ShnotHaTishim1.jpg"),

    ("Mission: Impossible Dead Reckoning Part 1", "משימה בלתי אפשרית: נקמת מוות-חלק ראשון",
     "משימה בלתי אפשרית: נקמת מוות – חלק ראשון",
     "https://www.seret.co.il/images/movies/MissionImpossible7/MissionImpossible71.jpg"),

    ("Rose", "אחותי", "אחותי", "https://www.seret.co.il/images/movies/Rose/Rose1.jpg"),

    ("Seven Blessings", "7 ברכות", "7 ברכות",
     "https://www.seret.co.il/images/movies/SevenBlessings/SevenBlessings1.jpg"),

    ("Puppy Love", "אהבה עד העצם", "אהבה עד העצם", "https://www.seret.co.il/images/movies/PuppyLove/PuppyLove1.jpg"),

    ("Miraculous: Tales of Ladybug & Cat Noir", "המופלאה", "המופלאה: הרפתקאות ליידי באג וחתול שחור",
     "https://www.seret.co.il/images/movies/LadybugandCatNoirTheMovie/LadybugandCatNoirTheMovie1.jpg"),

    ("Miraculous: Le Film", "המופלאה: הרפתקאות ליידי באג וחתול שחור", "המופלאה: הרפתקאות ליידי באג וחתול שחור",
     "https://www.seret.co.il/images/movies/LadybugandCatNoirTheMovie/LadybugandCatNoirTheMovie1.jpg"),

    ("Blood", "צמא דם", "צמא דם", "https://www.seret.co.il/images/movies/Blood/Blood1.jpg"),

    ("Home", "בית", "בית", "https://www.seret.co.il/images/movies/Home2023/Home20231.jpg"),

    ("Wish", "המשאלה", "המשאלה", "https://www.seret.co.il/images/movies/Wish/Wish1.jpg"),

    ("Weekend Rebels", 'מורדים לסופ"ש', 'מורדים לסופש', "https://www.seret.co.il/images/movies/WeeekendRebels/WeeekendRebels1.jpg"),
]

fake_movies_names = [
    ("really not a real movie", "סרט מאוד לא אמיתי"),
]


@pytest.mark.parametrize("movie_name,wanted_movie_name,expected_name,expected_image_url", testData)
def test_seret_url(movie_name, wanted_movie_name, expected_name, expected_image_url):
    session = requests.Session()
    fetcher = create_movie_info_fetcher(session)
    movie = fetch_info(fetcher, movie_name, wanted_movie_name)
    assert movie.name == expected_name
    assert movie.image_url == expected_image_url


@pytest.mark.parametrize("movie_name,wanted_movie_name", fake_movies_names)
def test_cant_find_movie(movie_name, wanted_movie_name):
    session = requests.Session()
    fetcher = create_movie_info_fetcher(session)
    movie = fetch_info(fetcher, movie_name, wanted_movie_name)
    assert movie.description == "לא נמצא תיאור"
