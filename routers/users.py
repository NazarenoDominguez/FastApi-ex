from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from models import get_db
from models.tables import Alc_Users
from models.schemas import Dan_Users_Out, Dan_Users
from sqlalchemy.orm import Session

from security.hash import hash


router = APIRouter(prefix='/API/USERS', tags=['users'])

@router.post('/POST', status_code=status.HTTP_201_CREATED, response_model = Dan_Users_Out)
def post_data(base: Dan_Users, db : Session = Depends(get_db)):
    hashpass = hash(base.password)
    base.password = hashpass
    data = Alc_Users(**base.dict())   
    db.add(data)
    db.commit()
    db.refresh(data)
    return data



