from typing import Optional, List
from pydantic import BaseModel

# Note inside UserDisplay
class Note(BaseModel):
    title: str
    content: str
    class Config():
        from_attributes = True

class UserBase(BaseModel):
    id: Optional[int] = None
    username: Optional[str] = None
    email: str
    password: str
    
class UserDisplay(BaseModel):
    username:str
    email: str
    items: List[Note] = []
    class Config():
        from_attributes = True
        
class NoteBase(BaseModel):
    title: str
    content: str
    creator_id: Optional[int] = None

# user inside ArticleDisplay
class User(BaseModel):
    id: int
    username: str
    class Config():
        from_attributes = True

class NoteDisplay(BaseModel):
    title: str
    content: str
    user: User
    id: int
    class Config():
        from_attributes = True