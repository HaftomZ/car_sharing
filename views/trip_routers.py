from schemas.tripSchema import TripBase, TripDisplay
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from config.db_connect import get_db
from controller import trips

router = APIRouter(
    prefix="/trips",
    tags=['trips']
)
@router.post('/create/{user_id}/{car_id}',  response_model=TripDisplay)
def create_trip( req:TripBase,user_id: int, car_id: int, db: Session= Depends(get_db)):
    return trips.create_Trip(db, req, user_id, car_id)