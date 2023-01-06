from fastapi import status

from app.api import OpenAPIResponseType
from app.api.errors import ErrorCode, ErrorModel
from app.core.config import settings
from app.security import bearer_transport

pw_min: int = settings.PASSWORD_LENGTH_MIN
pw_max: int = settings.PASSWORD_LENGTH_MAX


# Auth
auth_register_responses: OpenAPIResponseType = {
    status.HTTP_400_BAD_REQUEST: {
        "model": ErrorModel,
        "content": {
            "application/json": {
                "examples": {
                    ErrorCode.USER_ALREADY_EXISTS: {
                        "summary": "A user with this email already exists.",
                        "value": {"detail": ErrorCode.USER_ALREADY_EXISTS},
                    },
                    ErrorCode.USER_PASSWORD_INVALID: {
                        "summary": "Password validation failed.",
                        "value": {
                            "detail": {
                                "code": ErrorCode.USER_PASSWORD_INVALID,
                                "reason": "Password must contain"
                                f"{pw_min} or more characters",
                            }
                        },
                    },
                    ErrorCode.USER_PASSWORD_INVALID: {
                        "summary": "Password validation failed.",
                        "value": {
                            "detail": {
                                "code": ErrorCode.USER_PASSWORD_INVALID,
                                "reason": "Password must contain "
                                f"{pw_max} or less characters",
                            }
                        },
                    },
                }
            }
        },
    },
}

auth_verification_responses: OpenAPIResponseType = {
    status.HTTP_400_BAD_REQUEST: {
        "model": ErrorModel,
        "content": {
            "application/json": {
                "examples": {
                    ErrorCode.USER_ALREADY_VERIFIED: {
                        "summary": "This user email is already verified.",
                        "value": {"detail": ErrorCode.USER_ALREADY_VERIFIED},
                    },
                }
            }
        },
    },
    status.HTTP_401_UNAUTHORIZED: {
        "model": ErrorModel,
        "content": {
            "application/json": {
                "examples": {
                    ErrorCode.BAD_TOKEN_USER: {
                        "summary": "Bad token, token.user_id does not belong current user.id.",
                        "value": {"detail": ErrorCode.BAD_TOKEN_USER},
                    },
                    ErrorCode.USER_NOT_ACTIVE: {
                        "summary": "User not active.",
                        "value": {"detail": ErrorCode.USER_NOT_ACTIVE},
                    },
                }
            }
        },
    },
    status.HTTP_404_NOT_FOUND: {
        "model": ErrorModel,
        "content": {
            "application/json": {
                "examples": {
                    ErrorCode.USER_NOT_FOUND: {
                        "summary": "User not found.",
                        "value": {"detail": ErrorCode.USER_NOT_FOUND},
                    },
                }
            }
        },
    },
}

auth_verification_confirmation_responses: OpenAPIResponseType = {
    status.HTTP_400_BAD_REQUEST: {
        "model": ErrorModel,
        "content": {
            "application/json": {
                "examples": {
                    ErrorCode.USER_ALREADY_VERIFIED: {
                        "summary": "The user is already verified.",
                        "value": {"detail": ErrorCode.USER_ALREADY_VERIFIED},
                    },
                }
            }
        },
    },
    status.HTTP_401_UNAUTHORIZED: {
        "model": ErrorModel,
        "content": {
            "application/json": {
                "examples": {
                    ErrorCode.BAD_TOKEN_USER: {
                        "summary": "Bad token, token.user_id does not belong current user.id.",
                        "value": {"detail": ErrorCode.BAD_TOKEN_USER},
                    },
                    ErrorCode.USER_NOT_ACTIVE: {
                        "summary": "User not active.",
                        "value": {"detail": ErrorCode.USER_NOT_ACTIVE},
                    },
                }
            }
        },
    },
    status.HTTP_404_NOT_FOUND: {
        "model": ErrorModel,
        "content": {
            "application/json": {
                "examples": {
                    ErrorCode.USER_NOT_FOUND: {
                        "summary": "User not found.",
                        "value": {"detail": ErrorCode.USER_NOT_FOUND},
                    },
                }
            }
        },
    },
}

