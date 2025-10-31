from redis import Redis

from core import config

cache = Redis(
    host=config.settings.redis.connection.host,
    port=config.settings.redis.connection.port,
    db=config.settings.redis.db.db,
)


def main() -> None:
    cache.set("foo", "bar")
    cache.set("bob", "Dilan")
    print(cache.keys())
    print(cache.get("foo"))
    print(cache.get("bob"))
    print(cache.get("bob"))


if __name__ == "__main__":
    main()
