import datetime
from typing import List

from pydantic import BaseModel


class SessionM(BaseModel):
    id: int
    duration_seconds: int
    session_date: datetime.date


class Session_In(BaseModel):
    duration_seconds: int
    session_date: datetime.date = datetime.date.today()


class DailySumary(BaseModel):
    total_seconds: int
    study_date: datetime.date


class Week_session(BaseModel):
    start_date: datetime.date
    end_date: datetime.date
    daily_totals: List[DailySumary]
    total_week_duration_minuts: int


class Month_session(BaseModel):
    total_month_duration_minuts: int
    total_month_sessions: int


class DifferenceDays(BaseModel):
    today: int
    yesterday: int
    difference: int


class Weekly_frequency(BaseModel):
    dayOfTheWeek: str
    duration: int