auth_password_forgot_responses: OpenAPIResponseType = {
    status.HTTP_401_UNAUTHORIZED: {
        "model": ErrorModel,
        "content": {
            "application/json": {
                "examples": {
                    ErrorCode.USER_NOT_VERIFIED: {
                        "summary": "User not verified.",
                        "value": {"detail": ErrorCode.USER_NOT_VERIFIED},
                    },
                    ErrorCode.USER_NOT_ACTIVE: {
                        "summary": "User not active.",
                        "value": {"detail": ErrorCode.USER_NOT_ACTIVE},
                    },
                }
            }
        },
    },
    status.HTTP_404_NOT_FOUND: {
        "model": ErrorModel,
        "content": {
            "application/json": {
                "examples": {
                    ErrorCode.USER_NOT_FOUND: {
                        "summary": "User not found.",
                        "value": {"detail": ErrorCode.USER_NOT_FOUND},
                    },
                }
            }
        },
    },
}

auth_password_reset_responses: OpenAPIResponseType = {
    status.HTTP_400_BAD_REQUEST: {
        "model": ErrorModel,
        "content": {
            "application/json": {
                "examples": {
                    ErrorCode.USER_PASSWORD_INVALID: {
                        "summary": "Password validation failed.",
                        "value": {
                            "detail": {
                                "code": ErrorCode.USER_PASSWORD_INVALID,
                                "reason": "Password must contain "
                                f"{pw_min} or more characters",
                            }
                        },
                    },
                    ErrorCode.USER_PASSWORD_INVALID: {
                        "summary": "Password validation failed.",
                        "value": {
                            "detail": {
                                "code": ErrorCode.USER_PASSWORD_INVALID,
                                "reason": "Password must contain "
                                f"{pw_max} or less characters",
                            }
                        },
                    },
                }
            }
        },
    },
    status.HTTP_401_UNAUTHORIZED: {
        "model": ErrorModel,
        "content": {
            "application/json": {
                "examples": {
                    ErrorCode.BAD_TOKEN_USER: {
                        "summary": "Bad token, token.user_id does not belong current user.id.",
                        "value": {"detail": ErrorCode.BAD_TOKEN_USER},
                    },
                    ErrorCode.USER_NOT_VERIFIED: {
                        "summary": "User not verified.",
                        "value": {"detail": ErrorCode.USER_NOT_VERIFIED},
                    },
                    ErrorCode.USER_NOT_ACTIVE: {
                        "summary": "User not active.",
                        "value": {"detail": ErrorCode.USER_NOT_ACTIVE},
                    },
                }
            }
        },
    },
    status.HTTP_404_NOT_FOUND: {
        "model": ErrorModel,
        "content": {
            "application/json": {
                "examples": {
                    ErrorCode.USER_NOT_FOUND: {
                        "summary": "User not found.",
                        "value": {"detail": ErrorCode.USER_NOT_FOUND},
                    },
                }
            }
        },
    },
}

auth_access_responses: OpenAPIResponseType = {
    status.HTTP_400_BAD_REQUEST: {
        "model": ErrorModel,
        "content": {
            "application/json": {
                "examples": {
                    ErrorCode.BAD_CREDENTIALS: {
                        "summary": "Bad credentials or the user is inactive.",
                        "value": {"detail": ErrorCode.BAD_CREDENTIALS},
                    },
                }
            }
        },
    },
    status.HTTP_401_UNAUTHORIZED: {
        "model": ErrorModel,
        "content": {
            "application/json": {
                "examples": {
                    ErrorCode.USER_NOT_VERIFIED: {
                        "summary": "User not verified.",
                        "value": {"detail": ErrorCode.USER_NOT_VERIFIED},
                    },
                }
            }
        },
    },
    **bearer_transport.get_openapi_login_responses_success(),
}

