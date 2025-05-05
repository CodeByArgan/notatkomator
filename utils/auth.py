from fastapi import HTTPException, Request, Response
from tortoise.exceptions import DoesNotExist

from utils.logger import logger
from settings import env_settings
from services.auth import auth_service
from models.user import User


async def get_current_user(request: Request, response: Response) -> User:
    token = request.cookies.get(env_settings.refresh_cookie_name)
    if not token:
        raise HTTPException(status_code=401, detail="No descope token")

    try:
        user_id = await auth_service.decode_refresh_token(token)
        user = await User.get(id=user_id).prefetch_related("role")
        if user.is_banned:
            logger.error(f'User {user.email} is banned.')
            raise HTTPException(status_code=403, detail="Banned user")
        return user
    except (DoesNotExist, HTTPException) as e:
        response.delete_cookie(
            env_settings.refresh_cookie_name,
            httponly=True,
            secure=False,
            samesite="strict"
        )
        logger.error(f'Error: {e}')
        raise HTTPException(status_code=401, detail="No user in database")
    except Exception as e:
        response.delete_cookie(
            env_settings.refresh_cookie_name,
            httponly=True,
            secure=False,
            samesite="strict"
        )
        logger.error(f'Error: {e}')
        raise HTTPException(status_code=401, detail="Invalid token")
