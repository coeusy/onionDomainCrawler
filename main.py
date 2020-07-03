from engines import *
from Utils.utils import load_keywords
from configure import *
from concurrent.futures import ThreadPoolExecutor


if __name__ == '__main__':
    redis = RedisClient(**REDIS)
    pool = ThreadPoolExecutor(max_workers=4)
    torch = TorchSearch(redis)
    haystak = HaystakSearch(redis)
    ahmia = AhmiaSearch(redis)
    not_evil = NotEvilSearch(redis)
    # torch.search(".onion")
    pool.submit(torch.run, load_keywords)
    pool.submit(haystak.run, load_keywords)
    pool.submit(ahmia.run, load_keywords)
    pool.submit(not_evil.run, load_keywords)
