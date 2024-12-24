from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm.session import Session
from schemas import UserBase
from db.database import get_db
from db import models
from db.hash import Hash
from auth import oauth2

router = APIRouter(
    tags=['authentication']
)

@router.post('/api/login')
def get_token(req:UserBase,
              db:Session = Depends(get_db)):
    user = db.query(models.DbUser).filter(models.DbUser.email == req.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Invalid credentials")
    if not Hash.verify(user.password, req.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Incorrect password")
    
    access_token = oauth2.create_access_token(data={'sub': user.email})
    
    return {
        "access_token": access_token,
        "token_type":"bearer",
        "username": user.username
    }
    
@router.post("/api/logout")
def logout(response: Response):
    # 쿠키 삭제
    response.delete_cookie(key="access_token")
    return {"message": "Logout successful"}
