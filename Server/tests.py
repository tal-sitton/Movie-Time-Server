import requests


def main():
    r = requests.get(
        "https://www.cinema-city.co.il/tickets/Events?Date=%D7%99%D7%95%D7%9D%C2%A0%D7%91%2004%2F07%2F2022")
    print(r.json())
    print(r.json()[0].keys())
    # date = r.json()[0]
    # r2 = requests.get(
    #     f"https://www.cinema-city.co.il/tickets/Events?TheatreId=1170&VenueTypeId=8&MovieId=0&Date={date}")
    # print(r2.json())


if __name__ == '__main__':
    main()
