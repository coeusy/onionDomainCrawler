import redis


class RedisClient:
    def __init__(self, host, port: int, db: int):
        self.client = redis.Redis(host, port=port, db=db, decode_responses=True)
        self.ping()

    def ping(self):
        if not self.client.ping():
            raise redis.exceptions.ConnectionError

    def add_domain(self, domain):
        self.client.sadd("darkweb_domain", domain)
