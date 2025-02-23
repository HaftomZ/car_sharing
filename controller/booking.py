from models.Booking import DbBooking
from sqlalchemy.orm.session import Session
#from schemas.userSchema import UserBase
def create_booking(db: Session, user_id: int, car_id: int, start_time, end_time):
    booking = DbBooking(
        user_id=user_id, 
        car_id=car_id, 
        start_time=start_time, 
        end_time=end_time)
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking