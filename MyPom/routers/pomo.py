import datetime

from datetime import date, timedelta
from time import sleep
from typing_extensions import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy import Date, cast
from sqlalchemy.future import select
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from MyPom.core.database import Pomo, get_db
from MyPom.schemas.pomo_schema import DailySumary, Session_In, SessionM

router = APIRouter(tags=["pomo"])


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
            duration=pomo.duration_minutes,
            session_date=pomo.session_date,
        )

        db.add(new_sesion)
        db.commit()
        db.refresh(new_sesion)

    except Exception as e:
        return HTTPException(
            detail=f"Erro ao inserir nova sessão, Erro: {e}",
            status_code=422,
        )

    return JSONResponse(
        content="Sessão adicionada com sucesso.",
        status_code=200,
    )


@router.get("/SessionList")
def session_list(db: Session = Depends(get_db)):
    response = db.query(Pomo).all()
    return response


@router.get("/dailysession", response_model=List[DailySumary])
def daily_session(db: Session = Depends(get_db)):
    today = date.today()
    response = (
        select(func.sum(Pomo.duration), Pomo.session_date)
        .where(cast(Pomo.session_date, Date) == today)
        .group_by(Pomo.session_date)
        .group_by(Pomo.session_date)
    )

    results = db.execute(response).all()

    dailly_summaries = []

    for total, study_date in results:
        dailly_summaries.append(DailySumary(total_minutes=total, study_date=study_date))

    return dailly_summaries


@router.get("/weekSession")
def week_session(db: Session = Depends(get_db)):
    today = date.today()

    uma_semana_atras = today - timedelta(weeks=1)

    response = (
        db.query(Pomo).where(Pomo.session_date.between(uma_semana_atras, today)).all()
    )

    return response
