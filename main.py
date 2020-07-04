from SearchEngines.engines import *
from multiprocessing import Process
from Databases.redisClient import RedisClient
cfg = ConfigLoader().config_dict['main']


if __name__ == '__main__':
    redis = RedisClient(**cfg['redis'])
    torch = TorchSearch(redis)
    haystak = HaystakSearch(redis)
    ahmia = AhmiaSearch(redis)
    not_evil = NotEvilSearch(redis)
    processes = []
    for engine in [torch, haystak, not_evil]:
        p = Process(target=engine.run)
        p.start()
        processes.append(p)
    for p in processes:
        p.join()
