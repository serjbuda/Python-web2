from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps

router = APIRouter()


@router.post("/contacts/", response_model=schemas.Contact)
def create_contact(
    contact: schemas.ContactCreate, db: Session = Depends(deps.get_db)
):
    """
    Create new contact.
    """
    db_contact = crud.get_contact_by_email(db, email=contact.email)
    if db_contact:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_contact(db=db, contact=contact)


@router.get("/contacts/", response_model=List[schemas.Contact])
def read_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(deps.get_db)):
    """
    Read contacts.
    """
    contacts = crud.get_contacts(db, skip=skip, limit=limit)
    return contacts
