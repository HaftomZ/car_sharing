from config.Hash import Hash
from sqlalchemy.orm.session import Session
from schemas.userSchema import UserBase
from models.Users import DbUser
from fastapi import HTTPException, status

def create_user(db: Session, request: UserBase):
    new_user = DbUser(
        user_name = request.username,
        email = request.email,
        password = Hash.bcrypt(request.password),
        about = request.about,
        phone_number = request.phone_number,
        avatar = request.avatar       
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_all_users(db:Session):
    all_users = db.query(DbUser).all()
    if not all_users:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f'there are no users exist!')
    return all_users

def login_user(db: Session, email: str, password: str):
    user = db.query(DbUser).filter(DbUser.email == email).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid data! User does not exist."
        )

    if not Hash.verify(user.password, password):  
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid password! Incorrect password."
        )

    # return {
    #     "user_name": user.user_name,
    #     "email": user.email,
    #     "message": "Login successful!"
    # }
    return user 


def update_user(db: Session, id:int, request: UserBase):
    user = db.query(DbUser).filter(DbUser.id == id)
    if not user.first():
         raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                             detail = f'user with id {id} is not exist!')
    user.update({
        DbUser.user_name : request.username,
        DbUser.email: request.email,
        DbUser.password: Hash.bcrypt(request.password),
        DbUser.about: request.about,
        DbUser.avatar: request.avatar,
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