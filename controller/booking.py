from models.Booking import DbBooking
from models.Trips import DbTrip
from sqlalchemy.orm.session import Session
from schemas.bookingSchema import *
from fastapi import HTTPException, status
from controller import cars

def create_booking(db: Session, booker_id:int, trip_id: int, request: BookingBase):
    booking_tobe_created = DbBooking(
        trip_id = trip_id,
        booker_id = booker_id,
        pickup_location = request.pickup_location,
        end_location = request.end_location,
        adult_seats = request.adult_seats,
        children_seats = request.children_seats
        )
    trip = db.query(DbBooking).filter(DbBooking.trip_id == trip_id, DbBooking.booker_id == booker_id).first()
    if trip:
          raise  HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= 'You have already boooked the trip!')
    
    if trip_id not in [trip.id for trip in db.query(DbTrip).all()]:
        raise  HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f'there is no such a trip!')
    
    #check for available seats first and then add the booking.
    # and update the available seats in the trip table here

    check_available_seats = db.query(DbTrip).filter(DbTrip.id==trip_id)
    if check_available_seats.first().available_adult_seats!=0:
     if (request.children_seats > check_available_seats.first().available_children_seats) or\
        (request.adult_seats > check_available_seats.first().available_adult_seats):
         message=f"Sorry you have entered more than available seats, the available seats are: Adult seat = {check_available_seats.first().available_adult_seats} and Children seat = {check_available_seats.first().available_children_seats}"
         raise  HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= message)                     
     else:
         check_available_seats.first().available_adult_seats-= request.adult_seats
         check_available_seats.first().available_children_seats-= request.children_seats
         check_available_seats.first().passengers_count += (request.adult_seats + request.children_seats)

         check_available_seats.update({
           DbTrip.available_adult_seats : check_available_seats.first().available_adult_seats,
           DbTrip.available_children_seats : check_available_seats.first().available_children_seats,
           DbTrip.passengers_count : check_available_seats.first().passengers_count
             
         })
           
    else:
        # after the available seats are all booked, the car status should be updated to not available
        update_car = cars.update_car_availability_status(
                                            db,check_available_seats.first().creator_id,
                                            check_available_seats.first().car_id, car_status="Unavailable"
                                            )
        raise  HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= 'Sorry the trip is fully boooked!')
    

 
    db.add(booking_tobe_created)
    db.commit()
    db.refresh(booking_tobe_created)
    return booking_tobe_created

#After cancelling the booking, the seats that were booked must be released and car availablity must be updated.
def cancel_booking(db: Session, booker_id: int,booking_id:int):
        booking_tobe_cancelled = db.query(DbBooking).filter(DbBooking.booker_id == booker_id,DbBooking.booking_id == booking_id).first()
        if not booking_tobe_cancelled:
             raise  HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f'Booking not found!')
        trip=db.query(DbTrip).filter(DbTrip.id == booking_tobe_cancelled.trip_id)
        trip.first().available_adult_seats+=booking_tobe_cancelled.adult_seats
        trip.first().available_children_seats+=booking_tobe_cancelled.children_seats
        trip.first().passengers_count -= (booking_tobe_cancelled.adult_seats + booking_tobe_cancelled.children_seats)
        trip.update({
               DbTrip.available_adult_seats : trip.first().available_adult_seats,
               DbTrip.available_children_seats: trip.first().available_children_seats,
               DbTrip.passengers_count : trip.first().passengers_count
           })
        update_car = cars.update_car_availability_status(
                                            db,trip.first().creator_id,
                                            trip.first().car_id, car_status ="available"
                                            )
        db.delete(booking_tobe_cancelled )
        db.commit()
        return "Booking cancelled successfully"

#it has to update the trip available seats and the cars availability if the status is rejected.
# Booking status should be updated by driver only
def update_booking_status(db: Session, user_id: int, trip_id:int, booking_id: int,booking_status: str):
    trip=db.query(DbTrip).filter(DbTrip.creator_id == user_id, DbTrip.id==trip_id)
    if not trip.first():
     raise  HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f'You are not the driver of this trip!')
    passenger_booking_id = db.query(DbBooking).filter(DbBooking.booking_id == booking_id)
    if not passenger_booking_id.first():
        raise  HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f'There is no such booking!')
    
    passenger_booking_id.update({
         DbBooking.status :booking_status
        })
    if booking_status == "rejected":
      
        trip.first().available_adult_seats+=passenger_booking_id.first().adult_seats
        trip.first().available_children_seats+=passenger_booking_id.first().children_seats
        trip.first().passengers_count -= (passenger_booking_id.first().adult_seats + passenger_booking_id.first().children_seats)
        trip.update({
               DbTrip.available_adult_seats : trip.first().available_adult_seats,
               DbTrip.available_children_seats: trip.first().available_children_seats,
               DbTrip.passengers_count : trip.first().passengers_count
        }) 
        update_car = cars.update_car_availability_status(
                                            db,trip.first().creator_id,
                                            trip.first().car_id, car_status ="available"
                                            )

    db.commit()
    return f"status of booking id {booking_id} is updated successfully to {booking_status}"

# Todo: After updating a booking, the available seats has to be updated in trip table.
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
    

