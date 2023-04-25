from better_ais.di.core import core_di
from better_ais.controllers.users import UsersController, AccUser
from better_ais.controllers.authentication import AuthenticationController, TokenData
from fastapi import APIRouter, Depends, HTTPException, status

acc_router = APIRouter()

@acc_router.get("/get_all")
async def get_mail(token_payload: TokenData = Depends(core_di.controllers.authentication.get_token_payload)) -> AccUser:
    try:
        return await core_di.controllers.users.get_user_accommodation(token_payload.login, token_payload.password)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect token",
        )