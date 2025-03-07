from schemas.bookingSchema import*
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from config.db_connect import get_db
from controller import booking
from models.Booking import DbBooking
from enum import Enum

router = APIRouter(
    prefix="/bookings",
    tags=['booking']
)

@router.post('/', response_model=BookingDisplay)
def create_booking(req: BookingBase, booker_id:int, trip_id: int,db: Session= Depends(get_db)):
    return booking.create_booking(db,  booker_id, trip_id,req)
  
@router.delete('/{booking_id}')
def cancel_booking(booking_id: int, db: Session= Depends(get_db)):
    return booking.cancel_booking(db,booking_id)

@router.put('/{booking_id}')
def update_my_bookings(booking_id: int, req: BookingBase, db: Session= Depends(get_db)):
    return booking.update_my_bookings(db,booking_id, req)

@router.get('/{user_id}', response_model= list[listBookingResponse])
def list_my_bookings(user_id: int, db: Session= Depends(get_db)):
    return booking.list_my_bookings(db, user_id)
@router.get('/')
def list_all_booking(db:Session=Depends(get_db)):
    return booking.list_all_booking(db)