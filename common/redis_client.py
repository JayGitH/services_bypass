import os, json

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
        self.__session = redis.Redis(
            connection_pool=redis.ConnectionPool.from_url(self.redis_url, decode_responses=True)
        )

    def set(self, key, value: dict, ex=None):
        self.__session.set(
            key,
            json.dumps(value, ensure_ascii=False),
            ex=(ex or self.default_ex),
        )

    def get(self, key, empty=None):
        result = self.__session.get(key)
        if result is None:
            return empty
        return json.loads(result)

    def delete(self, key):
        try:
            self.__session.delete(key)
        except Exception as e:
            print(e)
