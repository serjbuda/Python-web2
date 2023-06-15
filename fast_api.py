from typing import List, Optional
from fastapi import FastAPI, HTTPException
from sqlalchemy import Boolean, Column, Integer, String, Date, create_engine, or_
from sqlalchemy.orm import Session, sessionmaker, Query
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel, EmailStr
from datetime import datetime, timedelta

Base = declarative_base()

engine = create_engine('postgresql://user:password@localhost:5432/mydatabase')

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone_number = Column(String, index=True)
    birth_date = Column(Date)
    additional_info = Column(String, nullable=True)


class ContactBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    birth_date: str
    additional_info: Optional[str] = None


class ContactCreate(ContactBase):
    pass


class ContactRead(ContactBase):
    id: int


class ContactUpdate(ContactBase):
    pass


app = FastAPI()


@app.post("/contacts/", response_model=ContactRead)
def create_contact(contact: ContactCreate, db: Session = Depends(get_db)):
    db_contact = Contact(**contact.dict())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


@app.get("/contacts/", response_model=List[ContactRead])
def read_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    contacts = db.query(Contact).offset(skip).limit(limit).all()
    return contacts


@app.get("/contacts/{contact_id}", response_model=ContactRead)
def read_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact


@app.put("/contacts/{contact_id}", response_model=ContactRead)
def update_contact(contact_id: int, contact: ContactUpdate, db: Session = Depends(get_db)):
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    for key, value in contact.dict().items():
        setattr(db_contact, key, value)
    db.commit()
    db.refresh(db_contact)
    return db_contact


@app.delete("/contacts/{contact_id}")
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    db.delete(db_contact)
    db.commit()
    return {"detail": "Contact deleted"}


@app.get("/contacts/search", response_model=List[ContactRead])
def search_contacts(q: str, db: Session = Depends(get_db)):
    contacts = db.query(Contact).filter(
        or_(
            Contact.first_name.contains(q),
            Contact.last_name.contains(q),
            Contact.email.contains(q)
        )
    ).all()
    return contacts


@app.get("/contacts/upcoming_birthdays", response_model=List[ContactRead])
def upcoming_birthdays(db: Session = Depends(get_db)):
    today = datetime.today().date()
    week_from_now = today + timedelta(days=7)
    contacts = db.query(Contact).filter(
        (Contact.birth_date >= today) & (Contact.birth_date <= week_from_now)
    ).all()
    return contacts
