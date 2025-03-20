from typing import Optional
from fastapi import Depends,Response,status,HTTPException,APIRouter
from ..database import SessionDep
from .. import models,schemas ,oauth
from sqlmodel import select

router=APIRouter(prefix="/posts",tags=["posts"])

@router.get("/",response_model=list[schemas.PostResponse])
async def root(db:SessionDep,current_user:int=Depends(oauth.get_current_user),limit:int=10,skip:int =0,search:Optional[str]=""):

    # cursor.execute("SELECT * FROM posts")
    # post_data=cursor.fetchall()
    statement = select(models.POST).filter(models.POST.title.contains(search)).limit(limit).offset(skip)
    post_data=db.exec(statement).all()
    return post_data


@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.PostResponse)
async def createpost(post:schemas.create_post,db:SessionDep,current_user:int=Depends(oauth.get_current_user)) :
        # cursor.execute("INSERT INTO posts (title,content,published) VALUES (%s, %s, %s)  RETURNING * ", (post.title,post.content,post.published))
        # post_data=cursor.fetchone()
        # conn.commit()
        print(current_user.Email)
        New_data=models.POST(userid=current_user.id,**post.model_dump())
        db.add(New_data)
        db.commit()
        db.refresh(New_data)
        return New_data

@router.get("/{post_id}",response_model=schemas.PostResponse)
async def get_post(post_id:int,db:SessionDep,current_user:int=Depends(oauth.get_current_user)) :
    # post=find_id(post_id)
    # cursor.execute("SELECT * FROM posts where id =%s" ,(str(post_id)),)
    # post=cursor.fetchone()
    statement=select(models.POST).filter(models.POST.id==post_id)
    post_id_data=db.exec(statement).first()
    if not post_id_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=" id not found")   
    return post_id_data

@router.delete("/{post_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id:int,db:SessionDep,current_user:int=Depends(oauth.get_current_user)):
    # cursor.execute("DELETE FROM posts where id =%s RETURNING *", str(post_id))

    # delete_post=cursor.fetchone()
    # conn.commit()

    statement=select(models.POST).where(models.POST.id==post_id)
    query= db.exec(statement)
    results=query.first()
    
    if results is not None:
        if results.userid != current_user.id:
             raise HTTPException (status_code=status.HTTP_403_FORBIDDEN,detail="cannot allow the rqs")

        else:
                delete_post=db.delete(results)
                db.commit()
                return Response(status_code=status.HTTP_204_NO_CONTENT)

        
    else :
        raise HTTPException (status.HTTP_404_NOT_FOUND,detail=f"{post_id} not found")

@router.put("/{post_id}",response_model=schemas.PostResponse)
async def update_post(post_id:int,Updated_post:schemas.create_post,db:SessionDep,current_user:int=Depends(oauth.get_current_user)):

    
            # cursor.execute("UPDATE posts set title =%s where id = %s RETURNING *",(post.title,post.content,str(post_id)))
            # updated_post=cursor.fetchone()
            # conn.commit()
            statement= select(models.POST).where(models.POST.id==post_id)
            result=db.exec(statement).first()
            #new_data=models.POST(post.model_dump())
            
            
            if result is not None:
                if result.userid != current_user.id:
                    raise HTTPException (status_code=status.HTTP_403_FORBIDDEN,detail="cannot allow the rqs")
                else:
                
                    updated_post= result.sqlmodel_update(Updated_post.model_dump())
                    db.commit()
                    db.refresh(result)
                
                    return result
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"{post_id} not found")