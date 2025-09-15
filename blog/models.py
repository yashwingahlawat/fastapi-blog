from .database import Base
from sqlalchemy import Column,Integer,String,Boolean,ForeignKey
from sqlalchemy.orm import relationship

class Blog(Base):
    __tablename__='Blogs'
    id=Column(Integer,primary_key=True,index=True,autoincrement=True)
    title=Column(String(255),nullable=False)
    body=Column(String(255),nullable=False)
    published=Column(Boolean,default=False)
    user_id=Column(Integer,ForeignKey('Users.id'))
    creator=relationship('User',back_populates='blogs')

class User(Base):
    __tablename__='Users'
    id=Column(Integer,primary_key=True,index=True,autoincrement=True,unique=True)
    name=Column(String(255),index=True)
    email=Column(String(191),nullable=False,unique=True)
    password=Column(String(255),nullable=False)
    blogs=relationship('Blog',back_populates='creator')