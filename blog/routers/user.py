from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, models, database
from ..hashing import Hash

router=APIRouter(
    prefix='/user',
    tags=['Users']
)

get_db=database.get_db

@router.post('/',response_model=schemas.ShowUser)
def createUser(request:schemas.User,db:Session=Depends(get_db)):
    new_user=models.User(name=request.name,email=request.email,password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/',response_model=List[schemas.ShowUser])
def getAll(db:Session=Depends(get_db)):
    allUsers=db.query(models.User).all()
    return allUsers

@router.get('/{id}',response_model=schemas.ShowUser)
def getAll(id:int,db:Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'no record with id {id}')
    return user
