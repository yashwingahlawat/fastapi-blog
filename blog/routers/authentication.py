from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import database, models, schemas
from ..hashing import Hash
router=APIRouter(
    tags=['Authentication']
)

@router.post('/login',response_model=schemas.ShowUser)
def login(request:schemas.Login,db:Session=Depends(database.get_db)):
    user=db.query(models.User).filter(models.User.email==request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'user does not exist with username {request.username}')
    if not Hash.verifyPassword(request.password,user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f'Invalid Password')
    return user
    