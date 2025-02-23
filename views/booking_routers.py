from schemas.bookingSchema import*
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from config.db_connect import get_db
from controller import booking

router = APIRouter(
    prefix="/booking",
    tags=['booking']
)
@router.post('/create_booking')
def create_booking(req: BookingBase, db: Session= Depends(get_db)):
    return booking.create_booking(db, req)
@router.get('/cancel_booking/{booking_id}')
def cancel_booking(booking_id: int, db: Session= Depends(get_db)):
    return booking.cancel_booking(db, booking_id)
@router.get('/list_my_bookings/{user_id}')
def list_my_bookings(user_id: int, db: Session= Depends(get_db)):
    return booking.list_my_bookings(db, user_id)