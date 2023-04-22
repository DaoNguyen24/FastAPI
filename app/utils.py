from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")

def hash(password : str):
    hashed_password =pwd_context.hash(password)
    return hashed_password

def verify(plain_password,hashed_password):
    return pwd_context.verify(plain_password,hashed_password)
    #if hashed_password == pwd_context.hash(plain_password):
    #    return True
    #else: return False