from models.Booking import DbBooking
from models.Trips import DbTrip
from sqlalchemy.orm.session import Session
from schemas.bookingSchema import *
from models.Trips import DbTrip
from fastapi import HTTPException, status
def create_booking(db: Session,booker_id:int, trip_id: int,request: BookingBase):
    booking_tobe_created = DbBooking(
        trip_id=trip_id,
        booker_id=booker_id,
        pickup_location=request.pickup_location,
        end_location=request.end_location,
        adult_seats=request.adult_seats,
        children_seats=request.children_seats
        )
    trip = db.query(DbBooking).filter(DbBooking.trip_id == trip_id, DbBooking.booker_id == booker_id).first()
    if trip:
          raise  HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= 'You have already boooked the trip!')
    
    if trip_id not in [trip.id for trip in db.query(DbTrip).all()]:
        raise  HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f'there is no such a trip!')
    #todo: check for available seats first and then add the booking.
    # and update the available seats in the trip table
    # after the available seats are all booked, the car status should be updated to not available
    db.add(booking_tobe_created)
    db.commit()
    db.refresh(booking_tobe_created)
    
    return booking_tobe_created
def cancel_booking(db: Session, booker_id: int,booking_id:int):
        booking_tobe_cancelled = db.query(DbBooking).filter(DbBooking.booker_id == booker_id,DbBooking.booking_id == booking_id).first()
        if not booking_tobe_cancelled:
             raise  HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f'Booking not found!')
        db.delete(booking_tobe_cancelled )
        db.commit()
        return "Booking cancelled successfully"
# Booking status should be updated by driver only
def update_booking_status(db: Session, user_id: int, trip_id:int, booking_id: int,booking_status: str):
    driver=db.query(DbTrip).filter(DbTrip.creator_id == user_id, DbTrip.id==trip_id).first()
    if not driver:
     raise  HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f'You are not the driver of this trip!')
    passenger_booking_id = db.query(DbBooking).filter(DbBooking.booking_id == booking_id)
    if not passenger_booking_id.first():
        raise  HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f'There is no such booking!')
    
    passenger_booking_id.update({
         DbBooking.status :booking_status
        })

    db.commit()
    return f"status of booking id {booking_id} is updated successfully to {booking_status}"
def update_my_bookings(db: Session, booker_id: int,booking_id: int, request: BookingBase):
    booking_tobe_update = db.query(DbBooking).filter(DbBooking.booking_id == booking_id,DbBooking.booker_id==booker_id)
    if not booking_tobe_update.first():
        raise  HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f'Booking not found!')
    booking_tobe_update.update({
        DbBooking.pickup_location : request.pickup_location,
        DbBooking.end_location:request.end_location,
        DbBooking.adult_seats : request.adult_seats,
        DbBooking.children_seats :request.children_seats
    })
    db.commit()
    return f"Booking {booking_id} is updated successfully"
   
def list_my_bookings(db: Session, user_id: int):
    lists= db.query(DbBooking).filter(DbBooking.booker_id == user_id).all()

    if user_id not in [booking.booker_id for booking in db.query(DbBooking).all()]:
        raise  HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f'You do not have any bookings!')
     
    return lists
    

