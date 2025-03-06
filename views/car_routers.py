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

router = APIRouter(
prefix='/cars',
tags=['cars']
)

class car_availability(str, Enum):
    available = "Available"
    unavailable = "Unavailable"

#create car for a user
@router.post('/', response_model=CarDisplay , status_code=status.HTTP_201_CREATED)
def create_car(request: CarBase , db: Session=Depends(get_db), current_user: UserBase = Depends(get_current_user) ):
    return cars.create_car(db, request)

#get all cars that are related to a user
@router.get('/', response_model=List[CarDisplay])
def get_all_user_cars(user_id: int, db: Session=Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    return cars.get_all_user_cars(db, user_id)

#update car that is related to a user
@router.put('/{car_id}', response_model=CarDisplay)
def update_user_car(request: CarBase, car_id: int, db: Session=Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    return cars.update_user_car(db, car_id, request)

#delete car that is related to a user
@router.delete('/{car_id}' , status_code=status.HTTP_204_NO_CONTENT)
def delete_user_car(car_id: int, user_id: int, db: Session=Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    return cars.delete_user_car(db, user_id, car_id)