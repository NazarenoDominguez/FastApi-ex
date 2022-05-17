from pydantic import BaseModel, EmailStr
from typing import Optional, List



class Dan_Products(BaseModel):
    title : str
    description : str
    form_text : str
    public : Optional[bool] = False
    
class Dan_products_Get(BaseModel):
    id_user : Optional[int]
    id_form : int
    title : str
    description : str
    form_text : str
    public : bool
    
    class Config:
        orm_mode = True
#esto no tenia el id de usuario, fijarse de que no este rompiendo nada... hablo de lo de arriba  
class Dan_product_Out(BaseModel):
    Alc_Forms : Dan_products_Get
    likes : int
    
    class Config:
        orm_mode = True
    
    

class Dan_Products_POST(BaseModel):
    id_form : Optional[int]
    #id_user : int
    title : str
    
    class Config:
        orm_mode = True


class Dan_Users(BaseModel):
    id_user : Optional[int]
    name : str
    email : EmailStr
    password : str
    active : Optional[bool]

class Dan_Users_Out(BaseModel):
    id_user : Optional[int]
    name : str
    email : EmailStr
    
    class Config:
        orm_mode = True
   


class Dan_Users_Login(BaseModel):
    email : EmailStr
    password : str
    
class Token(BaseModel):
    access_token : str
    token_type : str
    
    """class Config:
        orm_mode = True"""
        
class TokenData(BaseModel):
    id_user : Optional[str]
    
    
class Dan_Like(BaseModel):
    id_form : int
    dir : bool


