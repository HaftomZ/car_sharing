from schemas.userSchema import UserBase, userDisplay
from fastapi import APIRouter, Depends, File, UploadFile, status
from sqlalchemy.orm import Session
from config.db_connect import get_db
from controller import users
from controller.authentication import get_current_user

router = APIRouter(
    prefix="/users",
    tags=['users']
)


@router.post('/', response_model=userDisplay)
def create_user(req: UserBase, db: Session = Depends(get_db)):
    return users.create_user(db, req)


@router.put("/{id}/avatar")
def upload_avatar(id: int, file: UploadFile = File(...), db: Session = Depends(get_db),
                  current_user: userDisplay = Depends(get_current_user)):
    return users.upload_avatar(db, id, current_user, file)

@router.delete("/{id}/avatar", status_code=status.HTTP_204_NO_CONTENT)
def delete_avatar(id: int, db: Session = Depends(get_db), current_user: userDisplay = Depends(get_current_user)):
    return users.delete_avatar(db, id, current_user)

@router.get('/', response_model=list[userDisplay])
def get_all_users(db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    return users.get_all_users(db)

@router.get('/{id}', response_model=userDisplay)
def get_user_by_id(id: int, db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    return users.get_user_by_id(db, id)

@router.put('/{id}')
def update_user(id: int, request: UserBase, db: Session = Depends(get_db),
                current_user: userDisplay = Depends(get_current_user)):
    return users.update_user(db, id, request, current_user)

@router.delete('/{id}')
def delete_user(id: int, db: Session = Depends(get_db), current_user: userDisplay = Depends(get_current_user)):
    return users.delete_user(db, id, current_user)

