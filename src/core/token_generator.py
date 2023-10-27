import datetime

from schemas import TokenSchema
from jose import jwt
from .config import ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM


class TokenGenerator:
    @staticmethod
    def _generate_token(data: dict, token_expire: int) -> str:
        data.update({"exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=token_expire)})
        return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

    @staticmethod
    def create_access_token(data: dict) -> TokenSchema:
        to_encode = data.copy()
        to_encode["token_type"] = "access"
        token = TokenGenerator._generate_token(to_encode, ACCESS_TOKEN_EXPIRE_MINUTES)
        return TokenSchema(token=token, token_type="bearer")

    @staticmethod
    def create_refresh_token(data: dict) -> TokenSchema:
        to_encode = data.copy()
        to_encode["token_type"] = "refresh"
        token = TokenGenerator._generate_token(to_encode, REFRESH_TOKEN_EXPIRE_MINUTES)
        return TokenSchema(token=token, token_type="bearer")

    @staticmethod
    def decode_token(token: str):
        try:
            encoded_jwt = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        except jwt.JWSError:
            return None
        return encoded_jwt
