from config.Hash import Hash
from  sqlalchemy.orm.session import Session
from schema import UserBase
from models.Users import DbUser

def create_user(db: Session, request: UserBase):
    new_user = DbUser(
        username = request.username,
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