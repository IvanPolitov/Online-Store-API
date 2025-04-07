from datetime import datetime, timedelta
from typing import Dict
from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt
import uuid

from online_store.app.config import API_VERSION, AUTH_ENDPOINT
from online_store.app.db.models import User
from online_store.app.db.base import get_db
from online_store.app.schema.auth_schema import TokenResponse, UserCreate, UserResponse


auth_router = APIRouter(prefix='/auth', tags=['auth'])
oauth2_schema = OAuth2PasswordBearer(tokenUrl=f'{API_VERSION}{AUTH_ENDPOINT}')

UNAUTH_401 = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
CRED_EXC = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={'WWW-Authenticate': 'Bearer'}
    )

ACCESS_TOKEN_EXPIRE_MINUTES = 60
SECRET_KEY = 'SECRET_KEY'
ALGORITHM = "HS256"


def password_hash(password: str) -> str:
    return password


def create_token(data: Dict) -> str:
    to_encode = data.copy()
    jti = str(uuid.uuid4())
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"jti": jti, 'exp': expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token


def get_current_user(
        db: Session = Depends(get_db),
        token: str = Depends(oauth2_schema)
        ) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="Не авторизован")
    except JWTError:
        raise HTTPException(status_code=401, detail="Не авторизован1")

    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=401, detail="Пользователь не найден")
    return user


@auth_router.post("/login", response_model=TokenResponse)
async def login(
    db: Session = Depends(get_db),
    credentials: OAuth2PasswordRequestForm = Depends()
):
    user = db.query(User).filter(credentials.username == User.username).first()
    if not user:
        raise UNAUTH_401

    if user.password_hash != password_hash(credentials.password):
        raise UNAUTH_401

    access_token = create_token({'sub': user.username})
    token = TokenResponse(access_token=access_token)
    return token


@auth_router.post("/register", response_model=UserResponse)
async def register(
    credentials: UserCreate,
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(
        (User.username == credentials.username) |
        (User.email == credentials.email)
        ).first()

    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email or username already registered"
            )

    new_user = User(
        username=credentials.username,
        email=credentials.email,
        age=credentials.age,
        password_hash=password_hash(credentials.password),
        created_at=datetime.now()
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@auth_router.get("/logout")
async def logout():
    
    return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )


@auth_router.get("/protected")
async def protected(current_user: User = Depends(get_current_user)):
    return {"message": f"protected {current_user.username}"}
