from baseEngine import *


class TorchSearch(SearchEngine):
    def __init__(self):
        super().__init__()
        self.url = "http://xmh57jrzrnw6insl.onion"
        self.name = "Torch"

    def search(self, keyword: str):
        collector = set()
        search_url = f"{self.url}/4a1f6b371c/search.cgi"
        params = {
            "s": "DRP",
            "q": keyword,
            "cmd": "Search!",
        }
        for i in range(100):
            params['np'] = i
            resp = self._get(search_url, params=params)
            if "No documents were found containing" in resp.text:
                break
            self._parse(resp.text, collector)


class NotEvilSearch(SearchEngine):
    def __init__(self):
        super().__init__()
        self.url = "http://hss3uro2hsxfogfq.onion"
        self.name = "not Evil"
        self._session_id = self._get_session_id()

    def search(self, keyword: str):
        if len(keyword) < 4:
            return
        collector = set()
        search_url = f"{self.url}/index.php"
        params = {
            "q": keyword,
            "hostLimit": 20,
            "numRows": 20,
            "template": 0,
            "session": self._session_id
        }
        for i in range(100):
            params["start"] = params["numRows"] * 20
            resp = self._get(search_url, params=params)
            self._parse(resp.text, collector)

    def _get_session_id(self):
        resp = self._get(self.url, params={})
        soup = BeautifulSoup(resp.text, features="lxml")
        for element in soup.find_all("input"):
            if element.attrs['name'] == "session":
                return element.attrs["value"]


class AhmiaSearch(SearchEngine):
    def __init__(self):
        super().__init__()
        self.url = "http://msydqstlz2kzerdg.onion"
        self.name = "Ahmia"

    def search(self, keyword: str):
        collector = set()
        search_url = f"{self.url}/search"
        params = {
            "q": keyword
        }
        resp = self._get(search_url, params=params)
        self._parse(resp.text, collector)


class HaystakSearch(SearchEngine):
    def __init__(self):
        super().__init__()
        self.url = "http://haystakvxad7wbk5.onion"
        self.name = "Haystak"

    def search(self, keyword: str):
        collector = set()
        search_url = self.url
        params = {
            "q": keyword
        }
        for i in range(500):
            params["offset"] = i * 20
            resp = self._get(search_url, params=params)
            self._parse(resp.text, collector)
