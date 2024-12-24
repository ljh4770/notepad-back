from fastapi import HTTPException, Request, Depends
from sqlalchemy.orm.session import Session 
from db.models import DbNote
from db.db_user import get_user_by_email
from schemas import NoteBase, UserBase
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Create a note
def create_note(db:Session, req:NoteBase, current_user:UserBase):
    user = get_user_by_email(db, current_user.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    new_note = DbNote(
        title = req.title,
        content = req.content,
        user_id = user.id
    )
    
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note

# Get a note
def get_note(db:Session, id:int):
    note = db.query(DbNote).filter(DbNote.id == id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

# Get all notes from a user
def get_all_notes(db:Session, email:str):
    user = get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # 사용자의 메모 조회
    return db.query(DbNote).filter(DbNote.user_id == user.id).all()

# Update a note
def update_note(db:Session, req:NoteBase):
    note = db.query(DbNote).filter(DbNote.id == id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    note.update({
        DbNote.title: req.title,
        DbNote.content: req.content
    })
    
    db.commit()
    return 'ok'

# Delete a note
def delete_note(db:Session, id:int):
    note = db.query(DbNote).filter(DbNote.id == id).first()
    db.delete(note)
    db.commit()
    return 'ok'