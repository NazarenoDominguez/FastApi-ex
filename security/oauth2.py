from jose import JWTError, jwt

from datetime import datetime,timedelta

from models.schemas import TokenData
from models import get_db
from sqlalchemy.orm import Session

from fastapi import Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordBearer

from models.tables import Alc_Users
from config import settings

oauth2_schema = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data : dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    
    return encoded_jwt

def verify_access_token(token : str, credentials_exception):
    
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms = [ALGORITHM])
        
        id_decode : str = payload.get('id_user')
        
        if id_decode == None:
            raise credentials_exception
        token_data = TokenData(id_user = id_decode)
        
    except JWTError:
        raise credentials_exception
    
    return token_data
    

def get_current_user(token:str = Depends(oauth2_schema), db : Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail='Could not validate credentials',
                                          headers={'WWW-authenticate':'Bearer'})
    
    token = verify_access_token(token, credentials_exception)
    user = db.query(Alc_Users).filter(Alc_Users.id_user == token.id_user).first()
    
    return user