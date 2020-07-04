import requests
from bs4 import BeautifulSoup
import re
from Databases.redisClient import RedisClient


class SearchEngine:
    def __init__(self, redis_client: RedisClient):
        self._session = requests.session()
        self.redis_client = redis_client
        self._initialize()
        self.url = None
        self.name = None

    def _initialize(self):
        self._session.proxies = {
            "http": "socks5h://127.0.0.1:9050",
            "https": "socks5h://127.0.0.1:9050"
        }

    def search(self, keyword):
        collector = set()
        self._search(keyword, collector)
        print(self.name, keyword, len(collector))
        self._save(collector)

    def _save(self, collector):
        for domain in collector:
            self.redis_client.add_domain(domain)

    def _search(self, keyword: str, collector: set):
        pass

    def _get(self, url, params, retry=5, timeout=60):
        tried = 0
        while tried < retry:
            try:
                resp = self._session.get(url, timeout=timeout, params=params)
                if resp.status_code == 200:
                    return resp
                else:
                    tried += 1
            except requests.exceptions.ReadTimeout:
                tried += 1
            except requests.exceptions.ConnectionError:
                tried += 1
            except Exception as e:
                print(e)
                tried += 1
        print(self.name, " fail to get ", url, params)
        return None

    @staticmethod
    def _parse(page_source, collector: set):
        try:
            soup = BeautifulSoup(page_source, features="lxml")
            for a in soup.find_all("a"):
                if a.has_attr("href"):
                    href = a['href'].replace("%2F", "/").replace("%3A", ":")
                    res = re.search(r"https?://[a-zA-Z0-9]+.onion", href)
                    if res:
                        if res.group() not in collector:
                            collector.add(res.group())
        except Exception as e:
            print(e)

    def run(self, keywords):
        for keyword in keywords():
            self.search(keyword)
