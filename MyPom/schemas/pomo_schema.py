from typing import List
from pydantic import BaseModel
from datetime import date, today


class SessionM(BaseModel):
    id: int
    duration_minuts: int
    session_date: date


class Session_In(BaseModel):
    duration_minuts: int
    session_date: date = today()


class DailySumary(BaseModel):
    total_minuts: int
    date: date


class week_session(BaseModel):
    start_date: date
    end_date: date
    week_duration: List[DailySumary]
    total_week_duration: int
