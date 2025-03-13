
from sqlmodel import Field, Session, SQLModel, create_engine, select
from typing import Annotated
from fastapi import Depends

sql_url = "postgresql://postgres:postgres@localhost/fastapi"

engine = create_engine(sql_url, echo=True)


def get_session():
    with Session(engine) as session:
        yield session
SessionDep = Annotated[Session, Depends(get_session)]

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    print("connection to db was sucessful")