from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from .. import models
from .. import schemas

def get_all(db:Session):
    allBlogs=db.query(models.Blog).all()
    return allBlogs

def create(request:schemas.Blog,db:Session):
    if not request.published:
        new_blog=models.Blog(title=request.title,body=request.body,user_id=1)
    else:
        new_blog=models.Blog(title=request.title,body=request.body,user_id=1,published=request.published)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

def get(id:int,db:Session):
    blog=db.query(models.Blog).filter(models.Blog.id==id).first()
    if not blog:
        raise HTTPException(status.HTTP_404_NOT_FOUND,detail=f'no record with id {id}')
    return blog

def destroy(id:int,db:Session):
    blog=db.query(models.Blog).filter(models.Blog.id==id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'no record with id {id}')
    blog.delete(synchronize_session=False)
    db.commit()
    return {'detail':f'record deleted with id {id}'}

def update(id:int,request:schemas.Blog,db:Session):
    blog=db.query(models.Blog).filter(models.Blog.id==id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'no record with id {id}')
    blog.update(request.model_dump())
    db.commit()
    return {'detail':f'record updated with id {id}'}
