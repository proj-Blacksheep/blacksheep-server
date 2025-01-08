from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from src.services.login import create_access_token, authenticate_user


router = APIRouter(tags=["login"])


@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Authenticate user and create access token.

    Args:
        form_data: OAuth2 password request form containing username and password.

    Returns:
        dict: Access token and user role.

    Raises:
        HTTPException: If authentication fails.
    """
    # 여기서 사용자 검증 로직 구현
    user = await authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # JWT 토큰 생성
    access_token = create_access_token(data={"sub": user.username})

    return {"access_token": access_token, "role": user.role}
