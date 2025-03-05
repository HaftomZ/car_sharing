from fastapi import APIRouter , Depends
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
prefix='/Cars',
tags=['Cars']
)

class car_availability(str, Enum):
    available = "Available"
    unavailable = "Unavailable"

#create car for a user
@router.post('/create/{user_id}', response_model=CarDisplay)
def create_car(request: CarBase ,user_id: int, db: Session=Depends(get_db), current_user: UserBase = Depends(get_current_user) ):
    return cars.create_car(db, request, user_id)

#get all cars that are related to a user
@router.get('/get/{user_id}', response_model=List[CarDisplay])
def get_all_user_cars(user_id: int, db: Session=Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    return cars.get_all_user_cars(db, user_id)

#update car that is related to a user
@router.put('/update/{user_id}/{car_id}')
def update_user_car(request: CarBase, user_id: int, car_id: int, db: Session=Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    return cars.update_user_car(db, user_id, car_id, request)


#update car availability status
@router.put('/update_availability/{user_id}/{car_id}')
def update_car_availability_status(user_id: int, car_id: int, status: car_availability,db: Session=Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    return cars.update_car_availability_status(db, user_id, car_id, status.value)

#delete car that is related to a user
@router.delete('/delete/{user_id}/{car_id}')
def delete_user_car(user_id: int, car_id: int, db: Session=Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    return cars.delete_user_car(db, user_id, car_id)