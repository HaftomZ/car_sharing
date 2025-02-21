from config.Hash import Hash
from  sqlalchemy.orm.session import Session
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