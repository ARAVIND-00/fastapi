import select
from fastapi import APIRouter,HTTPException,status
from .. import schemas,database,models,utils,oauth
from sqlmodel import select
router=APIRouter(tags=["authentications"])

@router.post("/login")
def login_user(user_credentials:schemas.loginuser,db:database.SessionDep):
    print("sssssssss")
    statement=select(models.USER).where(models.USER.Email==user_credentials.Email)
    user=db.exec(statement).first()
    print("LLLLL",user)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="invalid credentials")
    
    if not utils.verify(user_credentials.password,user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="invalid credentials")
    

    access_token=oauth.create_token(data={"user_id":user.id})
        
    return{"token":access_token,"token_type":"bearer"}