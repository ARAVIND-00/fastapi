
import sys
import uvicorn
from fastapi import FastAPI,Response,status,HTTPException
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models,schemas 

from .database import engine,SessionDep,create_db_and_tables
from fastapi import Depends, FastAPI, HTTPException, Query
from contextlib import asynccontextmanager
from sqlmodel import SQLModel
import logging
from .routers import post,user,auth


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     try:
#         create_db_and_tables
#         print("connection to db was sucessful")
#         yield
#     finally:
#         await engine.dispose()
# app = FastAPI(
#     lifespan=lifespan)


@asynccontextmanager
async def lifespan(app: FastAPI):
        create_db_and_tables()
        yield


app = FastAPI(lifespan=lifespan)

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
## Schmea design




app.include_router(post.router)
app.include_router(user.router) 
app.include_router(auth.router) 
