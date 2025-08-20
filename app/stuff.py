from redis import Redis
from core import config

cache = Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_DB,
)


def main():
    cache.set("foo", "bar")
    cache.set("bob", "Dilan")
    print(cache.keys())
    print(cache.get("foo"))
    print(cache.get("bob"))


if __name__ == "__main__":
    main()
