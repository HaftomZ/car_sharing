from models.Booking import DbBooking
from sqlalchemy.orm.session import Session
from schemas.bookingSchema import *
from models.Trips import DbTrip
from fastapi import HTTPException, status
def create_booking(db: Session, request: BookingBase):
    booking = DbBooking(
        ride_id=request.ride_id,
        booker_id=request.booker_id,
        pickup_location=request.pickup_location,
        adult_seats=request.adult_seats,
        children_seats=request.children_seats
        )
    if request.ride_id not in [trip.id for trip in db.query(DbTrip).all()]:
        raise  HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f'there is no such a trip!')
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return BookingDisplay(
        status=booking.status,
        created_at=booking.created_at,
        updated_at=booking.updated_at,
        message=f"Trip {booking.ride_id} is booked successfully"
    )
def cancel_booking(db: Session, booking_id: int):
        booking = db.query(DbBooking).filter(DbBooking.booking_id == booking_id).first()
        if not booking:
             raise  HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f'Booking not found!')
        booking.status = 'cancelled'
        db.delete(booking)
        db.commit()
        return "Booking cancelled successfully"
def update_my_bookings(db: Session, booking_id: int, request: BookingBase):
    booking = db.query(DbBooking).filter(DbBooking.booking_id == booking_id).first()
    if not booking:
        raise  HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f'Booking not found!')
    booking.ride_id = request.ride_id
    booking.booker_id = request.booker_id
    booking.pickup_location = request.pickup_location
    booking.adult_seats = request.adult_seats
    booking.children_seats = request.children_seats
    db.commit()
    db.refresh(booking)
    return BookingDisplay(
        status=booking.status,
        created_at=booking.created_at,
        updated_at=booking.updated_at,
        message=f"Booking {booking_id} is updated successfully"
    )
def list_my_bookings(db: Session, user_id: int):
    lists= db.query(DbBooking).filter(DbBooking.booker_id == user_id).all()

    if user_id not in [booking.booker_id for booking in db.query(DbBooking).all()]:
        raise  HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f'You donot have any bookings!')
     
    return lists
        #  listBookingResponse(
        #  booking_list =[].map(lambda booking: BookingList(
        #       lists.booking_id, lists.status, lists.created_at, lists.updated_at, lists.pickup_location
        #  )))
  

