from sqlalchemy import Column, String
from sqlalchemy.sql.sqltypes import Integer
from sqlalchemy.schema import ForeignKey
from sqlalchemy.orm import relationship

from db.database import Base

class DbUser(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    items = relationship('DbNote', back_populates='user')
    
class DbNote(Base):
    __tablename__ = 'notes'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('DbUser', back_populates='items')