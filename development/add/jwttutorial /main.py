from fastapi import Depends, FastAPI,HTTPException, status, Request
from app.routers import auth, user
from app.routers import auth
import models
from database import engine,SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session


app = FastAPI()
app.include_router(auth.router)

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.get("/", status_code=status.HTTP_200_OK)
def root(request: Request, db: db_dependency):
    # This acts as a standard API endpoint returning pure JSON
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    return {"user": user}