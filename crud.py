from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from app import models, schemas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "YOUR_SECRET_KEY" 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_user(db: Session, user: schemas.UserCreate):
    """
    Создаёт нового пользователя в базе данных.

    Args:
        db (Session): Сессия SQLAlchemy для взаимодействия с базой данных.
        user (schemas.UserCreate): Схема Pydantic для создания нового пользователя.

    Returns:
        models.User: Модель пользователя SQLAlchemy, представляющая только что созданного пользователя.
    """
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_contact(db: Session, contact: schemas.ContactCreate, user_id: int):
    """
    Создаёт новый контакт в базе данных.

    Args:
        db (Session): Сессия SQLAlchemy для взаимодействия с базой данных.
        contact (schemas.ContactCreate): Схема Pydantic для создания нового контакта.
        user_id (int): ID пользователя, которому принадлежит контакт.

    Returns:
        models.Contact: Модель контакта SQLAlchemy, представляющая только что созданный контакт.
    """
    db_contact = models.Contact(**contact.dict(), owner_id=user_id)
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

def authenticate_user(db: Session, email: str, password: str):
    """
    Аутентифицирует пользователя по электронной почте и паролю.

    Args:
        db (Session): Сессия SQLAlchemy для взаимодействия с базой данных.
        email (str): Электронная почта пользователя.
        password (str): Пароль пользователя.

    Returns:
        models.User: Модель пользователя SQLAlchemy, представляющая аутентифицированного пользователя.
    """
    user = get_user_by_email(db, email)
    if not user:
        return False
    if not pwd_context.verify(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Создает токен доступа JWT.

    Args:
        data (dict): Данные, которые следует включить в токен.
        expires_delta (Optional[timedelta]): Время, через которое истекает срок действия токена.

    Returns:
        str: Токен доступа JWT.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
