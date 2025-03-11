from fastapi import HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi.param_functions import Depends
from sqlalchemy.orm.session import Session
from config.db_connect import get_db
from config import Hash , oauth2
from models.Users import DbUser
from jose import jwt
from jose.exceptions import JWEError


def create_token(request: OAuth2PasswordRequestForm, db: Session):
    user= db.query(DbUser).filter(DbUser.user_name == request.username).first()

    if user:
        if not user.is_verified:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unverified account")
        if not Hash.Hash.verify(user.password, request.password):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid password")
        access_token = oauth2.create_access_token(data={"sub": str(user.id)})
        return {"access_token": access_token}

    # elif admin:
    #     if not Hash.Hash.verify(admin.password, request.password):
    #         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid password")
    #     access_token = oauth2.create_access_token(data={"sub": str(admin.id), "role": "admin"})
    #     return {"access_token": access_token}

    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials")


def get_current_user(token: str = Depends(oauth2.oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                        detail='Could not validate credentials', 
                                        headers={"WWW-Authenticate":"Bearer"})
    try:
        payload= jwt.decode(token, oauth2.SECRET_KEY,algorithms=[oauth2.ALGORITHM])
        user_id = payload.get("sub")
        #role = payload.get("role")
        if user_id is None: # or role is None:
            raise credentials_exception
    except JWEError:
       raise credentials_exception
    
    #if role == "user":
    user = db.query(DbUser).filter(DbUser.id == int(user_id)).first()
    if not user:
        raise credentials_exception
    return user

    # elif role == "admin":
    #     admin = db.query(DbAdmin).filter(DbAdmin.id == int(user_id)).first()
    #     if not admin:
    #         raise credentials_exception
    #     return admin

    # raise credentials_exception