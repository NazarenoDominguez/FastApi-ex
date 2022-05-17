
from fastapi import APIRouter, Depends, HTTPException, status
from models.schemas import Dan_Like, Dan_product_Out
from sqlalchemy.orm import Session
from sqlalchemy import func
from models import get_db
from models.tables import Alc_Forms, Alc_Like,Alc_Users
from security.oauth2 import get_current_user

router = APIRouter(prefix='/API/LIKES')

@router.post('/',response_model=Dan_product_Out)
def like(lk : Dan_Like, 
         db : Session = Depends(get_db), 
         user : int = Depends(get_current_user)):
    
    """q = db.query(Alc_Forms.title,Alc_Users.email).join(
        Alc_Forms,Alc_Forms.id_user==Alc_Users.id_user,
        ).filter(Alc_Forms.public== True)
    exp = q.all()"""
    
    
    
    
    data = db.query(Alc_Like).filter(Alc_Like.id_form == lk.id_form,
                                        Alc_Like.id_user == user.id_user)
    target = data.first()
   
    
    
    if lk.dir:
        if target:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f'the user {user.id_user} already voted the post {lk.id_form}')
        if not target:
            try:
                data = Alc_Like(id_user = user.id_user, id_form = lk.id_form)
                db.add(data)
                db.commit()
                db.refresh(data)
                rt = db.query(Alc_Forms,func.count(Alc_Like.id_form).label("likes")).join(
                    Alc_Like,Alc_Like.id_form==Alc_Forms.id_form, isouter=True).group_by(
                        Alc_Forms.id_form).filter(Alc_Forms.id_form==lk.id_form).first()
                return rt
            except:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
            
    if not lk.dir:
        if target:
            data.delete(synchronize_session = False)
            db.commit()
        if not target:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
            
            
        
    