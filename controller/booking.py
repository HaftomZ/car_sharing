from models.Booking import DbBooking
from sqlalchemy.orm.session import Session
from schemas.bookingSchema import BookingBase, BookingResponse
#from schemas.userSchema import UserBase
def create_booking(db: Session, request: BookingBase):
    booking = DbBooking(
        start_time=request.start_time, 
        end_time=request.end_time,
        location=request.location,
        status=request.status,
        created_at=request.created_at,
        updated_at=request.updated_at


        )
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return BookingResponse(  
        status=booking.status,
        created_at=booking.created_at,
        updated_at=booking.updated_at,
        start_time=booking.start_time,
        end_time=booking.end_time,
        location=booking.location,
        booking_id=booking.id
        
    )