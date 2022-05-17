from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from models import get_db
from sqlalchemy.orm import Session
from models.tables import Alc_Users
from models.schemas import Token

from security.hash import verify
from security.oauth2 import create_access_token

router = APIRouter(prefix='/API/AUTH',tags=['auth'])

@router.post('/login',response_model=Token)
def login(credentials : OAuth2PasswordRequestForm = Depends(), db : Session = Depends(get_db)):
    user = db.query(Alc_Users).filter(Alc_Users.email == credentials.username).first()
    
    if user and verify(credentials.password,user.password):
        access_token = create_access_token({'id_user':user.id_user})
        return {'access_token': access_token,'token_type':'Bearer'}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='invalid credentials')
    