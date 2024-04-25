import logging

import requests


class ProxifiedSession:
    def __init__(self, session: requests.Session):
        self.session = session

    def __enter__(self):
        self.set_proxies()
        proxy_info = self.session.get("https://wtfismyip.com/json").json()
        logging.getLogger(__name__).info(f"Proxy: {proxy_info}")
        return self.session

    def set_proxies(self):
        proxy = "127.0.0.1:8118"
        self.session.proxies = {'http': proxy, 'https': proxy}

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.proxies = {}
        logging.getLogger(__name__).info("Proxy removed")
