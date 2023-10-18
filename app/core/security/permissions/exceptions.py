from fastapi import HTTPException, status

# the exception that will be raised, if no sufficient permissions are found
# can be configured in the configure_permissions() function
permission_exception = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Insufficient permissions",
    headers={"WWW-Authenticate": "Bearer"},
)
