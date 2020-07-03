import requests
from bs4 import BeautifulSoup
import re


class SearchEngine:
    def __init__(self):
        self._session = requests.session()
        self._initialize()
        self.url = None

    def _initialize(self):
        self._session.proxies = {
            "http": "socks5h://127.0.0.1:9050",
            "https": "socks5h://127.0.0.1:9050"
        }

    def search(self, keyword: str):
        pass

    def _get(self, url, retry=5, timeout=60):
        tried = 0
        while tried < retry:
            try:
                resp = self._session.get(url, timeout=timeout)
                if resp.status_code == 200:
                    return resp
                else:
                    tried += 1
            except requests.exceptions.ReadTimeout:
                tried += 1
        print(self.url, " fail to get ", url)
        return None

    @staticmethod
    def _parse(page_source, collector: set):
        try:
            soup = BeautifulSoup(page_source, features="lxml")
            for a in soup.find_all("a"):
                if a.has_attr("href"):
                    href = a['href'].replace("%2F", "/").replace("%3A", ":")
                    res = re.search("(http|https)://[a-zA-Z0-9]+.onion", href)
                    if res:
                        print(res.group())
                        collector.add(res.group())
        except Exception as e:
            print(e)
