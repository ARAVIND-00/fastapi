from datetime import datetime
from typing import Optional
from sqlmodel import TIMESTAMP, Field, SQLModel,Column,text,Relationship
from pydantic import EmailStr


class POST(SQLModel, table=True):
    __tablename__: str = "posts"
    id: Optional[int] = Field(default=None, primary_key=True,nullable=False)
    title: str=Field(nullable=False)
    content: str=Field(nullable=False)
    published: bool = Field(default=True,nullable=False)
    created_at:datetime=Field(sa_column=Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"),
    ))
    userid:int=Field(foreign_key="users.id",ondelete="CASCADE",nullable=False)
    user: "USER" = Relationship(back_populates="posts")

class USER(SQLModel,table=True):
    __tablename__:str="users"
    id: Optional[int] = Field(default=None, primary_key=True,nullable=False)
    Email:EmailStr=Field(nullable =False,unique=True)
    password:str= Field(nullable=False)
    created_at:datetime=Field(sa_column=Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"),
    ))
    posts: list["POST"] = Relationship(back_populates="user")
