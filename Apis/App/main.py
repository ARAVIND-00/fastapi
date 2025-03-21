
import uvicorn
from .database import create_db_and_tables
from fastapi import FastAPI
from contextlib import asynccontextmanager
from .routers import post,user,auth,vote

@asynccontextmanager
async def lifespan(app: FastAPI):
        try:
                create_db_and_tables()
                yield
        except Exception as e:
                print(f"Error during lifespan: {e}")
                raise
        finally:
                print("Application is shutting down.")

app = FastAPI(lifespan=lifespan)

app.include_router(post.router)
app.include_router(user.router) 
app.include_router(auth.router) 
app.include_router(vote.router)
