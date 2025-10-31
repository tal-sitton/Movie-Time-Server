import pytest
import requests

from seret.info_fetcher import fetch_info, create_movie_info_fetcher

# scheme: (movie_name, wanted_movie_name, expected_name, expected_image_url)
testData: list[tuple[str, str, list[str], list[str]]] = [
    ("Forever Young", "צעירים לנצח", ["צעירים לנצח"],
     ["https://www.edb.co.il/photos/181302022_poster01.poster.jpg",
      "https://www.seret.co.il/images/movies/ForeverYoung/ForeverYoung1.jpg"]),

    ("Everything Everywhere All At Once", "הכל בכל מקום בבת אחת", ["הכל בכל מקום בבת אחת"],
     ["https://www.edb.co.il/photos/173172022_poster01.poster.jpg",
      "https://www.seret.co.il/images/movies/EverythingEverywhereAllAtOnce/EverythingEverywhereAllAtOnce1.jpg"]),

    ("הסירו דאגה מלבכם", "הסירו דאגה מלבכם", ["הסירו דאגה מלבכם"],
     ["https://www.edb.co.il/photos/156702021_poster01.poster.jpg",
      "https://www.seret.co.il/images/movies/ShakeYourCaresAway/ShakeYourCaresAway1.jpg"]),

    ("65", "65", ["65"], ["https://www.edb.co.il/photos/179012023_poster01.poster.jpg",
                          "https://www.seret.co.il/images/movies/65/651.jpg"]),

    ("The Covenant", "החוזה", ["החוזה"], ["https://www.edb.co.il/photos/180152023_poster01.poster.jpg",
                                          "https://www.seret.co.il/images/movies/TheCovenant/TheCovenant1.jpg"]),

    ("העיר הזאת", "העיר הזאת", ["העיר הזאת"], ["https://www.edb.co.il/photos/182102023_poster01.poster.jpg",
                                               "https://www.seret.co.il/images/movies/TheCity/TheCity1.jpg"]),

    ("ההילולה - שנות ה90 הסרט", "ההילולה - שנות ה90 הסרט", ["ההילולה"],
     ["https://www.edb.co.il/photos/180332023_poster01.poster.jpg",
      "https://www.seret.co.il/images/movies/ShnotHaTishim/ShnotHaTishim1.jpg"]),

    ("Mission: Impossible Dead Reckoning Part 1", "משימה בלתי אפשרית: נקמת מוות-חלק ראשון",
     ["משימה בלתי אפשרית 7: נקמת מוות - חלק 1", "משימה בלתי אפשרית: נקמת מוות – חלק ראשון"],
     ["https://www.edb.co.il/photos/162822023_poster02.poster.jpg",
      "https://www.seret.co.il/images/movies/MissionImpossible7/MissionImpossible71.jpg"]),

    ("Rose", "אחותי", ["אחותי"], ["https://www.edb.co.il/photos/181952022_poster01.poster.jpg",
                                  "https://www.seret.co.il/images/movies/Rose/Rose1.jpg"]),

    ("Seven Blessings", "7 ברכות", ["7 ברכות", "שבע ברכות"],
     ["https://www.seret.co.il/images/movies/SevenBlessings/SevenBlessings1.jpg",
      "https://www.edb.co.il/photos/181342023_poster01.poster.jpg"]),

    (
        "Puppy Love", "אהבה עד העצם", ["אהבה עד העצם"],
        ["https://www.edb.co.il/photos/184152023_poster01.poster.jpg",
         "https://www.seret.co.il/images/movies/PuppyLove/PuppyLove1.jpg"]),

    ("Miraculous: Le Film", "המופלאה: הרפתקאות ליידי באג וחתול שחור", ["המופלאה: הרפתקאות ליידי באג וחתול שחור"],
     ["https://www.edb.co.il/photos/182662023_poster02.poster.jpg",
      "https://www.seret.co.il/images/movies/LadybugandCatNoirTheMovie/LadybugandCatNoirTheMovie1.jpg"]),

    ("Blood", "צמא דם", ["צמא דם"], ["https://www.edb.co.il/photos/184272022_poster01.poster.jpg",
                                     "https://www.seret.co.il/images/movies/Blood/Blood1.jpg"]),

    ("Wish", "המשאלה", ["המשאלה"], ["https://www.edb.co.il/photos/176452023_poster04.poster.jpg",
                                    "https://www.seret.co.il/images/movies/Wish/Wish1.jpg"]),

    ("Weekend Rebels", 'מורדים לסופ"ש', ['מורדים לסופ"ש', "מורדים לסופש"],
     ["https://www.edb.co.il/photos/187202023_poster01.poster.jpg",
      "https://www.seret.co.il/images/movies/WeeekendRebels/WeeekendRebels1.jpg"]),

    ("Kalki 2898 AD", 'קאלקי - אחרית הימים', ['קאלקי: אחרית הימים'],
     ["https://www.edb.co.il/photos/187762024_poster01.poster.jpg"]),

    ("Kalki 2898 AD", 'קאלקי-אחרית הימים-סרט הודי', ['קאלקי: אחרית הימים'],
     ["https://www.edb.co.il/photos/187762024_poster01.poster.jpg"]),

    ("Deadpool and Wolverine", 'דדפול ווולברין', ['דדפול & וולברין'],
     ["https://www.edb.co.il/photos/187052024_poster05.poster.jpg",
      "https://www.seret.co.il/images/movies/DeadpoolandWolverine/DeadpoolandWolverine1.jpg"]),
]

fake_movies_names = [
    ("Mission Imposibble: the last man standing", "משימה בלתי אפשרית: האיש האחרון בחיים"),
]


@pytest.mark.parametrize("movie_name,wanted_movie_name,expected_names,expected_image_urls", testData)
def test_seret_url(movie_name: str, wanted_movie_name: str, expected_names: list[str], expected_image_urls: list[str]):
    session = requests.Session()
    fetcher = create_movie_info_fetcher(session)
    movie = fetch_info(fetcher, movie_name, wanted_movie_name)
    assert movie.name in expected_names
    assert movie.image_url in expected_image_urls


@pytest.mark.parametrize("movie_name,wanted_movie_name", fake_movies_names)
def test_cant_find_movie(movie_name, wanted_movie_name):
    session = requests.Session()
    fetcher = create_movie_info_fetcher(session)
    movie = fetch_info(fetcher, movie_name, wanted_movie_name)
    assert movie.description == "לא נמצא תיאור"
