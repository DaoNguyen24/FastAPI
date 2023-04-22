from typing import Optional
from pydantic import BaseModel,EmailStr
import email_validator
from datetime import datetime


class Post(BaseModel):
    title: str
    content : str
    published: bool = True
    
    

class CreatePost(Post):
    id: int
    user_id : Optional[int]
    created_at : Optional[datetime]




    
class User(BaseModel):
    email : EmailStr
    password : str

class CreateUser(User):
    id : int

class ShowUSer(BaseModel):
    id : int
    email : EmailStr
    
class Token(BaseModel):
    access_token: str
    token_type : str

class TokenData(BaseModel):
    id : Optional[str] = None
