
from sqlmodel import Session, SQLModel, create_engine
from typing import Annotated
from fastapi import Depends
import psycopg2
from psycopg2.extras import RealDictCursor
from .config import settings
from functools import lru_cache

#database
# while True:
#     try:
#         # Connect to  postgres DB
#         conn = psycopg2.connect(host ="localhost",dbname="fastapi", user="postgres",password="postgres",cursor_factory=RealDictCursor)
#         cursor=conn.cursor()
#         print("db connection was successful")
#         break
#     except Exception as e:
#         time.sleep(2)
#         print(e)

sql_url = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(sql_url, echo=True)


def get_session():
    with Session(engine) as session:
        yield session
SessionDep = Annotated[Session, Depends(get_session)]

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    print("connection to db was sucessful")