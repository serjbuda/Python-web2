import pytest
from sqlalchemy.orm import Session
from app import crud, models, schemas

def test_create_user():
    db = Session()
    user_data = schemas.UserCreate(email="test@example.com", password="password")
    user = crud.create_user(db, user_data)
    assert user.email == user_data.email
