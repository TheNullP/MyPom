from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
import pytest
from fastapi.testclient import TestClient

from MyPom.core.database import User, get_db, reg
from MyPom.core.setting import Settings
from MyPom.app import app

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
        
    new_user =  User(
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
def client(db: Session):

    def override_get_db():
        return db

    with TestClient(app) as client:
        app.dependency_overrides[get_db] = override_get_db

        yield client

    app.dependency_overrides.clear()
