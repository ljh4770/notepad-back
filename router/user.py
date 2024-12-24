from typing import List
from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm.session import Session
from schemas import UserBase, UserDisplay
from db.database import get_db
from db import db_user
from auth.oauth2 import get_current_user

router = APIRouter(
    prefix='/api/user',
    tags=['user']
)

# Create user
@router.post('/create', response_model=UserDisplay)
def create_user(req:UserBase, db: Session = Depends(get_db)):
    return db_user.create_user(db, req)

# Fetch all user
@router.get('/all', response_model=List[UserDisplay])
def get_all_users(db:Session = Depends(get_db)):
    return db_user.get_all_users(db)

# Read user
@router.get('/{id}', response_model=UserDisplay)
def get_user(id:int, db:Session = Depends(get_db),
             current_user:UserBase = Depends(get_current_user)):
    return db_user.get_user(db, id)

# Update user
@router.post('/update/{id}')
def update_user(id:int, req:UserBase, db:Session = Depends(get_db),
                current_user:UserBase = Depends(get_current_user)):
    return db_user.update_user(db, id, req)

# Delete user
@router.get('/delete/{id}')
def delete_user(id:int, db:Session = Depends(get_db),
                current_user:UserBase = Depends(get_current_user)):
    return db_user.delete_user(db, id)

# Login
@router.post('/login')
def login(req:UserBase, res:Response, db:Session = Depends(get_db),):
    return db_user.login(db, req, res)