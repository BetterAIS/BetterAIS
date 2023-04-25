from fastapi import APIRouter, Depends, HTTPException, status
from .auth.endpoints import auth_router
from .ais.endpoints import ais_router
from .accommodation.endpoints import acc_router

api_router = APIRouter()

api_router.include_router(auth_router, prefix="/auth")
api_router.include_router(ais_router, prefix="/ais")
api_router.include_router(acc_router, prefix="/accommodation")

