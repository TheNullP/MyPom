from http import HTTPStatus
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from MyPom.core.database import User, get_db
from MyPom.schemas.user_schema import CurrentUser, UserModel
from MyPom.core.security import email_pattern, get_current_user, get_password_hash

router = APIRouter(tags=["user"])


@router.post("/createUser")
def createUser(user: UserModel, db: Session = Depends(get_db)):
    existsUser = db.query(User).filter_by(username=user.username).first()

    if existsUser:
        raise HTTPException(detail="Username ou Email já Existe.", status_code=400)

    if not email_pattern(user.email):
        raise HTTPException(detail="Email inválido.", status_code=400)

    hashed_password = get_password_hash(user.password)
    newUser = User(username=user.username, email=user.email, password=hashed_password)

    db.add(newUser)
    db.commit()
    db.refresh(newUser)

    return JSONResponse(
        content={"msg": f"Usuário {user.username} criado com sucesso."}, status_code=201
    )


@router.get("/searchUser")
def search_user(db: Session = Depends(get_db)):
    response = db.query(User).all()

    return response


@router.get("/currentUser")
def current_user(
    user: User = Depends(get_current_user),
):
    try:
        current_user = CurrentUser(
            username=user.username,
            email=user.email,
            focus=user.focus,
        )
        return current_user
    except Exception as e:
        raise e


@router.delete("/deleteUser/")
def delete_user(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    exist_user = db.query(User).filter_by(username=current_user.username).first()

    if not exist_user:
        raise HTTPException(
            detail="Usario não localizado.",
            status_code=404,
        )

    db.delete(exist_user)
    db.commit()

    return JSONResponse(
        content="Usuario excluido com sucesso",
        status_code=200,
    )


@router.put("/updateUser")
def update_user(
    user: UserModel,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user != user.username:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail="Not enough permission"
        )
    hashed_password = get_password_hash(user.password)

    if not current_user:
        raise HTTPException(
            detail="Usuario não localizado.",
            status_code=404,
        )

    try:
        current_user.username = user.username
        current_user.email = user.email
        current_user.password = hashed_password

        db.commit()
        db.refresh(current_user)

    except Exception as e:
        raise e

    return JSONResponse(
        content="Atualizado com sucesso.",
        status_code=200,
    )
