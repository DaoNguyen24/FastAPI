from jose import ExpiredSignatureError, JWSError, jwt
from datetime import datetime, timedelta
from . import schemas
from fastapi import Depends,status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from . import main

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

#SECRET_KEY
#ALGORITHM
#EXPIRATION TIME
SECRET_KEY = '8tu509ntguitug9tu095ug09urru0934895798t7ygihg9ty85g'
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTE = 30

def Create_access_token(data :dict):
   to_encode = data.copy()
   expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTE)
   to_encode["exp"] = expire

   encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

   return encoded_jwt


############################################# VERIFY USER ############################################################

def verify_access_token(token :str, exception):
   try:
      payload =jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
      id :str = payload.get("userid")

      if id is None:
         raise exception
      token_data = schemas.TokenData(id = id )
   except JWSError :
      raise exception
   except AssertionError:
      raise exception
   except ExpiredSignatureError:
      raise exception
   return token_data
   
def get_curent_user(token : str = Depends(oauth2_scheme) ):
   credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f"Could not valid credentials", headers={"WWW-Autheticate": "Bearer"})

   return verify_access_token(token,credentials_exception) 
#######################################################################################################