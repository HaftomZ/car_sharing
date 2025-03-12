from models.Booking import DbBooking
from models.Trips import DbTrip
from models.Payment import DbPayment
from models.Users import DbUser
from sqlalchemy.orm.session import Session
from schemas.bookingSchema import *
from fastapi import HTTPException, status
from controller import cars
from threading import Timer
from datetime import datetime,timezone,timedelta
from schemas.userSchema import UserBase,userDisplay

def create_booking(db: Session,request: BookingBase,current_user:userDisplay):
   
    if request.booker_id != current_user.id and current_user.is_admin != True:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN)
    users = db.query(DbUser).filter(DbUser.id == request.booker_id).first()
    trip = db.query(DbTrip).filter(DbTrip.id==request.trip_id)

    if not trip.first():
        raise  HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="No Trip found")
    if not users:
        raise  HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="No user id found")
    if  trip.first().status =="cancelled":
         raise  HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= "The trip was cancelled")
    
    trip_departure_time = trip.first().departure_time.replace(tzinfo=timezone.utc)
    grace_time =  trip_departure_time - datetime.now(timezone.utc)  
    if grace_time <=timedelta(seconds=0):
           raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail="You can't book the trip, grace time is over")
   
    temp_booking = db.query(DbBooking).filter(DbBooking.trip_id == request.trip_id, DbBooking.booker_id == request.booker_id).first()
    if temp_booking:
          raise  HTTPException(status_code= status.HTTP_409_CONFLICT, detail= 'You have already boooked the trip!')
    
    if trip.first().available_adult_seats!=0:
     if request.adult_seats <= 0 or request.children_seats < 0:
          raise  HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail= "Adult seats must be > 0 and child seat >= 0")
     if (request.children_seats > trip.first().available_children_seats) or\
        (request.adult_seats > trip.first().available_adult_seats):
         message=f"Sorry you have entered more than available seats, the available seats are: Adult seat = {trip.first().available_adult_seats} and Children seat = {trip.first().available_children_seats}"
         raise  HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail= message)                     
     else:
         trip.first().available_adult_seats-= request.adult_seats
         trip.first().available_children_seats-= request.children_seats
         trip.first().passengers_count += (request.adult_seats + request.children_seats)

         trip.update({
           DbTrip.available_adult_seats : trip.first().available_adult_seats,
           DbTrip.available_children_seats : trip.first().available_children_seats,
           DbTrip.passengers_count : trip.first().passengers_count
             
         })
           
    else:
        raise  HTTPException(status_code= status.HTTP_409_CONFLICT, detail= 'Sorry the trip is fully boooked!')
    booking_tobe_created = DbBooking(
        trip_id = request.trip_id,
        booker_id = request.booker_id,
        pickup_location = request.pickup_location,
        end_location = request.end_location,
        adult_seats = request.adult_seats,
        children_seats = request.children_seats,
        created_at= datetime.now(timezone.utc),
        updated_at = datetime.now(timezone.utc)
        )
    db.add(booking_tobe_created)
    db.commit()
    db.refresh(booking_tobe_created)
    if trip.first().available_adult_seats==0:
            # after the available seats are all booked, the car status should be updated to not available
            update_car = cars.update_car_availability_status(
                                            db,trip.first().creator_id,
                                            trip.first().car_id, car_status="Unavailable"
                                            )
    
    Timer(60, release_seat_if_payment_fails, args=[request.booker_id, request.trip_id, db]).start()
    
    return booking_tobe_created

def release_seat_if_payment_fails(booker_id : int, trip_id : int, db:Session):
     
    temp_booking = db.query(DbBooking).filter(DbBooking.booker_id == booker_id,DbBooking.trip_id == trip_id).with_for_update().first()
    if temp_booking:
     if temp_booking.status =="Pending":
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
def cancel_booking(db: Session, booking_id:int, current_user: userDisplay):
        
        booking_tobe_cancelled = db.query(DbBooking).filter(DbBooking.booking_id == booking_id).first()
        if not booking_tobe_cancelled:
            raise  HTTPException(status_code= status.HTTP_404_NOT_FOUND)
        if booking_tobe_cancelled.booker_id != current_user.id and current_user.is_admin != True:
            raise HTTPException(status_code= status.HTTP_403_FORBIDDEN)
       
        trip=db.query(DbTrip).filter(DbTrip.id == booking_tobe_cancelled.trip_id)
        if trip.first().status !="cancelled":
         
         trip_departure_time = trip.first().departure_time.replace(tzinfo=timezone.utc)
         grace_time =  trip_departure_time - datetime.now(timezone.utc)
        
         if grace_time <=timedelta(seconds=0):
           raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail="you can't cancel, grace time is over")
    
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
        
         payment_refund = db.query(DbPayment).filter(DbPayment.booking_id == booking_id).first()
         if payment_refund:
            payment_refund.refund_status = True

        db.delete(booking_tobe_cancelled )
        db.commit()
       
        return 

# After updating a booking, the available seats and car availabilty has to be updated.
def update_my_bookings(db: Session,booking_id: int, request: BookingBase,current_user:userDisplay):

    booking_tobe_update = db.query(DbBooking).filter(DbBooking.booking_id == booking_id)
    if not booking_tobe_update.first():
        raise  HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= "Booking not found")
    if booking_tobe_update.first().booker_id != current_user.id and current_user.is_admin != True:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN)
    
    trip = db.query(DbTrip).filter(DbTrip.id == booking_tobe_update.first().trip_id)

    if  trip.first().status =="cancelled":
         raise  HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= "The trip was cancelled")
    
    trip_departure_time = trip.first().departure_time.replace(tzinfo=timezone.utc)
    grace_time =  trip_departure_time - datetime.now(timezone.utc)
    
    if grace_time <=timedelta(seconds=0):
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail="You can't update, grace time is over")
    
    if booking_tobe_update.first().status == "Confirmed": 
        if booking_tobe_update.first().adult_seats != request.adult_seats or\
           booking_tobe_update.first().children_seats != request.children_seats or\
           booking_tobe_update.first().booker_id != request.booker_id or\
           booking_tobe_update.first().trip_id != request.trip_id :
           raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail= "Only pickup_location and end_location can be updated")
    else:
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
   
    if trip.first().available_adult_seats==0:          
            car_status ="unavailable"
    else:
            car_status = "available"
    update_car = cars.update_car_availability_status(
                                            db,trip.first().creator_id,
                                            trip.first().car_id, car_status
                                            )

    return booking_tobe_update.first()
   
def list_of_bookings(db: Session, user_id: int, current_user: userDisplay):
    lists= db.query(DbBooking)
    if user_id is not None:
      users = db.query(DbUser).filter(DbUser.id==user_id).first()
      if user_id != current_user.id and current_user.is_admin != True:
          raise HTTPException(status_code= status.HTTP_403_FORBIDDEN)
      if not users:
          raise  HTTPException(status_code= status.HTTP_404_NOT_FOUND) 
      lists = lists.filter(DbBooking.booker_id == user_id)
    else:
        if current_user.is_admin != True:
             raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail="You must be an admin")
    return lists.all()

def get_a_booking(db: Session, booking_id: int, current_user : userDisplay):
     lists = db.query(DbBooking).filter(DbBooking.booking_id == booking_id).first()
     if not lists:
      raise  HTTPException(status_code= status.HTTP_404_NOT_FOUND)
     if lists.booker_id != current_user.id and current_user.is_admin != True:
         raise HTTPException(status_code= status.HTTP_403_FORBIDDEN)
     
     return lists

