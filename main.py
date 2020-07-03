from engines import *
from Utils.utils import load_keywords
from concurrent.futures import ThreadPoolExecutor


if __name__ == '__main__':
    pool = ThreadPoolExecutor(max_workers=4)
    torch = TorchSearch()
    haystak = HaystakSearch()
    ahmia = AhmiaSearch()
    not_evil = NotEvilSearch()
    # torch.search(".onion")
    for keyword in load_keywords():
        pool.submit(torch.search, keyword)
        pool.submit(haystak.search, keyword)
        pool.submit(ahmia.search, keyword)
        pool.submit(not_evil.search, keyword)
