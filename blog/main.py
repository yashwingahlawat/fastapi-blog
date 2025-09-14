from fastapi import FastAPI, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session

from . import schemas, models
from .database import engine, SessionLocal

app=FastAPI()

BlogTable=models.Blog
models.Base.metadata.create_all(engine)

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/blog',status_code=status.HTTP_201_CREATED,response_model=schemas.ShowBlog)
def createBlog(request:schemas.Blog,db:Session=Depends(get_db)):
    new_blog=BlogTable(**request.model_dump())
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.get('/blog',response_model=list[schemas.ShowBlog])
def getAll(db:Session=Depends(get_db)):
    allBlogs=db.query(BlogTable).all()
    return allBlogs

@app.get('/blog/{id}',status_code=status.HTTP_200_OK,response_model=schemas.ShowBlog)
def getBlog(id:int,response:Response,db:Session=Depends(get_db),):
    blog=db.query(BlogTable).filter(BlogTable.id==id).first()
    if not blog:
        raise HTTPException(status.HTTP_404_NOT_FOUND,detail=f'no record with id {id}')
    return blog

@app.delete('/blog/{id}',status_code=status.HTTP_204_NO_CONTENT)
def deleteBlog(id:int,db:Session=Depends(get_db)):
    blog=db.query(BlogTable).filter(BlogTable.id==id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'no record with id {id}')
    blog.delete(synchronize_session=False)
    db.commit()
    return {'detail':f'record deleted with id {id}'}

@app.patch('/blog/{id}')
def updateBlog(id:int,request:schemas.Blog,db:Session=Depends(get_db)):
    blog=db.query(BlogTable).filter(BlogTable.id==id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'no record with id {id}')
    blog.update(request.model_dump())
    db.commit()
    return {'detail':f'record updated with id {id}'}

