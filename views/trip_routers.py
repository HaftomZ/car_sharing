from schemas.tripSchema import TripBase, TripDisplay
from fastapi import APIRouter, Depends , status
from sqlalchemy.orm import Session
from config.db_connect import get_db
from controller import trips
from typing import List
from datetime import datetime
from enum import Enum

router = APIRouter(
    prefix="/trips",
    tags=['trips']
)


#get all trips that are related to a user
@router.get('/', response_model=List[TripDisplay])
def get_all_user_trips(user_id: int, db: Session=Depends(get_db)):
    return trips.get_all_user_trips(db, user_id)

#create a trip
@router.post('/',  response_model=TripDisplay , status_code=status.HTTP_201_CREATED)
def create_trip( req:TripBase, db: Session= Depends(get_db)):
    return trips.create_trip(db, req)

#update a trip
@router.put('/{trip_id}',  response_model=TripDisplay)
def update_trip( req:TripBase, trip_id: int, db: Session= Depends(get_db)):
    return trips.update_trip(db, req, trip_id)

#search trip
@router.get('/search', response_model=List[TripDisplay])
def searsh_trip(departure_location: str, destination_location: str, departure_time: datetime,
                 available_adult_seats: int, available_children_seats: int  , db: Session=Depends(get_db)):
    return trips.search_trip(db, departure_location, destination_location, departure_time, available_adult_seats, available_children_seats)

#delete trip
@router.delete('/{trip_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_trip(trip_id: int, user_id: int, db: Session=Depends(get_db)):
    return trips.delete_trip(db, user_id, trip_id)