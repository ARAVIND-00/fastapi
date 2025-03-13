import sys
import uvicorn
from numbers import Real
from fastapi import FastAPI,Response,status,HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .models import Post
from .database import engine,SessionDep
from fastapi import Depends, FastAPI, HTTPException, Query
from contextlib import asynccontextmanager
from sqlmodel import  SQLModel


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     try:
#         SQLModel.metadata.create_all(engine)
#         yield
#     finally:
#         await engine.dispose()
# app = FastAPI(
#     lifespan=lifespan)

app=FastAPI()
#database
while True:
    try:
        # Connect to  postgres DB
        conn = psycopg2.connect(host ="localhost",dbname="fastapi", user="postgres",password="postgres",cursor_factory=RealDictCursor)
        cursor=conn.cursor()
        print("db connection was successful")
        break
    except Exception as e:
        time.sleep(2)
        print(e)
## Schmea design
class post(BaseModel):
    title:str
    content:str
    published:bool=True
post_data=[{"title":"senju","content":"hashirama","published":"online","rating":1,"id":1}]




@app.get("/posts")
async def root():

    cursor.execute("SELECT * FROM posts")
    post_data=cursor.fetchall()
    return {"Post_data":post_data}

@app.get("/sqlalchemy")
def test_get_sql( session: SessionDep):

    return{"status":"successful"}

@app.post("/posts",status_code=status.HTTP_201_CREATED)
def createpost(post:post) :
        cursor.execute("INSERT INTO posts (title,content,published) VALUES (%s, %s, %s)  RETURNING * ", (post.title,post.content,post.published))
        post_data=cursor.fetchone()
        conn.commit()
        return {"data":post_data}

@app.get("/posts/{post_id}")
def get_post(post_id:int) :
    # post=find_id(post_id)
    cursor.execute("SELECT * FROM posts where id =%s" ,(str(post_id)),)
    post=cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=" id not found")
   
    return {"post_details":post}

@app.delete("/posts/{post_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id:int):
    cursor.execute("DELETE FROM posts where id =%s RETURNING *", str(post_id))

    delete_post=cursor.fetchone()
    conn.commit()

    if delete_post is not None:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else :
        raise HTTPException (status.HTTP_404_NOT_FOUND,detail=f"{post_id} not found")

@app.put("/posts/{post_id}")

def update_post(post_id:int,post:post):

    try:
        cursor.execute("UPDATE posts set title =%s where id = %s RETURNING *",(post.title,post.content,str(post_id)))
        updated_post=cursor.fetchone()
        conn.commit()
        if updated_post is not None:
        
            return{"data":updated_post}
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"{post_id} not found")
    except Exception as e:

        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=f"server error {e}")
