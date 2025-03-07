from config.Hash import Hash
from sqlalchemy.orm.session import Session
from schemas.userSchema import UserBase
from models.Users import DbUser
from fastapi import HTTPException, status, File, UploadFile
from pathlib import Path
from config.pictures_handler import upload_picture

def create_user(db: Session, request: UserBase):
    if len(request.about) >= 50:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="About section cannot be more than 50 characters!."
        )
    existing_user = db.query(DbUser).filter(DbUser.email == request.email).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists. Please choose a different email!."
        )
    new_user = DbUser(
        user_name = request.username,
        email = request.email,
        password = Hash.bcrypt(request.password),
        about = request.about,
        phone_number = request.phone_number
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


UPLOAD_DIR = Path("avatars")
UPLOAD_DIR.mkdir(exist_ok=True)


def upload_avatar(db: Session, id: int, file: UploadFile = File(...)):
    user = db.query(DbUser).filter(DbUser.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    old_avatar_path = Path(user.avatar)
    if old_avatar_path.exists():
        old_avatar_path.unlink()
    final_path = upload_picture(UPLOAD_DIR, file)
    user.avatar = str(final_path)
    db.commit()
    db.refresh(user)
    return user


def get_all_users(db:Session):
    all_users = db.query(DbUser).all()
    if not all_users:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f'there are no users found!')
    return all_users

def login_user(db: Session, email: str, password: str):
    user = db.query(DbUser).filter(DbUser.email == email).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid Email! Create an account first!."
        )

    if not Hash.verify(user.password, password):  
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid password! Incorrect password."
        )
       
    return user 


def update_user(db: Session, id:int, request: UserBase):
    if len(request.about) >= 50:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="About section cannot be more than 50 characters!."
        )
    user = db.query(DbUser).filter(DbUser.id == id)
    if not user.first():
         raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                             detail = f'user with id {id} is not exist!')
    user.update({
        DbUser.user_name : request.username,
        DbUser.email: request.email,
        DbUser.password: Hash.bcrypt(request.password),
        DbUser.about: request.about,
        DbUser.phone_number: request.phone_number,
    })
    db.commit()
    return 'user information has been updated successfully!'

def delete_user(db: Session, id: int):
    user = db.query(DbUser).filter(DbUser.id == id).first()
    if not user:
         raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                             detail = f'user with id {id} is not exist!')
    db.delete(user)
    db.commit()
    return 'user has been deleted!'