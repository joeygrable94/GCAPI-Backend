from app.core.redis import redis_conn


def test_redis_connected() -> None:
    assert redis_conn.ping()
