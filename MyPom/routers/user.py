from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse

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
    # db = databaseTemp
):
    existsUser = db_Query(databaseTemp, username)

    if existsUser:
        raise HTTPException(
            detail={'msg': 'Username ou Email já Existe.'},
            status_code=404
        )

    user = {
        'username': username,
        'email': email,
        'password': password,
    }

    databaseTemp.append(user)

    return JSONResponse(
        content={'msg': f'Usuário {username} criado com sucesso.'},
        status_code=201
    )

