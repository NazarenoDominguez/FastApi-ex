from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from models import get_db
from models.tables import Alc_Forms
from models.schemas import Dan_Products, Dan_Products_POST,Dan_products_Get
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_

from security.oauth2 import get_current_user

router = APIRouter(prefix='/API/FORMS', tags=['forms'])


## %20 is space in url
@router.get('/GETALL', response_model = List[Dan_products_Get])
def get_all(db : Session = Depends(get_db),
              user : int = Depends(get_current_user),
              limit : Optional[int] = 100,
              search : Optional[str] = ""):
    data = db.query(Alc_Forms).filter(
        Alc_Forms.id_user == user.id_user).filter(
            Alc_Forms.title.contains(search)).limit(limit).all()
    return data


@router.post('/POST',status_code=status.HTTP_201_CREATED, response_model = Dan_Products_POST)
def post_data(base: Dan_Products,
              db : Session = Depends(get_db),
              user : int = Depends(get_current_user)):
  
    
    data = Alc_Forms(id_user = user.id_user, **base.dict())
    db.add(data)
    db.commit()
    db.refresh(data)
    return data


@router.get('/GET/{id}', response_model = Dan_products_Get)
def get_Id(id : int, db : Session = Depends(get_db),
              user : int = Depends(get_current_user)):
    
    data = db.query(Alc_Forms).filter(or_(Alc_Forms.id_form == id,Alc_Forms.id_user == user.id_user)).first()
    if not data:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, 
                            detail="invalid credentials")
    return data

@router.delete('/DELETE/{id}')
def del_Id(id: int, db : Session = Depends(get_db),
              user : int = Depends(get_current_user)):
    target = db.query(Alc_Forms).filter(Alc_Forms.id_form == id)
    
    if not target.first():
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"Id {id} NOT FOUND")
    
    target.delete(synchronize_session = False)
    db.commit()
    return Response(status_code = status.HTTP_204_NO_CONTENT)


@router.put('/UPDATE')
def del_Id(base : Dan_Products , db : Session = Depends(get_db),
              user : int = Depends(get_current_user)):
    target = db.query(Alc_Forms).filter(Alc_Forms.id_form == base.id_form)

    if not target.first():
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"Id {base.id_form} NOT FOUND")
    
    target.update(base.dict(), synchronize_session = False)
    
    db.commit()
    return {'Update':target.first()}
    
