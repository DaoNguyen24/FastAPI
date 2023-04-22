from fastapi import FastAPI
from random import randrange
from typing import Optional
from fastapi import FastAPI,Response,status,HTTPException
from fastapi.params import Body
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor 
import time
from passlib.context import CryptContext
from . import schemas,utils
from .routers import post,user,auth

pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")

app = FastAPI()





while True:
    try:
        connect = psycopg2.connect(host = 'localhost',port = 5433, database = 'fastapi', user = 'postgres', password = 'Nguyen2003', cursor_factory=RealDictCursor)
        cursor = connect.cursor()
        print("Connect to database was sucessful")
        break
    except Exception as err:
        print("Failed to connect to database")
        print("Error:", err)
        time.sleep(2)
    

#my_posts = [{"title" : "How i grow","content": "I grow besstt","id" : 1 },{"title" : "How i grow22","content": "I grow besstt22","id" : 2 }]

#def find_post(id):
#    for p in my_posts:
#        if p["id"] == id:
#            return p
#        
#def find_index_post(id):
#    for i, p in enumerate(my_posts):
#        if p["id"] == id:
#            return i
    
app.include_router(post.router)
app.include_router(auth.router)

@app.get("/")
async def root():
    return{"message":"Hellooooooooo World"}



@app.post("/users",status_code= status.HTTP_201_CREATED,response_model=schemas.CreateUser)
def create_user(user :schemas.User):

    #Hash the password
    
        user.password = utils.hash(user.password)

        cursor.execute('''INSERT INTO users (email, password ) VALUES (%s, %s) RETURNING *''',(user.email,user.password))
        new_user = cursor.fetchone()
        connect.commit()

        return new_user

@app.get("/users/{id}",response_model=schemas.ShowUSer)
def get_user(id :int):
    cursor.execute('''SELECT * FROM users WHERE id = %s''',(str(id)))
    user = cursor.fetchone()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} does not exist")
    
    return user