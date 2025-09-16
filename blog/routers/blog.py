from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from .. import schemas, database
from ..repository import blog as BlogRepository

router=APIRouter(
    prefix='/blog',
    tags=['Blogs']
)
get_db=database.get_db

@router.get('/',response_model=List[schemas.ShowBlog])
def getAll(db:Session=Depends(get_db)):
    return BlogRepository.get_all(db)

@router.post('/',status_code=status.HTTP_201_CREATED,response_model=schemas.ShowBlog)
def createBlog(request:schemas.Blog,db:Session=Depends(get_db)):
    return BlogRepository.create(request,db)

@router.get('/{id}',status_code=status.HTTP_200_OK,response_model=schemas.ShowBlog)
def getBlog(id:int,db:Session=Depends(get_db),):
   return BlogRepository.get(id,db)

@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def deleteBlog(id:int,db:Session=Depends(get_db)):
    return BlogRepository.destroy(id,db)

@router.patch('/{id}')
def updateBlog(id:int,request:schemas.Blog,db:Session=Depends(get_db)):
    return BlogRepository.update(id,request,db)