auth_refresh_responses: OpenAPIResponseType = {
    status.HTTP_401_UNAUTHORIZED: {
        "model": ErrorModel,
        "content": {
            "application/json": {
                "examples": {
                    ErrorCode.TOKEN_INVALID: {
                        "summary": "Refresh token invalid.",
                        "value": {"detail": ErrorCode.TOKEN_INVALID},
                    }
                }
            }
        },
    },
    status.HTTP_401_UNAUTHORIZED: {
        "model": ErrorModel,
        "content": {
            "application/json": {
                "examples": {
                    ErrorCode.USER_NOT_VERIFIED: {
                        "summary": "User not verified.",
                        "value": {"detail": ErrorCode.USER_NOT_VERIFIED},
                    },
                }
            }
        },
    },
    status.HTTP_401_UNAUTHORIZED: {
        "model": ErrorModel,
        "content": {
            "application/json": {
                "examples": {
                    ErrorCode.USER_NOT_VERIFIED: {
                        "summary": "User not verified.",
                        "value": {"detail": ErrorCode.USER_NOT_VERIFIED},
                    },
                }
            }
        },
    },
    status.HTTP_404_NOT_FOUND: {
        "model": ErrorModel,
        "content": {
            "application/json": {
                "examples": {
                    ErrorCode.USER_NOT_FOUND: {
                        "summary": "User not found.",
                        "value": {"detail": ErrorCode.USER_NOT_FOUND},
                    },
                }
            }
        },
    },
}

auth_revoke_responses: OpenAPIResponseType = {}

auth_logout_responses: OpenAPIResponseType = {
    status.HTTP_401_UNAUTHORIZED: {
        "model": ErrorModel,
        "content": {
            "application/json": {
                "examples": {
                    ErrorCode.TOKEN_INVALID: {
                        "summary": "Access token invalid.",
                        "value": {"detail": ErrorCode.TOKEN_INVALID},
                    }
                }
            }
        },
    },
    status.HTTP_404_NOT_FOUND: {
        "model": ErrorModel,
        "content": {
            "application/json": {
                "examples": {
                    ErrorCode.USER_NOT_FOUND: {
                        "summary": "User not found.",
                        "value": {"detail": ErrorCode.USER_NOT_FOUND},
                    },
                }
            }
        },
    },
    **bearer_transport.get_openapi_logout_responses_success(),
}

# Users
get_user_or_404_responses: OpenAPIResponseType = {
    status.HTTP_401_UNAUTHORIZED: {
        "model": ErrorModel,
        "content": {
            "application/json": {
                "examples": {
                    ErrorCode.USER_NOT_VERIFIED: {
                        "summary": "User not verified.",
                        "value": {"detail": ErrorCode.USER_NOT_VERIFIED},
                    },
                    ErrorCode.USER_NOT_ACTIVE: {
                        "summary": "User not active.",
                        "value": {"detail": ErrorCode.USER_NOT_ACTIVE},
                    },
                    ErrorCode.TOKEN_INVALID: {
                        "summary": "Access token invalid.",
                        "value": {"detail": ErrorCode.TOKEN_INVALID},
                    },
                }
            }
        },
    },
    status.HTTP_404_NOT_FOUND: {
        "model": ErrorModel,
        "content": {
            "application/json": {
                "examples": {
                    ErrorCode.USER_NOT_FOUND: {
                        "summary": "User not found.",
                        "value": {"detail": ErrorCode.USER_NOT_FOUND},
                    },
                }
            }
        },
    },
}

