from fastapi import APIRouter , Depends , status
from schemas.carSchema import CarBase , CarDisplay
from sqlalchemy.orm import Session
from config.db_connect import get_db
from controller import cars
from typing import List
from enum import Enum
from config.oauth2 import oauth2_scheme
from controller.authentication import get_current_user
from schemas.userSchema import UserBase
from schemas.adminSchema import AdminBase

router = APIRouter(
prefix='/cars',
tags=['cars']
)

#create car for a user
@router.post('/', response_model=CarDisplay , status_code=status.HTTP_201_CREATED)
def create_car(request: CarBase , db: Session=Depends(get_db), current_user: UserBase | AdminBase = Depends(get_current_user) ):
    return cars.create_car(db, request)

#get all cars 
@router.get('/', response_model=List[CarDisplay])
def get_all_cars(user_id: int = None, db: Session=Depends(get_db), current_user: UserBase | AdminBase = Depends(get_current_user)):
    return cars.get_all_cars(db, user_id)


#get car
@router.get('/{id}', response_model=CarDisplay)
def get_car(id: int, db: Session=Depends(get_db), current_user: UserBase | AdminBase = Depends(get_current_user)):
    return cars.get_car(db, id)


#update car that is related to a user
@router.put('/{id}', response_model=CarDisplay)
def update_car(request: CarBase, id: int, db: Session=Depends(get_db), current_user: UserBase | AdminBase = Depends(get_current_user)):
    return cars.update_car(db, id, request)

#delete car that is related to a user
@router.delete('/{id}' , status_code=status.HTTP_204_NO_CONTENT)
def delete_car(id: int, db: Session=Depends(get_db), current_user: UserBase | AdminBase = Depends(get_current_user)):
    return cars.delete_car(db, id, current_user)