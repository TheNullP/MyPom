from time import sleep

from fastapi import APIRouter, Depends
from fastapi.requests import HTTPConnection
from fastapi.responses import JSONResponse

from MyPom.core.database import Pomo, Session, get_db
from MyPom.schemas.pomo_schema import Session_In, SessionM

router = APIRouter(tags=["Pomo"])


def chrono(time):
    for i in range(time, -1, -1):
        print(i)
        sleep(0.1)


@router.post("/sessionIn", response_model=SessionM)
def session_in(
    pomo: Session_In,
    db: Session = Depends(get_db),
):
    try:
        new_sesion = Pomo(
            duration=pomo.duration_minuts,
            date=pomo.session_date,
        )

        db.commit()
        db.add(new_sesion)
        db.refresh(new_sesion)

    except Exception as e:
        raise f"Erro ao tentar registar Sessão, {e}"
    return JSONResponse(
        content="Sessão adicionada com sucesso.",
        status_code=200,
    )
