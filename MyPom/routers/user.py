from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from core.database import User, get_db

router = APIRouter(tags=["user"])

databaseTemp = [
    {
        "username":"test",
        "email": 'test@email.com',
        "password": 'test'
    }
]

def db_Query(db, username):
    for i in db:
        if i['username'] == username:
            return True
        return False



@router.post('/createUser')
def createUser(
    username: str,
    email: str,
    password: str,
    db: Session = Depends(get_db)
):
    existsUser = db.query(User).filter_by(username=username).first()

    if existsUser:
        raise HTTPException(
            detail={'msg': 'Username ou Email já Existe.'},
            status_code=404
        )

    newUser = User(
        username=username,
        email=email,
        password=password
    )

    db.add(newUser)
    db.commit()
    db.refresh(newUser)

    return JSONResponse(
        content={'msg': f'Usuário {username} criado com sucesso.'},
        status_code=201
    )

