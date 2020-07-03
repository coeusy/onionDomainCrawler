from baseEngine import *


class TorchSearch(SearchEngine):
    def __init__(self):
        super().__init__()
        self.url = "http://xmh57jrzrnw6insl.onion"

    def search(self, keyword: str):
        collector = set()
        base_url = f"{self.url}/4a1f6b371c/search.cgi?s=DRP&q={keyword.replace(' ', '+')}&cmd=Search!"
        for i in range(100):
            url = f"{base_url}&np={i}"
            resp = self._get(url)
            self._parse(resp.text, collector)

