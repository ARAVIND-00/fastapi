
import jwt
from jwt.exceptions import InvalidTokenError
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends,HTTPException, status
from datetime import datetime,timedelta,timezone
from . import schemas ,database,models
from sqlmodel import select
from .config import settings
oauth2_scheme=OAuth2PasswordBearer(tokenUrl="login")
# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorthm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def create_token(data:dict):
    to_encode=data.copy()
    expire= datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    encoded_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

    return encoded_jwt

def verify_access_token(token:str,credential_exception):
    try:   
        payload :str = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        id:int =payload.get("user_id")

        if id is None:
            raise credential_exception
        token_data=schemas.token_data(id=id)
    except InvalidTokenError :
        raise credential_exception
    return token_data
    
def get_current_user(db:database.SessionDep,token:str=Depends(oauth2_scheme)):
    credential_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="invalid credentials",
                                       headers={"WWW-Authenticate": "Bearer"})
    token=verify_access_token(token,credential_exception)
    statement=select(models.USER).where(models.USER.id==token.id)
    user=db.exec(statement).first()

    return user