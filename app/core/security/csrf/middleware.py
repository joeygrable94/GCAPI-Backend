import uuid
from typing import Any

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import PlainTextResponse


class CSRFMiddleware(BaseHTTPMiddleware):
    """Middleware to add CSRF protection to requests.

    This middleware will add a CSRF cookie to all responses, and it will check
    that cookie on all non-safe requests. If the cookie is missing or doesn't
    match the header, the request will be rejected with a 403 Forbidden error.

    1. Add this middleware using the middleware= parameter of your app.
    2. request.state.csrf_token will now be available.
    3. Use directly in an HTML <form> POST with
       `<input type="hidden" name="csrf_token" value="{{ csrf_token }}" />`
    4. Use with javascript / ajax POST by sending a request header `csrf_token`
       with request.state.csrf_token

    Notes

    - Users must should start on a "safe page" (a typical GET request) to
      generate the initial CSRF cookie.
    - Token is stored in request.state.csrf_token for use in templates.

    """

    async def dispatch(self, request: Any, call_next: Any) -> Any:
        CSRF_TOKEN_NAME = "csrf_token"

        # Valid for 10 days before regeneration.
        CSRF_TOKEN_EXPIRY = 10 * 24 * 60 * 60
        # Always available even if we don't get it from cookie.
        request.state.csrf_token = ""

        token_new_cookie = False
        token_from_cookie = request.cookies.get(CSRF_TOKEN_NAME, None)
        token_from_header = request.headers.get(CSRF_TOKEN_NAME, None)
        if hasattr(request.state, "post"):
            token_from_post = request.state.post.get(CSRF_TOKEN_NAME, None)

        # 🍪 Fetch the cookie only if we're using an appropriate request method.
        if request.method not in ("GET", "HEAD", "OPTIONS", "TRACE"):
            # Sanity check. UUID always > 30.
            if not token_from_cookie or len(token_from_cookie) < 30:
                # 🔴 Fail check.
                return PlainTextResponse("No CSRF cookie set!", status_code=403)
            # 🔴 Fail check.
            if (str(token_from_cookie) != str(token_from_post)) and (
                str(token_from_cookie) != str(token_from_header)
            ):  # noqa: E501
                return PlainTextResponse("CSRF cookie does not match!", status_code=403)
        else:
            # 🍪 Generates the cookie if one does not exist.
            # Has to be the same token throughout session! NOT a nonce.
            if not token_from_cookie:
                token_from_cookie = str(uuid.uuid4())
                token_new_cookie = True

        # 🟢 All good. Pass csrf_token up to controllers, templates.
        request.state.csrf_token = token_from_cookie

        # ⏰ Wait for response to happen.
        response = await call_next(request)

        # 🍪 Set CSRF cookie on the response.
        if token_new_cookie and token_from_cookie:
            response.set_cookie(
                CSRF_TOKEN_NAME,
                token_from_cookie,
                CSRF_TOKEN_EXPIRY,
                path="/",
                domain=None,
                secure=False,
                httponly=False,
                samesite="strict",
            )

        return response
