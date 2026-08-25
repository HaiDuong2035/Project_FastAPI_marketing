from pydantic import BaseModel, EmailStr

class UserRegisterInput(BaseModel):
    email: EmailStr
    password: str
    full_name: str

class UserLoginInput(BaseModel):
    email: EmailStr
    password: str