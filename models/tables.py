from sqlalchemy import TIMESTAMP, Column, String, Integer, Float, Boolean, ForeignKey
from sqlalchemy_utils import EmailType
from sqlalchemy.sql.expression import text
from models import Base
from sqlalchemy.orm import relationship


class Alc_Forms(Base):
    __tablename__ = "forms"
    id_form = Column(Integer, primary_key = True, nullable = False)
    id_user = Column(Integer,  ForeignKey('users.id_user', ondelete="CASCADE"), nullable = False)
    title = Column(String, nullable = False)
    description = Column(String, nullable = False)
    form_text = Column(String, nullable = False)
    public = Column(Boolean, server_default = "FALSE")
    created = Column(TIMESTAMP(timezone=True),nullable = False, server_default = text('now()'))
    
    owner = relationship('Alc_Users')



class Alc_Users(Base):
    __tablename__ = 'users'
    id_user = Column(Integer, primary_key = True, nullable = False)
    name = Column(String, nullable = False)
    email = Column(EmailType, nullable = False, unique = True)
    active = Column(Boolean, server_default = "FALSE")
    password = Column(String, nullable = False)
    

class Alc_Like(Base):
    __tablename__ = 'likes'
    id_user = Column(Integer, ForeignKey(
        'users.id_user', ondelete="CASCADE"),primary_key = True)
    id_form = Column(Integer, ForeignKey(
        'forms.id_form', ondelete="CASCADE"),primary_key = True)
