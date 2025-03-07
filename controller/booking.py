from models.Booking import DbBooking
from models.Trips import DbTrip
from models.Payment import DbPayment
from sqlalchemy.orm.session import Session
from schemas.bookingSchema import *
from fastapi import HTTPException, status
from controller import cars
from threading import Timer
from datetime import datetime,timezone

def create_booking(db: Session, booker_id:int, trip_id: int, request: BookingBase):
   
    booking_tobe_created = DbBooking(
        trip_id = trip_id,
        booker_id = booker_id,
        pickup_location = request.pickup_location,
        end_location = request.end_location,
        adult_seats = request.adult_seats,
        children_seats = request.children_seats,
        created_at= datetime.now(timezone.utc),
        updated_at = datetime.now(timezone.utc)
        

        )
    trip = db.query(DbBooking).filter(DbBooking.trip_id == trip_id, DbBooking.booker_id == booker_id).first()
    if trip:
          raise  HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= 'You have already boooked the trip!')
    
    if trip_id not in [trip.id for trip in db.query(DbTrip).all()]:
        raise  HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f'there is no such a trip!')
    
    #check for available seats first and then add the booking.
    # and update the available seats in the trip table here

    check_available_seats = db.query(DbTrip).filter(DbTrip.id==trip_id)
    if  check_available_seats.first().status in ["completed", "cancelled"]:
         raise  HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f'The trip is closed or cancelled')
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
        raise  HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= 'Sorry the trip is fully boooked!')
    
    db.add(booking_tobe_created)
    db.commit()
    db.refresh(booking_tobe_created)
    if check_available_seats.first().available_adult_seats==0:
            # after the available seats are all booked, the car status should be updated to not available
            update_car = cars.update_car_availability_status(
                                            db,check_available_seats.first().creator_id,
                                            check_available_seats.first().car_id, car_status="Unavailable"
                                            )
    
    Timer(60, release_seat_if_payment_fails, args=[booker_id, trip_id, db]).start()
    
    return booking_tobe_created

def release_seat_if_payment_fails(booker_id : int, trip_id : int, db:Session):
     
    temp_booking = db.query(DbBooking).filter(DbBooking.booker_id == booker_id,DbBooking.trip_id == trip_id).with_for_update().first()
    if temp_booking.status == "Pending":
       trip=db.query(DbTrip).filter(DbTrip.id == temp_booking.trip_id)
       trip.first().available_adult_seats += temp_booking.adult_seats
       trip.first().available_children_seats += temp_booking.children_seats
       trip.first().passengers_count -= (temp_booking.adult_seats + temp_booking.children_seats)
       trip.update({
               DbTrip.available_adult_seats : trip.first().available_adult_seats,
               DbTrip.available_children_seats: trip.first().available_children_seats,
               DbTrip.passengers_count : trip.first().passengers_count
           })
       update_car = cars.update_car_availability_status(
                                            db,trip.first().creator_id,
                                            trip.first().car_id, car_status ="available"
                                            )
       db.delete(temp_booking)  
       db.commit()
#After cancelling the booking, the seats that were booked must be released and car availablity must be updated.
def cancel_booking(db: Session, booking_id:int):
        booking_tobe_cancelled = db.query(DbBooking).filter(DbBooking.booking_id == booking_id).first()
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
        payment_refund = db.query(DbPayment).filter(DbPayment.booking_id == booking_id, DbPayment.user_id == booking_tobe_cancelled.booker_id).first()
        if payment_refund:
            payment_refund.refund_status = True
        db.delete(booking_tobe_cancelled )
        db.commit()
       
        return "Booking cancelled successfully"



# Todo: After updating a booking, the available seats and car availabilty has to be updated.
def update_my_bookings(db: Session, booking_id: int, request: BookingBase):
    booking_tobe_update = db.query(DbBooking).filter(DbBooking.booking_id == booking_id)
    if not booking_tobe_update.first():
        raise  HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f'Booking not found!')
    
    trip = db.query(DbTrip).filter(DbTrip.id == booking_tobe_update.first().trip_id)
    adult_seats_diff = request.adult_seats - booking_tobe_update.first().adult_seats
    children_seats_diff = request.children_seats - booking_tobe_update.first().children_seats

    if (trip.first().available_adult_seats - adult_seats_diff) < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"Not enough available adult seats. There are only {trip.first().available_adult_seats} seats"
        )
    
    if (trip.first().available_children_seats - children_seats_diff) < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail= f"Not enough available children seats.there are only {trip.first().available_children_seats} seats"
        )
    trip.first().available_adult_seats -= adult_seats_diff
    trip.first().available_children_seats -= children_seats_diff
    trip.first().passengers_count += (adult_seats_diff + children_seats_diff)
    trip.update({
    DbTrip.available_adult_seats : trip.first().available_adult_seats,
    DbTrip.available_children_seats: trip.first().available_children_seats,
    DbTrip.passengers_count : trip.first().passengers_count
    })
    booking_tobe_update.update({
        DbBooking.pickup_location : request.pickup_location,
        DbBooking.end_location:request.end_location,
        DbBooking.adult_seats : request.adult_seats,
        DbBooking.children_seats :request.children_seats
    })
    db.commit()
    # after the available seats are all booked, the car status should be updated to not available
    if trip.first().available_adult_seats==0:          
            car_status ="Unavailable"
    else:
            car_status = "available"
    update_car = cars.update_car_availability_status(
                                            db,trip.first().creator_id,
                                            trip.first().car_id, car_status
                                            )

    return booking_tobe_update.first()
   
def list_my_bookings(db: Session, user_id: int):
    lists= db.query(DbBooking).filter(DbBooking.booker_id == user_id).all()

    if user_id not in [booking.booker_id for booking in db.query(DbBooking).all()]:
        raise  HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f'You do not have any bookings!')
     
    return lists

def list_all_booking(db: Session):
     lists=db.query(DbBooking).all()
     return lists
    

