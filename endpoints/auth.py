import os
from fastapi import APIRouter, Depends, Response

from settings import env_settings
from models.user import User
from pydantic_types.auth import AuthMeResponse, VerifyOTPBody, VerifyOTPResponse
from services.auth import auth_service
from utils.logger import logger
from utils.auth import get_current_user


auth_router = APIRouter(prefix='/auth')


@auth_router.post(
    "/verify-otp",
    tags=["auth"],
    description="Method that validate OTP descope sessions, and creates cookies",
    response_model=VerifyOTPResponse
)
async def verify_otp(request: VerifyOTPBody, response: Response):
    refresh_token = await auth_service.verify_otp(request.sessionJwt, request.email)
    response.set_cookie(
        env_settings.refresh_cookie_name,
        refresh_token,
        httponly=True,
        max_age=60 * 60 * 24 * env_settings.refresh_token_expire_days,
        secure=False,
        samesite="strict"
    )

    return {"message": "ok"}


@auth_router.get(
    "/me",
    tags=["auth"],
    description="Method that returns user info if sessions is valid",
    response_model=AuthMeResponse
)
async def get_me(user: User = Depends(get_current_user)):
    return {"email": user.email, "role": user.role.name}


@auth_router.get(
    "/logout",
    tags=["auth"],
    description="Method that logout user",
)
async def logout(response: Response, user: User = Depends(get_current_user)):
    response.delete_cookie(
        env_settings.refresh_cookie_name,
        httponly=True,
        secure=False,
        samesite="strict"
    )

    return {"message": "ok"}


if os.getenv("ENV") == "dev":
    @auth_router.get(
        "/login-docs",
        tags=["auth"],
        description="Method that add httpCookie to swagger docs - should be visible only on ENV == dev",
    )
    async def login_docs(response: Response,):
        refresh_token = await auth_service.create_refresh_token(str(env_settings.test_user_uuid))
        response.set_cookie(
            env_settings.refresh_cookie_name,
            refresh_token,
            httponly=True,
            max_age=60 * 60 * 24 * env_settings.refresh_token_expire_days,
            secure=False,
            samesite="strict"
        )

        return {"message": "ok"}