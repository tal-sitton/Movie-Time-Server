import json

# noinspection PyUnresolvedReferences
import chromedriver_binary  # Adds chromedriver binary to path
import requests


class FlaredResponse:
    def __init__(self, response: str, original_response: requests.Response):
        self.response = response
        self.original_response = original_response

    def json(self):
        return json.loads(self.response)

    @property
    def text(self):
        return self.response

    @property
    def ok(self):
        return self.original_response.ok


class FlaredSession:
    def __init__(self, session: requests.Session):
        self.session = session

    def get(self, url, **kwargs):
        data = self.session.post(
            "http://127.0.0.1:8191/v1",
            json={
                "cmd": "request.get",
                "url": url,
                "maxTimeout": 60000
            })
        raw_response: str = data.json()["solution"]["response"]
        if raw_response.find("{") != -1 and raw_response.find("{") < raw_response.find("["):
            raw_response = "{" + raw_response.split("{", 1)[1].rsplit("}", 1)[0] + "}"
        elif raw_response.find("[") != -1:
            raw_response = "[" + raw_response.split("[", 1)[1].rsplit("]", 1)[0] + "]"
        return FlaredResponse(raw_response, data)


class FlaredProxy:
    def __init__(self, session: requests.Session):
        self.session = session

    def __enter__(self):
        flared_session = FlaredSession(self.session)
        return flared_session

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
