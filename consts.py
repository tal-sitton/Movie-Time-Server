import sys
from enum import Enum

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

options = webdriver.ChromeOptions()
options.add_argument('--blink-settings=imagesEnabled=false')
if len(sys.argv) > 1:
    driver = webdriver.Chrome(ChromeDriverManager().install())
else:
    options.binary_location = "GoogleChromePortableBeta/App/Chrome-bin/chrome.exe"
    driver = webdriver.Chrome(options=options)

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