update_user_me_responses: OpenAPIResponseType = {
    status.HTTP_400_BAD_REQUEST: {
        "model": ErrorModel,
        "content": {
            "application/json": {
                "examples": {
                    ErrorCode.USER_ALREADY_EXISTS: {
                        "summary": "A user with this email already exists.",
                        "value": {"detail": ErrorCode.USER_ALREADY_EXISTS},
                    },
                    ErrorCode.USER_PASSWORD_INVALID: {
                        "summary": "Password validation failed.",
                        "value": {
                            "detail": {
                                "code": ErrorCode.USER_PASSWORD_INVALID,
                                "reason": "Password must contain"
                                f"{pw_min} or more characters",
                            }
                        },
                    },
                    ErrorCode.USER_PASSWORD_INVALID: {
                        "summary": "Password validation failed.",
                        "value": {
                            "detail": {
                                "code": ErrorCode.USER_PASSWORD_INVALID,
                                "reason": "Password must contain "
                                f"{pw_max} or less characters",
                            }
                        },
                    },
                }
            }
        },
    },
    status.HTTP_401_UNAUTHORIZED: {
        "model": ErrorModel,
        "content": {
            "application/json": {
                "examples": {
                    ErrorCode.USER_NOT_VERIFIED: {
                        "summary": "User not verified.",
                        "value": {"detail": ErrorCode.USER_NOT_VERIFIED},
                    },
                    ErrorCode.USER_NOT_ACTIVE: {
                        "summary": "User not active.",
                        "value": {"detail": ErrorCode.USER_NOT_ACTIVE},
                    },
                    ErrorCode.TOKEN_INVALID: {
                        "summary": "Access token invalid.",
                        "value": {"detail": ErrorCode.TOKEN_INVALID},
                    },
                }
            }
        },
    },
    status.HTTP_404_NOT_FOUND: {
        "model": ErrorModel,
        "content": {
            "application/json": {
                "examples": {
                    ErrorCode.USER_NOT_FOUND: {
                        "summary": "User not found.",
                        "value": {"detail": ErrorCode.USER_NOT_FOUND},
                    },
                }
            }
        },
    },
}

get_all_users_responses: OpenAPIResponseType = {
    status.HTTP_401_UNAUTHORIZED: {
        "model": ErrorModel,
        "content": {
            "application/json": {
                "examples": {
                    ErrorCode.USER_NOT_VERIFIED: {
                        "summary": "User not verified.",
                        "value": {"detail": ErrorCode.USER_NOT_VERIFIED},
                    },
                    ErrorCode.USER_NOT_ACTIVE: {
                        "summary": "User not active.",
                        "value": {"detail": ErrorCode.USER_NOT_ACTIVE},
                    },
                    ErrorCode.TOKEN_INVALID: {
                        "summary": "Access token invalid.",
                        "value": {"detail": ErrorCode.TOKEN_INVALID},
                    },
                }
            }
        },
    },
    status.HTTP_403_FORBIDDEN: {
        "model": ErrorModel,
        "content": {
            "application/json": {
                "examples": {
                    ErrorCode.USER_FORBIDDEN: {
                        "summary": "Forbidden.",
                        "value": {"detail": ErrorCode.USER_FORBIDDEN},
                    },
                }
            }
        },
    },
    status.HTTP_404_NOT_FOUND: {
        "model": ErrorModel,
        "content": {
            "application/json": {
                "examples": {
                    ErrorCode.USER_NOT_FOUND: {
                        "summary": "User not found.",
                        "value": {"detail": ErrorCode.USER_NOT_FOUND},
                    },
                }
            }
        },
    },
}

get_user_reponses: OpenAPIResponseType = {
    status.HTTP_401_UNAUTHORIZED: {
        "model": ErrorModel,
        "content": {
            "application/json": {
                "examples": {
                    ErrorCode.USER_NOT_VERIFIED: {
                        "summary": "User not verified.",
                        "value": {"detail": ErrorCode.USER_NOT_VERIFIED},
                    },
                    ErrorCode.USER_NOT_ACTIVE: {
                        "summary": "User not active.",
                        "value": {"detail": ErrorCode.USER_NOT_ACTIVE},
                    },
                    ErrorCode.TOKEN_INVALID: {
                        "summary": "Access token invalid.",
                        "value": {"detail": ErrorCode.TOKEN_INVALID},
                    },
                }
            }
        },
    },
    status.HTTP_403_FORBIDDEN: {
        "model": ErrorModel,
        "content": {
            "application/json": {
                "examples": {
                    ErrorCode.USER_FORBIDDEN: {
                        "summary": "Forbidden.",
                        "value": {"detail": ErrorCode.USER_FORBIDDEN},
                    },
                }
            }
        },
    },
    status.HTTP_404_NOT_FOUND: {
        "model": ErrorModel,
        "content": {
            "application/json": {
                "examples": {
                    ErrorCode.USER_NOT_FOUND: {
                        "summary": "User not found.",
                        "value": {"detail": ErrorCode.USER_NOT_FOUND},
                    },
                }
            }
        },
    },
}

