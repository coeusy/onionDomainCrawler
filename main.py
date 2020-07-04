from engines import *
from Utils.utils import load_keywords
from configure import *
from multiprocessing import Process


if __name__ == '__main__':
    redis = RedisClient(**REDIS)
    torch = TorchSearch(redis)
    haystak = HaystakSearch(redis)
    ahmia = AhmiaSearch(redis)
    not_evil = NotEvilSearch(redis)
    # torch.search(".onion")
    threads = []
    for engine in [torch, haystak, ahmia, not_evil]:
        t = Process(target=engine.run, args=(load_keywords,))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
