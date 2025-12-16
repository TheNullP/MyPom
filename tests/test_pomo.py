from http import HTTPStatus


def test_lista_total_de_sessoes(client, db, session_pomo):
    response = client.get("/SessionList")

    data = response.json()

    assert response is not None
    assert response.status_code == 200
    assert data == [
        {"id": 1, "duration": 25, "session_date": "2025-12-15T00:00:00+00:00"},
        {"id": 2, "duration": 60, "session_date": "2025-12-15T00:00:00+00:00"},
        {"id": 3, "duration": 25, "session_date": "2025-12-14T00:00:00+00:00"},
        {"id": 4, "duration": 25, "session_date": "2025-12-13T00:00:00+00:00"},
        {"id": 5, "duration": 25, "session_date": "2025-12-12T00:00:00+00:00"},
        {"id": 6, "duration": 25, "session_date": "2025-12-11T00:00:00+00:00"},
    ]


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
