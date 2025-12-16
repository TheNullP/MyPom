from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from MyPom.app import app
from MyPom.core.database import Pomo, User, get_db, reg
from MyPom.core.setting import Settings
from datetime import timedelta, date

settings = Settings()

engine = create_engine(settings.DB_URL_TEST)
# engine = create_engine(settings.DB_URL_TEST, connect_args={"check_same_thread": False})

TestingSessionLoca = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session")
def db():
    reg.metadata.create_all(bind=engine)

    db = TestingSessionLoca()
    try:
        yield db
    finally:
        db.rollback()
        db.close()
        reg.metadata.drop_all(bind=engine)


@pytest.fixture
def user(db: Session):
    new_user = User(
        username="test_user",
        password="test_password",
        email="test_email@example.com",
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    yield new_user

    db.delete(new_user)
    db.flush()


@pytest.fixture
def session_pomo(db: Session):
    today = date.today()

    new_pomo1 = Pomo(duration=25, session_date=f"{today - timedelta(days=1)}")
    new_pomo2 = Pomo(duration=60, session_date=f"{today - timedelta(days=1)}")
    new_pomo3 = Pomo(duration=25, session_date=f"{today - timedelta(days=2)}")
    new_pomo4 = Pomo(duration=25, session_date=f"{today - timedelta(days=3)}")
    new_pomo5 = Pomo(duration=25, session_date=f"{today - timedelta(days=4)}")
    new_pomo6 = Pomo(duration=25, session_date=f"{today - timedelta(days=5)}")

    db.add(new_pomo1)
    db.add(new_pomo2)
    db.add(new_pomo3)
    db.add(new_pomo4)
    db.add(new_pomo5)
    db.add(new_pomo6)
    db.commit()
    db.refresh(new_pomo1)
    db.refresh(new_pomo2)
    db.refresh(new_pomo3)
    db.refresh(new_pomo4)
    db.refresh(new_pomo5)
    db.refresh(new_pomo6)

    yield new_pomo1, new_pomo2, new_pomo3, new_pomo4, new_pomo5, new_pomo6

    db.delete(new_pomo1)
    db.flush()


@pytest.fixture
def client(db: Session):
    def override_get_db():
        return db

    with TestClient(app) as client:
        app.dependency_overrides[get_db] = override_get_db

        yield client

    app.dependency_overrides.clear()
