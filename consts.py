import os

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.3',
    'referer': 'https://www.bing.com/'
}

LOGGING_LEVEL = os.environ.get("LOGGING_LEVEL") or "DEBUG"
