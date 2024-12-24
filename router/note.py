from typing import List
from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm.session import Session
from fastapi.security import OAuth2PasswordBearer
from schemas import NoteBase, NoteDisplay, UserBase
from db.database import get_db
from db import db_note
from auth.oauth2 import get_current_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter(
    prefix='/api/note',
    tags=['note']
)

# Create note
@router.post('/', response_model=NoteDisplay)
def create_note(req:NoteBase, db:Session = Depends(get_db),
                current_user:UserBase = Depends(get_current_user)):
    return db_note.create_note(db, req, current_user)

# Get all notes from a user
@router.get('/all', response_model=List[NoteDisplay])
def get_all_note(db:Session = Depends(get_db),
                 current_user:UserBase = Depends(get_current_user)):
    return db_note.get_all_notes(db, current_user.email)

# Get a note
@router.get('/{id}', response_model=NoteDisplay)
def get_note(id:int, db:Session = Depends(get_db),
             current_user:UserBase = Depends(get_current_user)):
    return db_note.get_note(db, id)

# Update a note
@router.post('/update/{id}', response_model=NoteDisplay)
def update_note(id:int, db:Session = Depends(get_db),
                current_user:UserBase = Depends(get_current_user)):
    return db_note.update_note(db, id)

# Delete a note
@router.post('/delete/{id}')
def delete_note(id:int, db:Session = Depends(get_db),
                current_user:UserBase = Depends(get_current_user)):
    return db_note.delete_note(db, id)
