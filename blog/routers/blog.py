from typing import List
from fastapi import APIRouter, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, models, database

router=APIRouter(
    prefix='/blog',
    tags=['Blogs']
)
get_db=database.get_db

@router.get('/',response_model=List[schemas.ShowBlog])
def getAll(db:Session=Depends(get_db)):
    allBlogs=db.query(models.Blog).all()
    return allBlogs

@router.post('/',status_code=status.HTTP_201_CREATED,response_model=schemas.ShowBlog)
def createBlog(request:schemas.Blog,db:Session=Depends(get_db)):
    if not request.published:
        new_blog=models.Blog(title=request.title,body=request.body,user_id=1)
    else:
        new_blog=models.Blog(title=request.title,body=request.body,user_id=1,published=request.published)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@router.get('/{id}',status_code=status.HTTP_200_OK,response_model=schemas.ShowBlog)
def getBlog(id:int,response:Response,db:Session=Depends(get_db),):
    blog=db.query(models.Blog).filter(models.Blog.id==id).first()
    if not blog:
        raise HTTPException(status.HTTP_404_NOT_FOUND,detail=f'no record with id {id}')
    return blog

@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def deleteBlog(id:int,db:Session=Depends(get_db)):
    blog=db.query(models.Blog).filter(models.Blog.id==id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'no record with id {id}')
    blog.delete(synchronize_session=False)
    db.commit()
    return {'detail':f'record deleted with id {id}'}

@router.patch('/{id}')
def updateBlog(id:int,request:schemas.Blog,db:Session=Depends(get_db)):
    blog=db.query(models.Blog).filter(models.Blog.id==id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'no record with id {id}')
    blog.update(request.model_dump())
    db.commit()
    return {'detail':f'record updated with id {id}'}
