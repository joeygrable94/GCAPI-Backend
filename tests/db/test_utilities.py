from app.db.utilities import hash_url


def test_hash_url() -> None:
    test_url = hash_url("https://www.google.com")
    assert len(test_url) == 64
