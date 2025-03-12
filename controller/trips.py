from models.Trips import DbTrip
from models.Cars import DbCar
from models.Booking import DbBooking
from models.Payment import DbPayment
from models.Users import DbUser
from sqlalchemy.orm.session import Session
from schemas.tripSchema import TripBase , TripStatus
from schemas.carSchema import CarAvailability
from schemas.userSchema import userDisplay
from fastapi import HTTPException , status
import datetime
from datetime import timezone
from sqlalchemy import  func 
from controller import cars
import requests

def trip_duration(departure_time: datetime, arrival_time: datetime):
    duration = arrival_time - departure_time
    duration_per_hours = duration.total_seconds() / 3600
    return round(duration_per_hours,2)


def city_name_validation(city_name: str):
    if city_name.lower() == "string":  
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= f'Invalid city {city_name}')
    
    api_url = f"https://nominatim.openstreetmap.org/search?q={city_name}&format=json"
    headers = {
        "User-Agent": "HRIN/1.0 (noreply.hrin@gmail.com)" 
    }
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        if not response.json(): #response.json()[0]['display_name']
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= f'Invalid city {city_name}')
    else:
       raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= 'something went wrong')


def trip_vaildation(db: Session, request: TripBase):

    #check if the user has the car that he wants to create a trip using it or move the trip for
    car = db.query(DbCar).filter(DbCar.id == request.car_id, DbCar.owner_id == request.creator_id).first()
    if not car:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f'User {request.creator_id} does not have car {request.car_id}')

    #check the availability of the car
    if car.car_availability_status != CarAvailability.available:
       raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail= f'You can not add a trip with car id {request.car_id}, because the status of this car is not available. Turn it to available then try again.')

    #check departure and destination location
    city_name_validation(request.departure_location)
    city_name_validation(request.destination_location)

    #check the departure and arrival time
    if request.departure_time >= request.arrival_time:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= 'The arrival time should be after the departure time')
    
    #check the available seats if positive
    if request.available_adult_seats < 0 or request.available_children_seats < 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= 'The number of the available seats should be a positive number')

    #check if the sum of adult seats and children seats is more than the car total seats
    car = db.query(DbCar).filter(DbCar.id == request.car_id).first()
    if (request.available_adult_seats + request.available_children_seats > car.total_seats):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= 'The number of adults seats and children seats should not be more the the total seats in the car')

    #check if the cost is positive
    if request.cost < 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= 'The cost should be a positive number')


def create_trip(db: Session, request: TripBase, current_user: userDisplay):

    #check the user
    user = db.query(DbUser).filter(DbUser.id == request.creator_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f'User {request.creator_id} is not exsited')
    
    if user.id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    
    trip_vaildation(db, request)

    #check the status 
    if request.status.lower() != TripStatus.scheduled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= f"Invalid status {request.status}, it should be only scheduled")

    #check if the user have a trip before with the same car and during the same time
    trip = db.query(DbTrip).filter(DbTrip.creator_id == request.creator_id, DbTrip.car_id == request.car_id, DbTrip.departure_time<=request.departure_time, DbTrip.arrival_time>=request.departure_time).first()
    if trip:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail= f'You can not add a trip with car id {request.car_id}, because user {request.creator_id} already has a trip that its id is {trip.id} with the same car during this time.')


    trip = DbTrip(
        creator_id = request.creator_id,
        car_id = request.car_id,
        departure_location = request.departure_location.lower(),
        destination_location = request.destination_location.lower(),
        departure_time = request.departure_time.astimezone(timezone.utc),
        arrival_time = request.arrival_time.astimezone(timezone.utc),
        available_adult_seats = request.available_adult_seats,
        available_children_seats = request.available_children_seats,
        cost = request.cost,
        status = request.status.lower(),
        duration = trip_duration(request.departure_time, request.arrival_time)
        )
    db.add(trip)
    db.commit()
    db.refresh(trip)
    return trip


