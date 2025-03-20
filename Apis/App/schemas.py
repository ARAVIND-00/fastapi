from typing import Optional
from pydantic import BaseModel, EmailStr,Field
from datetime import datetime
from typing import Optional
class PostBase(BaseModel):
    title:str
    content:str
    published:bool=Field(default=True)

class create_post(PostBase):
    pass

class UserResponse(BaseModel):
    Email:EmailStr
    id:int


class PostResponse(PostBase):
    userid:int
    created_at:datetime
    user: UserResponse


class UserCreate(BaseModel):
    Email:EmailStr
    password:str



class loginuser(BaseModel):
    Email:EmailStr
    password:str
class token(BaseModel):
    token:str
    token_type:str

class token_data(BaseModel):
    id:Optional[int]=None
