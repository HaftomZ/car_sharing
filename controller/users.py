from config.Hash import Hash
from sqlalchemy.orm.session import Session
from schemas.userSchema import UserBase
from models.Users import DbUser

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
    return db.query(DbUser).all()

def get_one_user(db: Session, id: int):
    return db.query(DbUser).filter(DbUser.id == id).first()

def update_user(db: Session, id:int, request: UserBase):
    user = db.query(DbUser).filter(DbUser.id == id)
    user.update({
        DbUser.user_name : request.username,
        DbUser.email: request.email,
        DbUser.password: Hash.bcrypt(request.password),
        DbUser.about: request.about,
        DbUser.avatar: request.avatar,
        DbUser.phone_number: request.phone_number
    })
    db.commit()
    return 'user information has been updated successfully!'

def delete_user(db: Session, id: int):
    user = db.query(DbUser).filter(DbUser.id == id).first()
    db.delete(user)
    db.commit()
    return 'user has been deleted!'