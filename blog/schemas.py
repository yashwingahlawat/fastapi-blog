from pydantic import BaseModel
from typing import Optional

class Blog(BaseModel):
    title:str
    body:str
    published:Optional[bool]=False


class User(BaseModel):
    name:str
    email:str
    password:str

class ShowUser(BaseModel):
    name:str
    email:str
    blogs:list[Blog]
    class Config():
        orm_mode=True

class ShowUserForBlog(BaseModel):
    name:str
    email:str
    class Config():
        orm_mode=True

class ShowBlog(BaseModel):
    title:str
    body:str
    published:Optional[bool]=False
    creator:ShowUserForBlog
    class Config():
        orm_mode=True
