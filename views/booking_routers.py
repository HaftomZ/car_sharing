from schemas.bookingSchema import*
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from config.db_connect import get_db
from controller import booking

router = APIRouter(
    prefix="/booking",
    tags=['booking']
)
@router.post('', response_model=BookingResponse)
def create_booking(req: BookingBase, db: Session= Depends(get_db)):
    return booking.create_booking(db, req)