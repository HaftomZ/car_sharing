from schemas.tripSchema import TripBase, TripResponse
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from config.db_connect import get_db
from controller import trips

router = APIRouter(
    prefix="/trips",
    tags=['trips']
)
@router.post('/create_trips')
def create_trips( req:TripBase, db: Session= Depends(get_db)):
    return trips.create_Trips(db, req)