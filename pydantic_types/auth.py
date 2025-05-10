from pydantic import BaseModel


class VerifyOTPBody(BaseModel):
    sessionJwt: str
    email: str


class VerifyOTPResponse(BaseModel):
    message: str


class AuthMeResponse(BaseModel):
    email: str
    role: str
