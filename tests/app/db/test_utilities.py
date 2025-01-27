from app.db.utilities import hash_url


def test_hash_url():
    url = "https://example.com/some/path?utm_source=google"
    hashed = hash_url(url)

    assert len(hashed) == 64
    assert isinstance(hashed, str)

    assert hashed == hash_url(url)
    assert hashed != hash_url(url + "&extra_param=test")
