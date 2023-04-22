from fastapi import APIRouter,status,HTTPException,Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import schemas,utils,oauth2
from .. import main


router = APIRouter(tags=['Authetication'])

@router.post('/login')
def login(user: schemas.User):
    main.cursor.execute('''SELECT * FROM users WHERE email = %s''',(str(user.email),))
    checked_user = main.cursor.fetchone()
    

    if not checked_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Invalid user with email{user.email}")
    
    if not utils.verify(user.password,checked_user["password"]):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Wrong password with email{user.email}")
    
    #Create Token
    
    access_token = oauth2.Create_access_token(data={"userid": checked_user["id"]})
    #REturnToken
    return {"token": access_token,"token_type": "bearer"}