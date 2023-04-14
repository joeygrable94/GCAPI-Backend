from typing import Any, Dict, Union

from fastapi import status

from app.api.errors import ErrorCode, ErrorModel

OpenAPIResponseType: Any = Dict[Union[int, str], Dict[str, Any]]


# Clients
clients_read_responses: OpenAPIResponseType = {
    status.HTTP_404_NOT_FOUND: {
        "model": ErrorModel,
        "content": {
            "application/json": {
                "examples": {
                    ErrorCode.CLIENT_NOT_FOUND: {
                        "summary": "A client with that name was not found.",
                        "value": {"detail": ErrorCode.CLIENT_NOT_FOUND},
                    },
                }
            }
        },
    },
}
