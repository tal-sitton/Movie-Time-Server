import sys
from enum import Enum

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType

chrome_options = webdriver.ChromeOptions()

options = [
    "--headless",
    "--disable-gpu",
    "--window-size=1920,1200",
    "--ignore-certificate-errors",
    "--disable-extensions",
    "--no-sandbox",
    "--disable-dev-shm-usage",
    "--blink-settings=imagesEnabled=false"
]
for option in options:
    chrome_options.add_argument(option)

driver_path = ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()
driver = webdriver.Chrome(driver_path, options=chrome_options)
driver.implicitly_wait(10)

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
}


class MovieType(Enum):
    m_2D = 1
    m_3D = 2
    m_IMAX = 3
    m_VIP = 4
    m_SCREENX = 5
    m_4DX = 6


movies = []
