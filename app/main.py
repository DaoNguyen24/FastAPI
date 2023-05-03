from fastapi import FastAPI
from random import randrange
from typing import Optional
from fastapi import FastAPI,Response,status,HTTPException
from fastapi.params import Body
from pydantic import BaseModel,BaseSettings
import psycopg2
from psycopg2.extras import RealDictCursor 
import time
from passlib.context import CryptContext
from . import schemas,utils
from .routers import post,user,auth,vote

from .config import settings
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

#origins = ["https://www.google.com"]
origins = ["*"] #all domain can use the api

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,#Alow specific domain
    allow_credentials=True,
    allow_methods=["*"],#Alow specific http method
    allow_headers=["*"],
)



while True:
    try:
        connect = psycopg2.connect(host = settings.host,port = settings.database_port, database = settings.database_name, user = settings.database_username, password = settings.database_password, cursor_factory=RealDictCursor)
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
app.include_router(vote.router)

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