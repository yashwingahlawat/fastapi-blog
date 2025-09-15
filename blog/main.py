from fastapi import FastAPI, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session

from . import schemas, models
from .database import engine, SessionLocal
from .hashing import Hash

app=FastAPI()

BlogTable=models.Blog
models.Base.metadata.create_all(engine)

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/blog',status_code=status.HTTP_201_CREATED,response_model=schemas.ShowBlog,tags=['Blogs'])
def createBlog(request:schemas.Blog,db:Session=Depends(get_db)):
    if not request.published:
        new_blog=BlogTable(title=request.title,body=request.body,user_id=1)
    else:
        new_blog=BlogTable(title=request.title,body=request.body,user_id=1,published=request.published)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.get('/blog',response_model=list[schemas.ShowBlog],tags=['Blogs'])
def getAll(db:Session=Depends(get_db)):
    allBlogs=db.query(BlogTable).all()
    return allBlogs

@app.get('/blog/{id}',status_code=status.HTTP_200_OK,response_model=schemas.ShowBlog,tags=['Blogs'])
def getBlog(id:int,response:Response,db:Session=Depends(get_db),):
    blog=db.query(BlogTable).filter(BlogTable.id==id).first()
    if not blog:
        raise HTTPException(status.HTTP_404_NOT_FOUND,detail=f'no record with id {id}')
    return blog

@app.delete('/blog/{id}',status_code=status.HTTP_204_NO_CONTENT,tags=['Blogs'])
def deleteBlog(id:int,db:Session=Depends(get_db)):
    blog=db.query(BlogTable).filter(BlogTable.id==id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'no record with id {id}')
    blog.delete(synchronize_session=False)
    db.commit()
    return {'detail':f'record deleted with id {id}'}

@app.patch('/blog/{id}',tags=['Blogs'])
def updateBlog(id:int,request:schemas.Blog,db:Session=Depends(get_db)):
    blog=db.query(BlogTable).filter(BlogTable.id==id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'no record with id {id}')
    blog.update(request.model_dump())
    db.commit()
    return {'detail':f'record updated with id {id}'}

@app.post('/user',response_model=schemas.ShowUser,tags=['Users'])
def createUser(request:schemas.User,db:Session=Depends(get_db)):
    new_user=models.User(name=request.name,email=request.email,password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get('/users',response_model=list[schemas.ShowUser],tags=['Users'])
def getAll(db:Session=Depends(get_db)):
    allUsers=db.query(models.User).all()
    return allUsers

@app.get('/users/{id}',response_model=schemas.ShowUser,tags=['Users'])
def getAll(id:int,db:Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'no record with id {id}')
    return user
