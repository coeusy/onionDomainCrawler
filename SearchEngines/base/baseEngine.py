import requests
from bs4 import BeautifulSoup
import re
import os
from Databases.redisClient import RedisClient
from Utils.config_loader import ConfigLoader
from Utils.logger import Log
from Utils.utils import load_keywords
from traceback import format_exc
from concurrent.futures import ThreadPoolExecutor
import pickle
logger = Log().get_log()
cfg = ConfigLoader().config_dict['main']


class SearchEngine:
    def __init__(self, redis_client: RedisClient):
        self._session = requests.session()
        self.redis_client = redis_client
        self.tasks = set()
        self._initialize()
        self.url = None
        self.name = None

    def _initialize(self):
        self._session.proxies = {
            "http": cfg['tor-proxy']['http'],
            "https": cfg['tor-proxy']['https']
        }
        self.load_middle_status()

    def search(self, keyword):
        collector = set()
        try:
            self._search(keyword, collector)
            return True
        except Exception as e:
            logger.error(e)
            logger.error(format_exc())
            return False
        finally:
            logger.info(self.name, keyword, len(collector))
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
                logger.error(e)
                tried += 1
        logger.warning(self.name, " fail to get ", url, params)
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
            logger.error(e)

    def run(self):
        pool = ThreadPoolExecutor(max_workers=4)
        try:
            while len(self.tasks):
                keyword = self.tasks.pop()
                pool.submit(self.search, keyword)
        except Exception as e:
            logger.error(e)
            logger.error(format_exc())
        self.dump_middle_status()

    def dump_middle_status(self):
        dump_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "temp")
        os.makedirs(dump_dir, exist_ok=True)
        if len(self.tasks) != 0:
            pickle.dump(self.tasks, open(os.path.join(dump_dir, f"{self.name}.pkl"), "wb"))

    def load_middle_status(self):
        dump_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "temp")
        middle_filename = os.path.join(dump_dir, f"{self.name}.pkl")
        if os.path.exists(middle_filename):
            self.tasks = pickle.load(open(middle_filename, "rb"))
        else:
            self.tasks = load_keywords()
