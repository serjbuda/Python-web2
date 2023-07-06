from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas, crud, database
from fastapi.testclient import TestClient
import main.py
import unittest

router = APIRouter()
client = TestClient(app)

@router.post("/users/", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    """
    Создает нового пользователя в базе данных.

    Args:
        user (schemas.UserCreate): Объект Pydantic, содержащий данные нового пользователя.
        db (Session): Сессия SQLAlchemy, используемая для взаимодействия с базой данных.

    Raises:
        HTTPException: Пользователь с таким электронным адресом уже существует.

    Returns:
        schemas.User: Модель Pydantic пользователя, который был только что создан.
    """
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=409, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@router.post("/token", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    """
    Аутентифицирует пользователя и возвращает токен доступа.

    Args:
        form_data (OAuth2PasswordRequestForm): Форма FastAPI, содержащая имя пользователя и пароль.
        db (Session): Сессия SQLAlchemy, используемая для взаимодействия с базой данных.

    Raises:
        HTTPException: Имя пользователя или пароль некорректны.

    Returns:
        schemas.Token: Токен доступа для аутентифицированного пользователя.
    """
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=crud.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = crud.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

class TestUserRoutes(unittest.TestCase):
    def setUp(self):
        self.db = Session()  # You need to set up a test database connection here

    def test_create_user(self):
        user_data = {
            "email": "test@example.com",
            "password": "password",
        }
        response = client.post("/users/", json=user_data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["email"], user_data["email"])

    def test_login_for_access_token(self):
        user_data = {
            "username": "test@example.com",
            "password": "password",
        }
        response = client.post("/token", data=user_data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue("access_token" in response.json())

    def tearDown(self):
        self.db.rollback()  # Make sure the test data doesn't affect your actual database

if __name__ == "__main__":
    unittest.main()
