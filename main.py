from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from typing import List

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Security
from fastapi import Depends, status
from datetime import timedelta


app = FastAPI()

# Database setup
DATABASE_URL = "sqlite:///./users.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# SQLAlchemy model
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String)
    full_name = Column(String)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)
    submitted_by = Column(String, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow)

# Create the table
Base.metadata.create_all(bind=engine)

#//////////////////////// schema to enter details

class UserCreate(BaseModel):
    type: str
    full_name: str
    username: str
    email: EmailStr
    password: str
    submitted_by: Optional[str] = None



# //////////////////// schema to display password 
class UserOut(BaseModel):
    id: int
    type: str
    full_name: str
    username: str
    email: str
    password: str
    submitted_by: Optional[str]
    updated_at: datetime

    class Config:
        orm_mode = True



@app.post("/register")
def register_user(user: UserCreate):
    db = SessionLocal()
    # Check if username or email already exists
    existing_user = db.query(User).filter((User.username == user.username) | (User.email == user.email)).first()
    if existing_user:
        db.close()
        raise HTTPException(status_code=400, detail="Username or email already exists")

    db_user = User(
        type=user.type,
        full_name=user.full_name,
        username=user.username,
        email=user.email,
        password=get_password_hash(user.password),  # Consider hashing in real-world apps
        submitted_by=user.submitted_by,
        updated_at=datetime.utcnow()
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    db.close()

    return {"message": "User registered successfully", "user_id": db_user.id}


# //////////////////////////////////////////////////// get all user details


@app.get("/users", response_model=List[UserOut])
def get_users():
    db = SessionLocal()
    users = db.query(User).all()
    db.close()
    return users

# //////////////////////////////////////////////////// LOGIN 


# Secret key for JWT (use a strong key in production!)
SECRET_KEY = "f87b6e4e7c2a0d539d1b3fbecc30584f4bb0b4dc20f6c1d3b7811dfb92ac9aa4"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Token handling
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Modify password storage to use hashed passwords
def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Authentication helper
def authenticate_user(username: str, password: str):
    db = SessionLocal()
    user = db.query(User).filter(User.username == username).first()
    db.close()
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user

# /////////////////////////////////////////// get access token of the user down

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


# /////////////////////////////////////////// get access token of the user up



def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    db = SessionLocal()
    user = db.query(User).filter(User.username == username).first()
    db.close()
    if user is None:
        raise credentials_exception
    return user




@app.get("/profile")
def read_users_me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "full_name": current_user.full_name,
        "email": current_user.email,
        "type": current_user.type
    }


