from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import uvicorn

app=FastAPI()

class Blog(BaseModel):
    title:str
    body:str
    published:Optional[bool]=None

@app.get('/')
def index():
    return {'ok':'hlo'}

@app.get('/blog/{id}')
def getBlog(id:int,limit:int=10,published:bool=True):
    if published:
        return {'blog':f'{id} has a limit of {limit}'}
    else:
        return {'blog':''}
    
# @app.post('/blog')
# def createBlog(request:Blog):
#     return {'data':f'blog created -> {request.title}'}

if __name__== "__main__":
    uvicorn.run(app,host='127.0.0.1',port=9000)