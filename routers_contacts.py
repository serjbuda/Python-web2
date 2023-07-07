from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas, crud, database

router = APIRouter()

@router.post("/contacts/", response_model=schemas.Contact)
def create_contact(contact: schemas.ContactCreate, db: Session = Depends(database.get_db)):
    """
    Создает новый контакт для текущего пользователя.

    Args:
        contact (schemas.ContactCreate): Схема Pydantic для создания нового контакта.
        db (Session): Сессия SQLAlchemy для взаимодействия с базой данных.

    Returns:
        schemas.Contact: Модель Pydantic контакта, который был только что создан.
    """
    return crud.create_contact(db=db, contact=contact, user_id=1)  # you'll need to replace `user_id=1` with the ID of the current user

@router.get("/contacts/", response_model=List[schemas.Contact])
def read_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    """
    Возвращает список контактов текущего пользователя.

    Args:
        skip (int, optional): Количество контактов, которые следует пропустить. Defaults to 0.
        limit (int, optional): Максимальное количество контактов для возврата. Defaults to 100.
        db (Session): Сессия SQLAlchemy для взаимодействия с базой данных.

    Returns:
        List[schemas.Contact]: Список моделей Pydantic контактов.
    """
    contacts = crud.get_contacts(db, skip=skip, limit=limit)
    return contacts

@router.get("/contacts/{contact_id}", response_model=schemas.Contact)
def read_contact(contact_id: int, db: Session = Depends(database.get_db)):
    """
    Возвращает контакт по его идентификатору.

    Args:
        contact_id (int): ID контакта.
        db (Session): Сессия SQLAlchemy для взаимодействия с базой данных.

    Raises:
        HTTPException: Контакт не найден.

    Returns:
        schemas.Contact: Модель Pydantic контакта.
    """
    db_contact = crud.get_contact(db, contact_id=contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact
