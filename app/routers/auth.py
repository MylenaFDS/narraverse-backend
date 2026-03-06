from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import UserService
from app.db.deps import get_db
from app.models.user import User
from app.core.config import settings

router = APIRouter(prefix="/auth", tags=["Auth"])

# OAuth2 scheme para pegar o token
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
# 🔑 LOGIN (CORRIGIDO)
# ------------------------
@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    IMPORTANTE:
    O OAuth2PasswordRequestForm envia:
    - username
    - password
    como form-data (não JSON)

    Aqui estamos usando username como EMAIL.
    """

    try:
        token = UserService.login(
            db,
            form_data.username,  # ← aqui será o email
            form_data.password
        )

        return {
            "access_token": token,
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
        detail="Could not validate credentials",
    )

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
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