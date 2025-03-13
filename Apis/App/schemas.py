from pyclbr import Class
from pydantic import BaseModel, EmailStr,Field
from datetime import datetime
class PostBase(BaseModel):
    title:str
    content:str
    published:bool=Field(default=True)

class create_post(PostBase):
    pass

class PostResponse(PostBase):
    created_at:datetime

class UserCreate(BaseModel):
    Email:EmailStr
    password:str

class UserResponse(BaseModel):
    Email:EmailStr
    id:int

class loginuser(BaseModel):
    Email:EmailStr
    password:str