#update trip details
def update_trip(db: Session,request: TripBase, trip_id: int, current_user: userDisplay):

    trip = db.query(DbTrip).filter(DbTrip.id == trip_id)
    if not trip.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f'There is no trip with id {trip_id}')
    
    if trip.first().creator_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    #check the status of the trip
    if trip.first().status != TripStatus.scheduled:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail= f'You can not update trip {trip_id} when its status is {trip.first().status}')
    
    #check the new user that the creator wants to move this trip for
    new_user = db.query(DbUser).filter(DbUser.id == request.creator_id).first()
    if not new_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f'The user {request.creator_id} that you want to move this trip for, is not exsited')
    
    trip_vaildation(db, request)

    #check the status 
    if request.status.lower() not in [TripStatus.scheduled, TripStatus.ongoing, TripStatus.completed]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= f"Invalid status {request.status}, it should be scheduled, ongoing or completed")

    #check if the user have a trip before with the same car and during the same time
    pervious_trip = db.query(DbTrip).filter(DbTrip.creator_id == request.creator_id, DbTrip.car_id == request.car_id, DbTrip.id != trip_id, DbTrip.departure_time<=request.departure_time, DbTrip.arrival_time>=request.departure_time).first()
    if pervious_trip:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail= f'You can not update this trip with this time, because user {request.creator_id} already has a trip that its id is {pervious_trip.id} with the same car during this time.')


    trip.update({ 
        DbTrip.departure_location : request.departure_location.lower(),
        DbTrip.destination_location : request.destination_location.lower(),
        DbTrip.departure_time : request.departure_time.astimezone(timezone.utc),
        DbTrip.arrival_time : request.arrival_time.astimezone(timezone.utc),
        DbTrip.available_adult_seats : request.available_adult_seats,
        DbTrip.available_children_seats : request.available_children_seats,
        DbTrip.cost: request.cost,
        DbTrip.status : request.status.lower(),
        DbTrip.updated_at : func.now(),
        DbTrip.duration: trip_duration(request.departure_time, request.arrival_time),
        DbTrip.creator_id : request.creator_id,
        DbTrip.car_id : request.car_id
        })
    
    car_status = ""
    if request.status.lower() == TripStatus.ongoing:
        car_status = CarAvailability.in_use
        cars.update_car_availability_status(db, request.creator_id, request.car_id , car_status)

    elif request.status.lower() in [TripStatus.scheduled , TripStatus.completed]:
        car_status = CarAvailability.available
        cars.update_car_availability_status(db, request.creator_id, request.car_id , car_status)
    
    db.commit()

    updated_trip = db.query(DbTrip).filter(DbTrip.creator_id == request.creator_id, DbTrip.id == trip_id).first()
    return updated_trip


#delete trip
def delete_trip(db: Session, trip_id: int, current_user: userDisplay):
    trip = db.query(DbTrip).filter(DbTrip.id == trip_id)
    if not trip.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    if trip.first().creator_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    
    if trip.first().status != TripStatus.cancelled:
        trip.update({ 
            DbTrip.status : TripStatus.cancelled,
            DbTrip.updated_at : func.now()
             })
        temp_booking =db.query(DbBooking).filter(DbBooking.trip_id == trip_id).all()
        payments = db.query(DbPayment)
        for all_status in temp_booking:
            if all_status.status == "Confirmed":
             payments.filter(DbPayment.booking_id == all_status.booking_id).first().refund_status = True
             db.query(DbBooking).filter(DbBooking.booking_id == all_status.booking_id).first().status = "cancelled"
        car_status = CarAvailability.available
        cars.update_car_availability_status(db, trip.first().creator_id, trip.first().car_id , car_status)
        db.commit()
    return 

#get all trips 
def get_all_trips(db: Session, user_id: int):
   trip_query = db.query(DbTrip)
   if user_id is not None:
        trip_query =  trip_query.filter(DbTrip.creator_id == user_id)
   
   return trip_query.all()


#get trip
def get_trip(db: Session, id: int):
    trip = db.query(DbTrip).filter(DbTrip.id == id).first()
    if not trip:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    return trip



#search for trip
def search_trip(db: Session, departure_location: str, destination_location: str,
                departure_time: datetime, available_adult_seats: int, available_children_seats: int):
    trips=  db.query(DbTrip).filter(DbTrip.departure_location== departure_location.lower(),
                                    DbTrip.destination_location == destination_location.lower(),
                                    DbTrip.departure_time >= departure_time,
                                    DbTrip.available_adult_seats >= available_adult_seats,
                                    DbTrip.available_children_seats >= available_children_seats).all()
    if not trips:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return trips
