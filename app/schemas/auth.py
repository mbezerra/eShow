from pydantic import BaseModel, EmailStr

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

    model_config = {"from_attributes": True}

class TokenData(BaseModel):
    user_id: int | None = None

    model_config = {"from_attributes": True}

class UserLogin(BaseModel):
    email: EmailStr
    password: str

    model_config = {"from_attributes": True}

class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str
    is_active: bool = True

    model_config = {"from_attributes": True}

class RefreshToken(BaseModel):
    refresh_token: str

    model_config = {"from_attributes": True} 