from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from pydantic import BaseModel

from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import UserService
from app.db.deps import get_db
from app.models.user import User
from app.core.config import settings
from app.core.security import create_access_token, create_refresh_token

router = APIRouter(prefix="/auth", tags=["Auth"])

# OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# ------------------------
# 👤 REGISTER
# ------------------------
@router.post("/register", response_model=UserResponse)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    try:
        user = UserService.register(
            db,
            user_data.username,
            user_data.email,
            user_data.password
        )
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ------------------------
# 🔑 LOGIN
# ------------------------
@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    try:
        user = UserService.authenticate(
            db,
            form_data.username,
            form_data.password
        )

        if not user:
            raise ValueError("Credenciais inválidas")

        access_token = create_access_token({"sub": str(user.id)})
        refresh_token = create_refresh_token({"sub": str(user.id)})

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ------------------------
# 🔎 GET CURRENT USER
# ------------------------
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
    )

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        user_id: str = payload.get("sub")

        if user_id is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.id == int(user_id)).first()

    if user is None:
        raise credentials_exception

    return user


# ------------------------
# 🔒 PROTECTED ROUTE
# ------------------------
@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


# ------------------------
# 🔄 REFRESH TOKEN
# ------------------------
class RefreshRequest(BaseModel):
    refresh_token: str


@router.post("/refresh")
def refresh_token(data: RefreshRequest):
    try:
        payload = jwt.decode(
            data.refresh_token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        # 🔥 garante que é refresh token
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Token inválido")

        user_id = payload.get("sub")

        new_access_token = create_access_token({"sub": user_id})

        return {
            "access_token": new_access_token
        }

    except JWTError as e:
        print("ERRO REFRESH:", e)
        raise HTTPException(status_code=401, detail="Refresh inválido")