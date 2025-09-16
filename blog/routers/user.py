from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import schemas, database
from ..repository import user as UserRepository

router=APIRouter(
    prefix='/user',
    tags=['Users']
)

get_db=database.get_db

@router.post('/',response_model=schemas.ShowUser)
def createUser(request:schemas.User,db:Session=Depends(get_db)):
    return UserRepository.create(request,db)

@router.get('/',response_model=List[schemas.ShowUser])
def getAll(db:Session=Depends(get_db)):
    return UserRepository.get_all(db)

@router.get('/{id}',response_model=schemas.ShowUser)
def getAll(id:int,db:Session=Depends(get_db)):
    return UserRepository.get(id,db)
