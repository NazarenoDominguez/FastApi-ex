from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from models import *
from models.tables import *
Base.metadata.create_all(bind = engine)

from routers import forms, users, auth, likes

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(forms.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(likes.router)

@app.get('/API')
def fastAPIview():
    return {'API': 'API-dev'}

#uvicorn main:app --reload



