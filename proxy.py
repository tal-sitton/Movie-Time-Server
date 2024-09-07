import json
import logging

# noinspection PyUnresolvedReferences
import chromedriver_binary  # Adds chromedriver binary to path
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium_stealth import stealth


class MyResponse:
    def __init__(self, html: str, pre: str | None):
        self.html = html
        self.pre = pre

    def json(self):
        return json.loads(self.pre)

    @property
    def text(self):
        return self.html


class MyDriver:
    def __init__(self, driver: webdriver.Chrome):
        self.driver = driver

    def get(self, url, **kwargs):
        self.driver.get(url)
        res = self.driver.page_source
        elems = self.driver.find_elements(By.TAG_NAME, 'pre')
        pre = elems[0].text if elems else None
        return MyResponse(res, pre)


class ProxifiedSession:
    def __init__(self, session: requests.Session):
        self.session = session
        self.driver: MyDriver | None = None

    def __enter__(self):
        driver = MyDriver(self.set_proxies())
        proxy_info = driver.get("https://wtfismyip.com/json").json()
        logging.getLogger(__name__).info(f"Proxy: {proxy_info}")
        self.driver = driver
        return driver

    def set_proxies(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        proxy_addr = "127.0.0.1:8118"
        options.add_argument('--proxy-server=' + proxy_addr)
        options.add_argument('--ignore-certificate-errors')
        driver = webdriver.Chrome(options=options)

        stealth(driver,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
                )
        return driver

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.proxies = {}
        self.driver.driver.quit()
        logging.getLogger(__name__).info("Proxy removed")