update_user_responses: OpenAPIResponseType = {
    status.HTTP_400_BAD_REQUEST: {
        "model": ErrorModel,
        "content": {
            "application/json": {
                "examples": {
                    ErrorCode.USER_ALREADY_EXISTS: {
                        "summary": "A user with this email already exists.",
                        "value": {"detail": ErrorCode.USER_ALREADY_EXISTS},
                    },
                    ErrorCode.USER_PASSWORD_INVALID: {
                        "summary": "Password validation failed.",
                        "value": {
                            "detail": {
                                "code": ErrorCode.USER_PASSWORD_INVALID,
                                "reason": "Password must contain"
                                f"{pw_min} or more characters",
                            }
                        },
                    },
                    ErrorCode.USER_PASSWORD_INVALID: {
                        "summary": "Password validation failed.",
                        "value": {
                            "detail": {
                                "code": ErrorCode.USER_PASSWORD_INVALID,
                                "reason": "Password must contain "
                                f"{pw_max} or less characters",
                            }
                        },
                    },
                }
            }
        },
    },
    status.HTTP_401_UNAUTHORIZED: {
        "model": ErrorModel,
        "content": {
            "application/json": {
                "examples": {
                    ErrorCode.USER_NOT_VERIFIED: {
                        "summary": "User not verified.",
                        "value": {"detail": ErrorCode.USER_NOT_VERIFIED},
                    },
                    ErrorCode.USER_NOT_ACTIVE: {
                        "summary": "User not active.",
                        "value": {"detail": ErrorCode.USER_NOT_ACTIVE},
                    },
                    ErrorCode.TOKEN_INVALID: {
                        "summary": "Access token invalid.",
                        "value": {"detail": ErrorCode.TOKEN_INVALID},
                    },
                }
            }
        },
    },
    status.HTTP_403_FORBIDDEN: {
        "model": ErrorModel,
        "content": {
            "application/json": {
                "examples": {
                    ErrorCode.USER_FORBIDDEN: {
                        "summary": "Forbidden.",
                        "value": {"detail": ErrorCode.USER_FORBIDDEN},
                    },
                }
            }
        },
    },
    status.HTTP_404_NOT_FOUND: {
        "model": ErrorModel,
        "content": {
            "application/json": {
                "examples": {
                    ErrorCode.USER_NOT_FOUND: {
                        "summary": "User not found.",
                        "value": {"detail": ErrorCode.USER_NOT_FOUND},
                    },
                }
            }
        },
    },
}

delete_user_responses: OpenAPIResponseType = {
    status.HTTP_401_UNAUTHORIZED: {
        "model": ErrorModel,
        "content": {
            "application/json": {
                "examples": {
                    ErrorCode.USER_NOT_VERIFIED: {
                        "summary": "User not verified.",
                        "value": {"detail": ErrorCode.USER_NOT_VERIFIED},
                    },
                    ErrorCode.USER_NOT_ACTIVE: {
                        "summary": "User not active.",
                        "value": {"detail": ErrorCode.USER_NOT_ACTIVE},
                    },
                    ErrorCode.TOKEN_INVALID: {
                        "summary": "Access token invalid.",
                        "value": {"detail": ErrorCode.TOKEN_INVALID},
                    },
                }
            }
        },
    },
    status.HTTP_403_FORBIDDEN: {
        "model": ErrorModel,
        "content": {
            "application/json": {
                "examples": {
                    ErrorCode.USER_FORBIDDEN: {
                        "summary": "Forbidden.",
                        "value": {"detail": ErrorCode.USER_FORBIDDEN},
                    },
                }
            }
        },
    },
    status.HTTP_404_NOT_FOUND: {
        "model": ErrorModel,
        "content": {
            "application/json": {
                "examples": {
                    ErrorCode.USER_NOT_FOUND: {
                        "summary": "User not found.",
                        "value": {"detail": ErrorCode.USER_NOT_FOUND},
                    },
                }
            }
        },
    },
}
