from schemas.tripSchema import TripBase, TripDisplay
from fastapi import APIRouter, Depends , status
from sqlalchemy.orm import Session
from config.db_connect import get_db
from controller import trips
from typing import List
from datetime import datetime
from enum import Enum
from schemas.userSchema import userDisplay 
from controller.authentication import get_current_user

router = APIRouter(
    prefix="/trips",
    tags=['trips']
)

#create a trip
@router.post('/',  response_model=TripDisplay , status_code=status.HTTP_201_CREATED)
def create_trip( req:TripBase, db: Session= Depends(get_db), current_user: userDisplay  = Depends(get_current_user)):
    return trips.create_trip(db, req, current_user)

#get all trips
@router.get('/', response_model=List[TripDisplay])
def get_all_trips(user_id: int = None, db: Session=Depends(get_db), current_user: userDisplay  = Depends(get_current_user)):
    return trips.get_all_trips(db, user_id)


#search trip
@router.get('/search', response_model=List[TripDisplay])
def searsh_trip(departure_location: str, destination_location: str, departure_time: datetime,
                 available_adult_seats: int, available_children_seats: int  , db: Session=Depends(get_db), current_user: userDisplay  = Depends(get_current_user)):
    return trips.search_trip(db, departure_location, destination_location, departure_time, available_adult_seats, available_children_seats)


#get trip
@router.get('/{id}', response_model=TripDisplay)
def get_trip(id: int, db: Session=Depends(get_db), current_user: userDisplay  = Depends(get_current_user)):
    return trips.get_trip(db, id)

#update a trip
@router.put('/{id}',  response_model=TripDisplay)
def update_trip( req:TripBase, id: int, db: Session= Depends(get_db), current_user: userDisplay  = Depends(get_current_user)):
    return trips.update_trip(db, req, id, current_user)


#delete trip
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_trip(id: int, db: Session=Depends(get_db), current_user: userDisplay = Depends(get_current_user)):
    return trips.delete_trip(db, id, current_user)