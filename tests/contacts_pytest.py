import pytest
from sqlalchemy.orm import Session
from app import crud, models, schemas

def test_create_contact():
    db = Session()  
    contact_data = schemas.ContactCreate(name="John Doe", phone_number="+1234567890")
    contact = crud.create_contact(db, contact_data, user_id=1)  # replace `user_id=1` with a valid user ID
    assert contact.name == contact_data.name
