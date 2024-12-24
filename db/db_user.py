from fastapi import HTTPException, Response
from sqlalchemy.orm.session import Session
from schemas import UserBase
from db.models import DbUser
from db.hash import Hash

def create_user(db: Session, req: UserBase):
    # 중복 이메일 방지
    existing_user = db.query(DbUser).filter(DbUser.email == req.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # 비밀번호 강도 검사
    if len(req.password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters long")
    if not any(char.isdigit() for char in req.password):
        raise HTTPException(status_code=400, detail="Password must contain at least one number")
    if not any(char.isalpha() for char in req.password):
        raise HTTPException(status_code=400, detail="Password must contain at least one letter")
    
    # 유효한 이메일 형식인지 확인
    if "@" not in req.email or "." not in req.email:
        raise HTTPException(status_code=400, detail="Invalid email format")
    
    new_user = DbUser(
        username = req.username,
        email = req.email,
        password = Hash.bcrpyt(req.password)
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user) # refresh the auto created id column
    return new_user

# def get_all_users(db: Session):
#     return db.query(DbUser).all()

# def get_user(db:Session, id:int):
#     return db.query(DbUser).filter(DbUser.id == id).first()

def get_user_by_email(db:Session, email:str):
    return db.query(DbUser).filter(DbUser.email == email).first()

def update_user(db:Session, id:int, req:UserBase):
    user = db.query(DbUser).filter(DbUser.id == id)
    user.update({
        DbUser.username: req.username,
        DbUser.email: req.email,
        DbUser.password: Hash.bcrpyt(req.password)
    })
    
    db.commit()
    return 'ok'

def delete_user(db:Session, id:int):
    user = db.query(DbUser).filter(DbUser.id == id).first()
    db.delete(user)
    db.commit()
    return 'ok'

# def login(db:Session, req:UserBase, response: Response):
#     user = db.query(DbUser).filter(DbUser.email == req.email).first()
#     if not user or not Hash.verify(user.password, req.password):
#         raise HTTPException(status_code=401, detail="Invalid credentials")
#     # JWT 생성
#     token = create_access_token({"sub": user.email})

#     # JWT를 쿠키에 저장
#     response.set_cookie(key="access_token", value=token, httponly=True, secure=False)
#     return {"message": "Login successful"}
    