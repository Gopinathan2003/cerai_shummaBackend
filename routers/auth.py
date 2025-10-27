from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import Users as UserModel
from app.schemas.user import User, UserCreate, Login
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from app.controllers import auth

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

# def get_password_hash(password):
#     return pwd_context.hash(password)

# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)

# def create_access_token(data: dict, expires_delta: timedelta = None):
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + timedelta(minutes=15)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt

# def get_user(db, username: str):
#     return db.query(UserModel).filter(UserModel.user_name == username).first()


@router.post("/login")
async def login(user: Login, db: Session = Depends(get_db)):
    return auth.login(db, user)
    # user_obj = get_user(db, user.user_name)
    # if not user_obj or not verify_password(user.password, user_obj.password):
    #     raise HTTPException(status_code=400, detail="Incorrect username or password")
    # access_token = create_access_token({"sub": user_obj.user_name, "role": user_obj.role.value})
    # return {"access_token": access_token, "token_type": "bearer"}


# @router.post("/token")
# async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
#     user = get_user(db, form_data.username)
#     if not user or not verify_password(form_data.password, user.hashed_password):
#         raise HTTPException(status_code=400, detail="Incorrect username or password")
#     access_token = create_access_token({"sub": user.username, "role": user.role})
#     return {"access_token": access_token, "token_type": "bearer"}

# async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
#     credentials_exception = HTTPException(
#         status_code=401,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#         user = get_user(db, username)
#         if not user:
#             raise credentials_exception
#         return user
#     except:
#         raise credentials_exception

# @router.get("/dashboard")
# async def read_dashboard(current_user: UserModel = Depends(get_current_user)):
#     if current_user.role.value not in ["admin", "manager", "curator"]:
#         raise HTTPException(status_code=403, detail="Not enough permissions")
#     return {
#         "message": f"Welcome {current_user.role.value}",
#         "data": {
#             "test_cases": 1635,
#             "targets": 534,
#             "test_runs": 1215,
#             "strategies": 44,
#             "languages": 9,
#             "responses": 288,
#             "prompts": 407
#         }
#     }