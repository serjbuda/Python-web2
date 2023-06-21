from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    contacts = relationship("Contact", back_populates="owner")

class Contact(Base):
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="contacts")
