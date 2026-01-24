from fastapi import FastAPI,Depends
from contextlib import asynccontextmanager
from app.util.db import create_tables
from app.router.auth import authRouter
from app.router.message import messageRouter
from app.util.protectRoute import get_current_user
from app.db.schemas.user import UserOutput
from fastapi.security import OAuth2AuthorizationCodeBearer


@asynccontextmanager
async def lifespan(app: FastAPI):
    #Initialize DB at start
    create_tables()
    #things before the app starts over yield
    yield #separation point
    #things as the app closes

app=FastAPI(lifespan=lifespan)
app.include_router(router=authRouter,tags=["auth"])
app.include_router(dependencies=[Depends(get_current_user)],router=messageRouter,tags=["message"])


@app.get("/health")
def health_check():
    return {"status":"Running..."}

@app.get("/protected")
def read_protected(user:UserOutput=Depends(get_current_user)):
    return{"data":user}
    
    
