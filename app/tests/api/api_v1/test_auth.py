import pytest

pytestmark = pytest.mark.asyncio


"""
async def test_get_superuser_access_token(client: AsyncClient) -> None:
    r = await client.post(
        "auth/jwt/login",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={
            "username": settings.FIRST_SUPERUSER,
            "password": settings.FIRST_SUPERUSER_PASSWORD,
        }
    )
    tokens = r.json()
    assert r.status_code == 200
    assert "access_token" in tokens
    assert tokens["access_token"]


async def test_verify_access_token(
    client: AsyncClient,
    token_headers_from_email: Dict[str, str]
) -> None:
    rtok = await client.post(
        "auth/jwt/login",
        data={
            "email": settings.FIRST_SUPERUSER,
            "password": settings.FIRST_SUPERUSER_PASSWORD,
        }
    )
    assert rtok.status_code == 200
    tokens = rtok.json()
    access_token = tokens["access_token"]
    r = await client.post(
        "auth/verify",
        data={"token": access_token}
    )
    result = r.json()
    assert r.status_code == 200
    assert "email" in result
"""
