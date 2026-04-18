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
from MyPom.schemas.pomo_schema import (
    DailySumary,
    DifferenceDays,
    Month_session,
    Session_In,
    SessionM,
)

router = APIRouter(tags=["pomo"])
day_of_the_week = ["segunda", "terça", "quarta", "quinta", "sexta", "sábado", "domingo"]


@router.post("/sessionIn", response_model=SessionM)
def session_in(
    pomo: Session_In,
    db: Session = Depends(get_db),
):
    try:
        new_sesion = Pomo(
            duration=pomo.duration_seconds,
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
        dailly_summaries.append(DailySumary(total_seconds=total, study_date=study_date))

    return dailly_summaries


@router.get("/weekSession")
def week_session(db: Session = Depends(get_db)):
    today = date.today()

    uma_semana_atras = today - timedelta(weeks=1)

    response = (
        db.query(Pomo).where(Pomo.session_date.between(uma_semana_atras, today)).all()
    )
    total = [i.duration for i in response]

    return sum(total), response


@router.get("/monthSession")
def month_session(db: Session = Depends(get_db)):
    today = date.today()
    month = today.replace(day=1)

    query = [
        db.query(func.sum(Pomo.duration))
        .filter(Pomo.session_date >= month, Pomo.session_date <= today)
        .scalar(),
        db.query(func.count(Pomo.session_date))
        .filter(Pomo.session_date >= month, Pomo.session_date <= today)
        .scalar(),
    ]
    return Month_session(
        total_month_duration_minuts=query[0], total_month_sessions=query[1]
    )


@router.get("/differenceInDays")
def difference_in_days(db: Session = Depends(get_db)):
    today = date.today()
    yesterday = today - timedelta(days=1)

    query_day = (
        db.query(func.sum(Pomo.duration)).filter(Pomo.session_date == today).scalar()
        or 0
    )
    query_yesterday = (
        db.query(func.sum(Pomo.duration))
        .filter(Pomo.session_date == yesterday)
        .scalar()
        or 0
    )

    return DifferenceDays(
        today=query_day,
        yesterday=query_yesterday,
        difference=query_day - query_yesterday,
    )


@router.get("/weeklyfrequency")
def weekly_frequency(db: Session = Depends(get_db)):
    hoje = date.today()

    sunday = hoje - timedelta(days=(hoje.weekday() + 1) % 7)

    gabarito = {}
    for i in range(7):
        data_dia = sunday + timedelta(days=i)
        gabarito[data_dia] = 0

    results = (
        db.query(Pomo.session_date, func.sum(Pomo.duration).label("total"))
        .filter(Pomo.session_date >= sunday, Pomo.session_date <= hoje)
        .group_by(Pomo.session_date)
        .all()
    )

    for row in results:
        data_banco = row.session_date
        if hasattr(data_banco, "date"):
            data_banco = data_banco.date()

        if data_banco in gabarito:
            gabarito[data_banco] = int(row.total)

    frequency = []
    for data_dia, duracao in gabarito.items():
        frequency.append(
            {"dayOfTheWeek": day_of_the_week[data_dia.weekday()], "duration": duracao}
        )

    return frequency
