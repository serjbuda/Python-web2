from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from app import models, schemas
import unittest

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "YOUR_SECRET_KEY"  
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_user(db: Session, user: schemas.UserCreate):
    """
    Создает нового пользователя в базе данных.

    Args:
        db (Session): Сессия SQLAlchemy, используемая для взаимодействия с базой данных.
        user (schemas.UserCreate): Объект Pydantic, содержащий данные нового пользователя.

    Returns:
        models.User: Модель SQLAlchemy пользователя, который был только что создан.
    """
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_contact(db: Session, contact: schemas.ContactCreate, user_id: int):
    """
    Создает новый контакт в базе данных для данного пользователя.

    Args:
        db (Session): Сессия SQLAlchemy, используемая для взаимодействия с базой данных.
        contact (schemas.ContactCreate): Объект Pydantic, содержащий данные нового контакта.
        user_id (int): Уникальный идентификатор пользователя.

    Returns:
        models.Contact: Модель SQLAlchemy контакта, который был только что создан.
    """
    db_contact = models.Contact(**contact.dict(), owner_id=user_id)
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

def authenticate_user(db: Session, email: str, password: str):
    """
    Аутентифицирует пользователя, проверяя соответствие электронной почты и пароля.

    Args:
        db (Session): Сессия SQLAlchemy, используемая для взаимодействия с базой данных.
        email (str): Электронная почта пользователя.
        password (str): Пароль пользователя.

    Returns:
        models.User: Модель SQLAlchemy пользователя, если аутентификация прошла успешно.
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
        data (dict): Данные, которые будут включены в токен.
        expires_delta (Optional[timedelta]): Время жизни токена.

    Returns:
        str: JWT токен доступа.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

class TestGetUser(unittest.TestCase):
    def setUp(self):
        self.db = Session() 

    def test_get_user(self):
        user_id = 1
        user = crud.get_user(self.db, user_id)

        self.assertEqual(user.id, user_id)

    def tearDown(self):
        self.db.rollback()  

