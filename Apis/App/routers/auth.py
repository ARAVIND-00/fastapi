import select
from fastapi import APIRouter, Depends,HTTPException,status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import schemas,database,models,utils,oauth
from sqlmodel import select
router=APIRouter(tags=["authentications"])

@router.post("/login",response_model=schemas.token)
def login_user(db:database.SessionDep,user_credentials:OAuth2PasswordRequestForm=Depends()):
    statement=select(models.USER).where(models.USER.Email==user_credentials.username)
    user=db.exec(statement).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="invalid credentials")
    
    if not utils.verify(user_credentials.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="invalid credentials")
    

    access_token=oauth.create_token(data={"user_id":user.id})
        
    return{"token":access_token,"token_type":"bearer"}
