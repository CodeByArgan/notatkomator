
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException
import uuid
import jwt

from descope_client import descope_client
from services.audit_log import audit_log_service
from models.role import Role
from models.user import User
from settings import env_settings
from utils.logger import logger


class AuthService():

    async def verify_otp(self, session_token: str, user_email: str):
        await audit_log_service.create_new(
            username="SYSTEM", details=f"User with email {user_email} tries to log in.")

        if not session_token:
            raise HTTPException(401, detail="No descope token")
        try:
            session = descope_client.validate_session(
                session_token=session_token)
            descope_user_id = session["userId"]

            role = await Role.get(name="user")
            user, _ = await User.get_or_create(
                descope_user_id=descope_user_id,
                defaults={"email": user_email, "role": role}
            )

            refresh_token = await auth_service.create_refresh_token(str(user.id))

            await audit_log_service.create_new(
                username="SYSTEM", details=f"User with email {user_email} successfully logged in.")
            return refresh_token

        except Exception as e:
            logger.error(e)
            await audit_log_service.create_new(
                username="SYSTEM", details=f"User with email {user_email} error with login {e}")
            raise HTTPException(
                401, detail="Error with descope session, try again")

    @staticmethod
    async def decode_refresh_token(token: str) -> str:
        try:
            payload = jwt.decode(
                token, env_settings.refresh_secret, algorithms=["HS256"])
            return payload["user_id"]
        except jwt.ExpiredSignatureError:
            logger.error("Error - token expired")
            raise HTTPException(status_code=401, detail="Token expired")
        except jwt.InvalidTokenError:
            logger.error("Error - token invalid")
            raise HTTPException(status_code=401, detail="Invalid token")

    @staticmethod
    async def create_refresh_token(user_id: str) -> str:
        payload = {
            "user_id": user_id,
            "exp": datetime.now(timezone.utc) + timedelta(days=env_settings.refresh_token_expire_days),
            "jti": str(uuid.uuid4()),
            "iat": datetime.now(timezone.utc),
        }
        return jwt.encode(payload, env_settings.refresh_secret, algorithm="HS256")


auth_service = AuthService()
