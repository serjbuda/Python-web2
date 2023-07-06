from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app import models, schemas, crud
from sqlalchemy.orm import Session
from typing import Optional

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(db: Session = Depends(database.get_db), token: str = Depends(oauth2_scheme)):
    """
    Возвращает текущего пользователя на основе JWT токена.

    FastAPI будет автоматически использовать эту функцию, где бы это ни потребовалось, благодаря 
    механизму зависимостей.

    Args:
        db (Session): Сессия SQLAlchemy, используемая для взаимодействия с базой данных.
        token (str): JWT токен, предоставленный пользователем.

    Raises:
        HTTPException: JWT токен недействителен или пользователь не найден.

    Returns:
        models.User: Модель SQLAlchemy текущего пользователя.
    """
    try:
        payload = jwt.decode(token, crud.SECRET_KEY, algorithms=[crud.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise JWTError
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = crud.get_user_by_email(db, email=email)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
