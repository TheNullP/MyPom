from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from MyPom.core.database import User, get_db
from MyPom.schemas.user_schema import UserModel

router = APIRouter(tags=["user"])


@router.post("/createUser")
def createUser(user: UserModel, db: Session = Depends(get_db)):
    existsUser = db.query(User).filter_by(username=user.username).first()

    if existsUser:
        raise HTTPException(
            detail={"msg": "Username ou Email já Existe."}, status_code=404
        )
    newUser = User(username=user.username, email=user.email, password=user.password)

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


@router.delete("/deleteUser/")
def delete_user(
    IdUser: int,
    db: Session = Depends(get_db),
):
    exist_user = db.query(User).filter_by(id=IdUser).first()

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
    IdUser: int,
    user: UserModel,
    db: Session = Depends(get_db),
):
    exist_user = db.query(User).filter_by(id=IdUser).first()

    if not exist_user:
        raise HTTPException(
            detail="Usuario não localizado.",
            status_code=404,
        )
    try:
        exist_user.username = user.username
        exist_user.email = user.email
        exist_user.password = user.password

        db.commit()
        db.refresh(exist_user)

    except Exception as e:
        raise e

    return JSONResponse(
        content="Atualizado com sucesso.",
        status_code=200,
    )
