from models.Trips import DbTrip
from models.Cars import DbCar
from models.Booking import DbBooking
from models.Payment import DbPayment
from sqlalchemy.orm.session import Session
from schemas.tripSchema import TripBase , TripStatus
from schemas.carSchema import CarAvailability
from fastapi import HTTPException , status
import datetime
from sqlalchemy import  func 
from controller import cars
import requests

def trip_duration(departure_time: datetime, arrival_time: datetime):
    duration = arrival_time - departure_time
    duration_per_hours = duration.total_seconds() / 3600
    return round(duration_per_hours,2)


def city_name_validation(city_name: str):
    # api_url = 'https://api.api-ninjas.com/v1/city?name={}'.format(city_name)
    # response = requests.get(api_url, headers={'X-Api-Key': 'u6HXeCfNAwAIbH6BXUXdCg==ntvSIQMalRYRVEgb'})

    # if response.status_code == requests.codes.ok:
    #     if not response.json():
    #         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= f'Invalid city {city_name}')
    #     if (response.json()[0]['name'].lower() != city_name.lower()):
    #         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= f'Invalid city {city_name}')
    # else:
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= 'something went wrong')
    if city_name.lower() == "string":  
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= f'Invalid city {city_name}')
    
    api_url = f"https://nominatim.openstreetmap.org/search?q={city_name}&format=json"
    headers = {
        "User-Agent": "car_sharing/1.0 (roula.arab95@gmail.com)" 
    }
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        if not response.json(): #response.json()[0]['display_name']
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= f'Invalid city {city_name}')
    else:
       raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= 'something went wrong')


def trip_vaildation(db: Session, request: TripBase):

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
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= 'The number of adults seats and children seats should not be more the the total seats in your car')

    #check if the cost is positive
    if request.cost < 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= 'The cost should be a positive number')


def create_trip(db: Session, request: TripBase):

    #check if the user have the car that he wants to create a trip using it
    car = db.query(DbCar).filter(DbCar.id == request.car_id, DbCar.owner_id == request.creator_id).first()
    if not car:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f'You do not have a car with car id {request.car_id}')

    #check the availability of the car
    if car.car_availability_status != CarAvailability.available:
       raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail= f'You can not add a trip with car id {request.car_id}, because the status of this car is not available. Turn it to available then try again.')

    trip_vaildation(db, request)

    #check the status 
    if request.status.lower() != TripStatus.scheduled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= f"Invalid status {request.status}, it should be only scheduled")

    #check if the user have a trip before with the same car and during the same time
    trip = db.query(DbTrip).filter(DbTrip.creator_id == request.creator_id, DbTrip.car_id == request.car_id, DbTrip.departure_time<=request.departure_time, DbTrip.arrival_time>=request.departure_time).first()
    if trip:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail= f'You can not add a trip with car id {request.car_id}, because you already have a trip that its id is {trip.id} with the same car during this time.')


    trip = DbTrip(
        creator_id = request.creator_id,
        car_id = request.car_id,
        departure_location = request.departure_location.lower(),
        destination_location = request.destination_location.lower(),
        departure_time = request.departure_time,
        arrival_time = request.arrival_time,
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
def update_trip(db: Session,request: TripBase, trip_id: int):

    trip = db.query(DbTrip).filter(DbTrip.creator_id == request.creator_id, DbTrip.id == trip_id)
    if not trip.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f'You do not have a trip with id {trip_id}')
    
    #check if the car that the user wants to move this trip for, is exsited
    car= db.query(DbCar).filter(DbCar.owner_id == request.creator_id, DbCar.id == request.car_id).first()
    if not car:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f'You can not update this trip to be for car {request.car_id} , because you do not have this car')
    
    trip_vaildation(db, request)

    #check the status 
    if request.status.lower() not in [TripStatus.scheduled, TripStatus.ongoing, TripStatus.completed, TripStatus.cancelled]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= f"Invalid status {request.status}, it should be scheduled, ongoing, completed, or cancelled")

    #check if the user have a trip before with the same car and during the same time
    pervious_trip = db.query(DbTrip).filter(DbTrip.creator_id == request.creator_id, DbTrip.car_id == request.car_id, DbTrip.id != trip_id, DbTrip.departure_time<=request.departure_time, DbTrip.arrival_time>=request.departure_time).first()
    if pervious_trip:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail= f'You can not update your trip with this time, because you already have a trip that its id is {pervious_trip.id} with the same car during this time.')


    trip.update({ 
        DbTrip.departure_location : request.departure_location.lower(),
        DbTrip.destination_location : request.destination_location.lower(),
        DbTrip.departure_time : request.departure_time,
        DbTrip.arrival_time : request.arrival_time,
        DbTrip.available_adult_seats : request.available_adult_seats,
        DbTrip.available_children_seats : request.available_children_seats,
        DbTrip.cost: request.cost,
        DbTrip.status : request.status.lower(),
        DbTrip.updated_at : func.now(),
        DbTrip.duration: trip_duration(request.departure_time, request.arrival_time),
        DbTrip.car_id : request.car_id
        })
    
    car_status = ""
    if request.status.lower() == TripStatus.ongoing:
        car_status = CarAvailability.in_use
        cars.update_car_availability_status(db, request.creator_id, request.car_id , car_status)

    elif request.status.lower() in [TripStatus.cancelled , TripStatus.scheduled , TripStatus.completed]:
        car_status = CarAvailability.available
        cars.update_car_availability_status(db, request.creator_id, request.car_id , car_status)
    
    db.commit()

    updated_trip = db.query(DbTrip).filter(DbTrip.creator_id == request.creator_id, DbTrip.id == trip_id).first()
    return updated_trip


#delete trip
def delete_trip(db: Session, user_id: int, trip_id: int):
    trip = db.query(DbTrip).filter(DbTrip.id == trip_id, DbTrip.creator_id == user_id).first()
    if not trip:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f'There is no trip with id {trip_id}')
    temp_booking = db.query(DbBooking).filter(DbBooking.trip_id == trip_id).all()
    payments = db.query(DbPayment)
    for all_status in temp_booking:
        if all_status.status == "Confirmed":
         payments.filter(DbPayment.booking_id == all_status.booking_id).first().refund_status = True

    db.delete(trip)
    db.commit()
    return 

#get all trips that are related to a user
def get_all_user_trips(db: Session, user_id: int):
   trips=  db.query(DbTrip).filter(DbTrip.creator_id == user_id).all()
   if not trips:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='There are no trips found!')
   return trips


#search for trip
def search_trip(db: Session, departure_location: str, destination_location: str,
                departure_time: datetime, available_adult_seats: int, available_children_seats: int):
    trips=  db.query(DbTrip).filter(DbTrip.departure_location== departure_location.lower(),
                                    DbTrip.destination_location == destination_location.lower(),
                                    DbTrip.departure_time >= departure_time,
                                    DbTrip.available_adult_seats >= available_adult_seats,
                                    DbTrip.available_children_seats >= available_children_seats).all()
    if not trips:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='There are no trips match your request!')
    return trips
