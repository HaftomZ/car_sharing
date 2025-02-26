from schemas.bookingSchema import*
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from config.db_connect import get_db
from controller import booking
from enum import Enum

router = APIRouter(
    prefix="/booking",
    tags=['booking']
)
class BookingStatus(str,Enum):
    confirm ="confirm",
    pending = "pending",
    rejected = "rejected"
@router.post('/create_booking/{booker_id}/{trip_id}', response_model=BookingDisplay)
def create_booking(req: BookingBase, booker_id:int, trip_id: int,db: Session= Depends(get_db)):
    return booking.create_booking(db,  booker_id, trip_id,req)

@router.delete('/cancel_booking/{booking_id}')
def cancel_booking(booking_id: int, db: Session= Depends(get_db)):
    return booking.cancel_booking(db, booking_id)
@router.put('/update_booking_status/{user_id}/{trip_id}/{booking_id}/{booking_status}')
def update_booking_status(user_id: int, trip_id:int, booking_id: int, booking_status: BookingStatus, db: Session= Depends(get_db)):
   return booking.update_booking_status(db,user_id,trip_id,booking_id,booking_status.value)

@router.put('/update_my_bookings/{booker_id}/{booking_id}')
def update_my_bookings(booker_id: int, booking_id: int, req: BookingBase, db: Session= Depends(get_db)):
    return booking.update_my_bookings(db, booker_id,booking_id, req)

@router.get('/list_my_bookings/{user_id}', response_model= list[listBookingResponse])
def list_my_bookings(user_id: int, db: Session= Depends(get_db)):
    return booking.list_my_bookings(db, user_id)