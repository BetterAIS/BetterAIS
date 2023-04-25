from fastapi import APIRouter, Depends, HTTPException, status
from .models import Login, TokenPair
from better_ais.di.core import core_di

auth_router = APIRouter()

@auth_router.post("/login")
async def login(login_data: Login) -> TokenPair:
    try:
        user = await core_di.controllers.users.get_user(login_data.login, login_data.password)
    except Exception:
        try:
            user = await core_di.controllers.users.create_user(login_data.login, login_data.password)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect login or password",
            )
    access, refresh = await core_di.controllers.authentication.generete_pair(user.id, login_data.login, login_data.password)
    return TokenPair(access=access, refresh=refresh)

@auth_router.post("/refresh")
async def refresh(token: str) -> TokenPair:
    try:
        access, refresh = await core_di.controllers.authentication.use_refresh_token(token)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect token",
        )
    return TokenPair(access=access, refresh=refresh)

@auth_router.post("/revoke")
async def revoke(token: str) -> dict:
    try:
        await core_di.controllers.authentication.revoke_token(token)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect token",
        )
    return {"message": "Token revoked"}

