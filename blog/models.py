from .database import Base
from sqlalchemy import Column,Integer,String,Boolean

class Blog(Base):
    __tablename__='Blogs'
    id=Column(Integer,primary_key=True,index=True)
    title=Column(String(255),nullable=False)
    body=Column(String(255),nullable=False)
    published=Column(Boolean,default=False)