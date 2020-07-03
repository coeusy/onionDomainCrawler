import redis


class RedisClient:
    def __init__(self):
        self.client = redis.Redis("81.68.126.91", port=63790, db=1)

    def add_domain(self, domain):
        self.client.sadd("darkweb_domain", domain)