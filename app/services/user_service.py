from sqlalchemy.orm import Session
from app.repositories.user_repository import UserRepository
from app.core.security import hash_password, verify_password, create_access_token
from app.models.user import User


class UserService:

    @staticmethod
    def register(db: Session, username: str, email: str, password: str):
        existing_user = UserRepository.get_by_email(db, email)
        if existing_user:
            raise ValueError("Email já cadastrado")

        password_hash = hash_password(password)
        return UserRepository.create(db, username, email, password_hash)

    @staticmethod
    def login(db: Session, email: str, password: str):
        user = UserRepository.get_by_email(db, email)
        if not user:
            raise ValueError("Credenciais inválidas")

        if not verify_password(password, user.password_hash):
            raise ValueError("Credenciais inválidas")

        token = create_access_token({"sub": str(user.id)})
        return token

    @staticmethod
    def get_all(db: Session):
        return db.query(User).all()

    @staticmethod
    def get_by_id(db: Session, user_id: int):
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def update(db: Session, user_id: int, user_data):
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return None

        if user_data.username is not None:
            user.username = user_data.username

        if user_data.email is not None:
            user.email = user_data.email

        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def delete(db: Session, user_id: int):
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return False

        db.delete(user)
        db.commit()
        return True