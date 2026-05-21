from datetime import datetime, timedelta
from http import HTTPStatus
from zoneinfo import ZoneInfo
from alembic.util import exc
from fastapi import Depends, HTTPException
from jwt import DecodeError, encode, decode
import jwt
from pwdlib import PasswordHash
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from MyPom.core.database import User, get_db
import re


SECRET_KEY = "12345_PROVISORIO"
ALGORITHM = "HS256"
ACESS_TOKEN_EXPIRE_MINUTS = 30

oauth2_schema = OAuth2PasswordBearer(tokenUrl="token")


def create_acess_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(tz=ZoneInfo("UTC")) + timedelta(
        minutes=ACESS_TOKEN_EXPIRE_MINUTS
    )
    to_encode.update({"exp": expire})
    encode_jwt = encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt


def get_password_hash(password: str):
    return PasswordHash.recommended().hash(password)


def verify_password_hash(plain_password: str, hashed_password: str):
    return PasswordHash.recommended().verify(plain_password, hashed_password)


def email_pattern(email):
    pattern = r"^[a-zA-Z0-9._-]+@[a-zA-Z0-9]+\.[a-zA-Z\.a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))


def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_schema),
):
    credencials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")

        if not username:
            raise credencials_exception

    except DecodeError:
        raise credencials_exception

    except jwt.exceptions.ExpiredSignatureError:
        raise credencials_exception

    user = db.query(User).filter_by(username=username).first()

    if not user:
        raise credencials_exception

    return user
