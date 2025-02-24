from models.Booking import DbBooking
from sqlalchemy.orm.session import Session
from schemas.bookingSchema import BookingBase, BookingResponse
def create_booking(db: Session, request: BookingBase):
    booking = DbBooking(
        ride_id=request.ride_id,
        booker_id=request.booker_id,
        start_time=request.start_time,
        pickup_location=request.pickup_location
       
        )
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return BookingResponse(
        status=booking.status,
        created_at=booking.created_at,
        updated_at=booking.updated_at,
        start_time=booking.start_time,
        location=booking.pickup_location,
        message="Booking created successfully"
    )
def cancel_booking(db: Session, booking_id: int):
        booking = db.query(DbBooking).filter(DbBooking.booking_id == booking_id).first()
        if booking:
            booking.status = 'cancelled'
            db.delete(booking)
            db.commit()
            return "Booking cancelled successfully"
        return "Booking not found"
def list_my_bookings(db: Session, user_id: int):
    return db.query(DbBooking).filter(DbBooking.booker_id == user_id).all()
  

