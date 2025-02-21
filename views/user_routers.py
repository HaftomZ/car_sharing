from schemas.userSchema import UserBase, userDisplay
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from config.db_connect import get_db
from controller import users

router = APIRouter(
    prefix="/user",
    tags=['user']
)


@router.post('/', response_model= userDisplay)
def create_user(req: UserBase, db: Session= Depends(get_db)):
    return users.create_user(db, req)

@router.get('/', response_model=list[userDisplay])
def get_all_users(db: Session = Depends(get_db)):
    return users.get_all_users(db)

@router.get('/{id}', response_model=userDisplay)
def get_user(id: int, db: Session = Depends(get_db)):
    return users.get_one_user(db, id)

@router.post('/{id}/update')
def update_user(id: int, request: UserBase, db: Session = Depends(get_db)):
    return users.update_user(db, id, request)

@router.get('/delete/{id}')
def delete_user(id: int, db: Session = Depends(get_db)):
    return users.delete_user(db, id)