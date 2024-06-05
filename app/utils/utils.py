from fastapi import HTTPException, status


def get_user_exception():
    return HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="could not validate user",
                headers={"WWW-Authenticate": "Bearer"}
            )

def permission_exception():
    return HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Not enough privilages(permission)"
    )

def token_exception():
    token_exception_response = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail = "Incorrect email or password",
        headers = {"WWW-Authenticate": "Bearer"}
    )
    return token_exception_response

def no_such_waiter_exception():
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="No such waiter found"
    )


