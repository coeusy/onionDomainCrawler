from SearchEngines.engines import *
from configure import *
from multiprocessing import Process
from Databases.redisClient import RedisClient


if __name__ == '__main__':
    redis = RedisClient(**REDIS)
    torch = TorchSearch(redis)
    haystak = HaystakSearch(redis)
    ahmia = AhmiaSearch(redis)
    not_evil = NotEvilSearch(redis)
    processes = []
    for engine in [torch, haystak, ahmia, not_evil]:
        p = Process(target=engine.run)
        p.start()
        processes.append(p)
    for p in processes:
        p.join()
