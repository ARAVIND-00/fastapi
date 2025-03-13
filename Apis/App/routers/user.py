from fastapi import FastAPI,Response,status,HTTPException,APIRouter
from ..database import SessionDep
from .. import models,schemas,utils
from sqlmodel import select

router=APIRouter(prefix="/users",tags=["users"])

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.UserResponse)
def Createuser(user:schemas.UserCreate,db:SessionDep):
     try:
        
        hashed_password=utils.hash(user.password)
        user.password=hashed_password
        New_user=models.USER(**user.model_dump())
        db.add(New_user)
        db.commit()
        db.refresh(New_user)
        return New_user
     except Exception as e:
          raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="user already exists")
     
@router.get("/{user_id}",response_model=schemas.UserResponse)
def getuser(user_id:int,db:SessionDep):
    statement =select(models.USER).where(models.USER.id==user_id)
    user=db.exec(statement).first()
 
    if not user:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detial="user id not found")
    return user