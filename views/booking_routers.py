from schemas.bookingSchema import*
from fastapi import APIRouter, Depends,status
from sqlalchemy.orm import Session
from config.db_connect import get_db
from controller import booking
from models.Booking import DbBooking
from enum import Enum

router = APIRouter(
    prefix="/bookings",
    tags=['booking']
)

@router.post('/', response_model=BookingDisplay, status_code=status.HTTP_201_CREATED)
def create_booking(req: BookingBase, booker_id:int, trip_id: int,db: Session= Depends(get_db)):
    return booking.create_booking(db,  booker_id, trip_id,req)
  
@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def cancel_booking(booker_id:int,booking_id: int, db: Session= Depends(get_db)):
    return booking.cancel_booking(db,booker_id,booking_id)

@router.put('/{id}')
def update_my_bookings(booker_id:int,booking_id: int, req: BookingBase, db: Session= Depends(get_db)):
    return booking.update_my_bookings(db,booker_id,booking_id, req)

@router.get('/', response_model= list[listBookingResponse])
def list_of_bookings(user_id: int= None, db: Session= Depends(get_db)):
    return booking.list_of_bookings(db, user_id)

@router.get('/{id}')
def get_a_booking(booking_id:int, db: Session= Depends(get_db)):
    return booking.get_a_booking(db,booking_id)
