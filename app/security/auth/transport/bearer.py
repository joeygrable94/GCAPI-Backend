from typing import Any, Optional

from fastapi import Response, status
from fastapi.security import OAuth2PasswordBearer

from app.api import OpenAPIResponseType
from app.db.schemas import BearerResponse


class BearerTransport:
    scheme: OAuth2PasswordBearer

    def __init__(self, tokenUrl: str):
        self.scheme = OAuth2PasswordBearer(tokenUrl, auto_error=False)

    async def get_login_response(
        self,
        access_token: str,
        access_token_csrf: Optional[str],
        refresh_token: Optional[str],
        refresh_token_csrf: Optional[str],
        response: Response,
    ) -> Any:
        return BearerResponse(
            token_type="bearer",
            access_token=access_token,
            access_token_csrf=access_token_csrf,
            refresh_token=refresh_token,
            refresh_token_csrf=refresh_token_csrf,
        )

    async def get_logout_response(self, response: Response) -> Any:
        return BearerResponse(
            token_type="bearer",
            access_token="",
            access_token_csrf="",
            refresh_token="",
            refresh_token_csrf="",
        )

    @staticmethod
    def get_openapi_login_responses_success() -> OpenAPIResponseType:
        return {
            status.HTTP_200_OK: {
                "model": BearerResponse,
                "content": {
                    "application/json": {
                        "example": {
                            "token_type": "bearer",
                            "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoiYWNjZXNzIiwiaXNzIjoiR0NBUEkiLCJuYmYiOjE2NjQ1MTMyNTMsImlhdCI6MTY2NDUxMzI1MywianRpIjoiMWZmM2VkYzItNThmYS00MTA3LTk2YjItOGJkZGI4MmI5YTBhIiwic3ViIjoiMWZlMTE3Y2QtMzhiMy00NzhiLWEzYTktNWQ3NTBmZTIxNmI0IiwiYXVkIjpbImF1dGg6YWNjZXNzIl0sImV4cCI6MTY2NDUxNjg1MywiZnJlc2giOnRydWUsImNzcmYiOiI4ZmM2M2U5My0zZDc2LTQ3OWYtODU4OC1iZjI0NzViMjIwMzQifQ.yLW5X9SDaxVCgjPuu-dBapH5Wjzv9qnh4Fdqz0tO5Ls",  # allowinsecure  # noqa: E501
                            "access_token_csrf": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9",  # allowinsecure  # noqa: E501
                            "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoicmVmcmVzaCIsImlzcyI6IkdDQVBJIiwibmJmIjoxNjY0NTEzMjU0LCJpYXQiOjE2NjQ1MTMyNTQsImp0aSI6IjZiNWE0N2QxLTQ4YTQtNGVmMi1iMDdkLWQ3YmU4MzkwODhmMyIsInN1YiI6IjFmZTExN2NkLTM4YjMtNDc4Yi1hM2E5LTVkNzUwZmUyMTZiNCIsImF1ZCI6WyJhdXRoOnJlZnJlc2giXSwiZXhwIjoxNjY0NTk5NjU0LCJjc3JmIjoiZWQzMzA2ZTgtNGQ4Mi00MTg5LTgxZTQtMjhhNDA5MmRmMWE3In0.9pOEvAbHBZaQyPvgEt2UY3hqeV2TO0NCVmyHbRoTCfw",  # allowinsecure  # noqa: E501
                            "refresh_token_csrf": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9",  # allowinsecure  # noqa: E501
                        }
                    }
                },
            },
        }

    @staticmethod
    def get_openapi_logout_responses_success() -> OpenAPIResponseType:
        return {
            status.HTTP_200_OK: {
                "model": BearerResponse,
                "content": {
                    "application/json": {
                        "example": {
                            "access_token": "",  # allowinsecure  # noqa: E501
                            "refresh_token": "",  # allowinsecure  # noqa: E501
                            "token_type": "bearer",
                        }
                    }
                },
            },
        }
