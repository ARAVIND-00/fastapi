from email import message
from fastapi import Depends,Response,status,HTTPException,APIRouter
from httpx import delete
from sqlmodel import select
from .. import models, schemas,database,oauth

router=APIRouter(prefix="/vote",tags=["vote"])

@router.post("/",status_code=status.HTTP_201_CREATED)
def vote(vote:schemas.vote,db:database.SessionDep,current_user:int=Depends(oauth.get_current_user)):
    post=db.exec (select(models.POST).where(models.POST.id==vote.post_id)).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= f"{vote.post_id} not exist")

        statement=select(models.VOTE).where(models.VOTE.post_id==vote.post_id,models.VOTE.user_id==current_user.id)
        found_data=db.exec(statement).first()
        if( vote.dir==1):
            if found_data:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="Has all ready voted")
            new_vote=models.VOTE(post_id=vote.post_id,user_id=current_user.id)
            db.add(new_vote)
            db.commit()
            return {"message":"successfully voted"}
        else:
            if not found_data:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,details="vote doesn't exist")
            
            delete_post=db.delete(found_data)
            db.commit()

            return {"message":"successfully deleted"}
            