import os

import redis


class RedisPoolSession:
    __instance = None
    redis_url = os.getenv('REDIS_URL')
    default_ex = 180

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def __init__(self):
        self.session = redis.Redis(
            connection_pool=redis.ConnectionPool.from_url(self.redis_url, decode_responses=True)
        )
