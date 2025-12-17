from http import HTTPStatus
from datetime import date


def test_lista_total_de_sessoes(client, db, session_pomo):
    response = client.get("/SessionList")

    data = response.json()

    assert response is not None
    assert response.status_code == 200
    assert len(data) == 6


def test_inserir_nova_sessao(db, session_pomo, client):
    response = client.post(
        "/sessionIn",
        json={"duration_minutes": 25, "session_date": "2025-12-15T00:00:00+00:00"},
    )

    assert response is not None
    assert response.status_code == 200
    assert response.json() == "Sessão adicionada com sucesso."


def test_inserir_nova_sessao_com_dados_invalidos(db, session_pomo, client):
    response = client.post(
        "/sessionIn",
        json={"duration_minutes": "25", "session_date": "01-12-2025"},
    )

    assert response is not None
    assert response.status_code == 422


def test_lista_de_sessao_do_dia(db, session_pomo, client):
    response = client.get("/dailysession")

    data = response.json()

    assert response is not None
    assert response.status_code == 200
    assert data[0]["total_minutes"] == 85
    assert data[0]["study_date"] == str(date.today())


def test_lista_de_sessao_da_semana(db, session_pomo, client):
    response = client.get("/weekSession")

    data = response.json()

    assert response is not None
    assert response.status_code == 200
    assert len(data) == 7
