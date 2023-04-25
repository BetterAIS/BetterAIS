from better_ais.di.core import core_di
from better_ais.controllers.users import UsersController, Mail, Document, Homework, TimeTable
from better_ais.controllers.authentication import AuthenticationController, TokenData
from fastapi import APIRouter, Depends, HTTPException, status

ais_router = APIRouter()

@ais_router.get("/mails/new")
async def get_new_mails(token_payload: TokenData = Depends(core_di.controllers.authentication.get_token_payload)) -> list[Mail]:
    try:
        return await core_di.controllers.users.get_user_new_mails(token_payload.login, token_payload.password)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect token",
        )

@ais_router.get("/mails")
async def get_mails(token_payload: TokenData = Depends(core_di.controllers.authentication.get_token_payload)) -> list[Mail]:
    try:
        return await core_di.controllers.users.get_user_mails(token_payload.login, token_payload.password)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect token",
        )


@ais_router.get("/documents/new")
async def get_new_documents(token_payload: TokenData = Depends(core_di.controllers.authentication.get_token_payload)) -> list[Document]:
    try:
        return await core_di.controllers.users.get_user_new_documents(token_payload.login, token_payload.password)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect token",
        )


@ais_router.get("/documents")
async def get_documents(token_payload: TokenData = Depends(core_di.controllers.authentication.get_token_payload)) -> list[Document]:
    try:
        return await core_di.controllers.users.get_user_documents(token_payload.login, token_payload.password)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect token",
        )

@ais_router.get("/homeworks")
async def get_homeworks(token_payload: TokenData = Depends(core_di.controllers.authentication.get_token_payload)) -> list[Homework]:
    try:
        return await core_di.controllers.users.get_user_homeworks(token_payload.login, token_payload.password)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect token",
        )

@ais_router.get("/time-table")
async def get_time_table(token_payload: TokenData = Depends(core_di.controllers.authentication.get_token_payload)) -> list[TimeTable]:
    try:
        return await core_di.controllers.users.get_user_time_table(token_payload.login, token_payload.password)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect token",
        )