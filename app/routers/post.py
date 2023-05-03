from fastapi import APIRouter
from random import randrange
from typing import List, Optional
from fastapi import Response,status,HTTPException,Depends
from fastapi.params import Body
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor 
import time
from passlib.context import CryptContext
from .. import schemas,utils,oauth2
from .. import main






router = APIRouter(prefix="/posts", tags=["posts"])

@router.get("/",response_model=List[schemas.CreatePost],)
def get_post(limit:int =10, search: Optional[str] =''):
    #main.cursor.execute("""SELECT * FROM posts LIMIT %s""",(str(limit),))
    main.cursor.execute('''SELECT * FROM posts WHERE title LIKE %s LIMIT %s  ''', ('%'+search+'%',str(limit),))
    posts =main.cursor.fetchall() #use wwhen retrive many posts
    return posts


@router.post("/",status_code= status.HTTP_201_CREATED,response_model=schemas.CreatePost)#When create a post, should send Http 201
def create_posts(post : schemas.Post,user_id:int =Depends(oauth2.get_curent_user)):
    
    main.cursor.execute('''INSERT INTO posts (title,content, published,user_id) VALUES (%s,%s,%s,%s) RETURNING *''',(post.title,post.content,post.published,user_id.id))
    new_post = main.cursor.fetchone()
    main.connect.commit() #Đồng bộ thay đổi trên databse, dùng khi có thay đổi trên db
    return new_post





@router.get("/{id}",response_model=schemas.CreatePost)# The id is a string, remember to convert it to int
def get_post(id: int,response : Response): # Convert the id to int, if not, send back message
    main.cursor.execute('''SELECT * FROM posts WHERE id = %s''', (str(id),))
    post = main.cursor.fetchone()
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,detail=f"Post with id: {id} was not found ")
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"message": f"Post with id: {id} was not found "}
    return post


@router.delete("/{id}",response_model=schemas.CreatePost)
def delete_post(id: int,user_id:int =Depends(oauth2.get_curent_user)):
    main.cursor.execute('''DELETE FROM posts WHERE id = %s RETURNING *''',(str(id),))
    deleted_post = main.cursor.fetchone()
    
    print(deleted_post['user_id'])
    if deleted_post ==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} doesnt exist")

    if int(user_id.id) != deleted_post['user_id']:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"The post with id {deleted_post['id']} is not your post.You cannot delete it")

    main.connect.commit()

    
    return deleted_post 


@router.put("/{id}",response_model=schemas.CreatePost)
def update_post(id : int, post: schemas.Post,user_id:int =Depends(oauth2.get_curent_user)):
    
    main.cursor.execute('''UPDATE posts SET title = %s, content = %s WHERE id = %s RETURNING *''',(post.title,post.content,str(id),))
    updated_post = main.cursor.fetchone()

    if updated_post ==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} is notfound")
    if int(user_id.id) != updated_post['user_id']:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"The post with id {updated_post['id']} is not your post.You cannot update it")
    
    main.connect.commit()
    
    return updated_post