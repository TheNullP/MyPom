from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from MyPom.core.database import User, get_db
from MyPom.core.security import create_acess_token, verify_password_hash
from MyPom.schemas.token_schema import Token


router = APIRouter(tags=["Token"])


@router.post("/token", response_model=Token)
def login_for_acess_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter_by(username=form_data.username).first()

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Usuario ou senha incorreto.",
        )

    if not verify_password_hash(form_data.password, user.password):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Usuario ou senha incorreto.",
        )
    access_token = create_acess_token(data={"sub": user.username})

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }
