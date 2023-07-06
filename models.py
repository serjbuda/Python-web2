from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    """
    Модель пользователя в базе данных SQLAlchemy.

    Атрибуты:
        id (Integer): Уникальный идентификатор пользователя. Является первичным ключом.
        email (String): Электронная почта пользователя. Должна быть уникальной.
        hashed_password (String): Хэшированный пароль пользователя.
        is_active (Boolean): Статус активности пользователя. По умолчанию истина.
        contacts (relationship): Отношение к контактам, принадлежащим пользователю.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    contacts = relationship("Contact", back_populates="owner")

class Contact(Base):
    """
    Модель контакта в базе данных SQLAlchemy.

    Атрибуты:
        owner_id (Integer): Уникальный идентификатор пользователя, которому принадлежит контакт. Является внешним ключом.
        owner (relationship): Отношение к пользователю, которому принадлежит контакт.
    """
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="contacts")
