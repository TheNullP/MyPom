from http import HTTPStatus
from MyPom.core.database import User



def test_user_is_createad_and_exists(user, db):
    
    found_user = db.query(User).filter_by(username='test_user').first()

    assert found_user is not None, "O usuário criado pela fixture não foi localizado no DB"

    assert found_user.username == "test_user", "O username encontrado está incorreto"
    assert found_user.email == "test_email@example.com", "O email encontrado está incorreto"

def test_usuario_criaado_nao_localizado(user, db):

    found_user = db.query(User).filter_by(username='test').first()
    
    assert found_user is None, "Usuário não deve ser localizado DB."

def test_endpoint_pesquisa_usuarios( user, db, client):
    response = client.get("/searchUser")

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()) == 1, "Pesquisa de lista de usuário incorreto, deveria haver somente 1 resgistro."

def test_endpoint_criacao_de_usuario(user, db, client):
    response = client.post('/createUser', 
        json={
            "username": "test",
            "email": "test@test.com",
            "password": "test"
        }
    )

    assert response.status_code == 201

def test_endpoint_criacao_de_usuario_ja_existente(user, db, client):
    response = client.post('/createUser', 
    json={
        "username":"test_user",
        "password":"test_password",
        "email":"test_email@example.com",
    }) 

    assert response.status_code == 404
    assert response.json() == {"detail":{"msg": "Username ou Email já Existe."}}
