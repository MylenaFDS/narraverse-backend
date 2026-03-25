from pydantic import BaseModel, EmailStr
from typing import Optional, List

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None

class UserProfileResponse(BaseModel):
    id: int
    username: str
    email: str
    bio: Optional[str]

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    username: Optional[str] = None
    bio: Optional[str] = None


class UserRPG(BaseModel):
    id: int
    name: str
    description: str | None

    class Config:
        from_attributes = True


class UserProfileResponse(BaseModel):
    id: int
    username: str
    email: str
    bio: str | None

    created_rpgs: List[UserRPG] = []
    participating_rpgs: List[UserRPG] = []

    class Config:
        from_attributes = True