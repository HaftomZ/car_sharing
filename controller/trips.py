from models.Trips import DbTrip
from sqlalchemy.orm.session import Session
from schemas.tripSchema import TripBase
from fastapi import HTTPException , status
import datetime
from sqlalchemy import  func 
from controller import cars

def trip_duration(departure_time: datetime, arrival_time: datetime):
    duration = arrival_time - departure_time
    return duration.total_seconds() / 3600

def create_trip(db: Session, request: TripBase, creator_id: int, car_id: int):
    
    if request.departure_time >= request.arrival_time:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= 'The arrival time should be after the departure time')
    
    trip = DbTrip(
        creator_id = creator_id,
        car_id = car_id,
        departure_location = request.departure_location.lower(),
        destination_location = request.destination_location.lower(),
        departure_time = request.departure_time,
        arrival_time = request.arrival_time,
        available_adult_seats = request.available_adult_seats,
        available_children_seats = request.available_children_seats,
        cost = request.cost,
        duration = trip_duration(request.departure_time, request.arrival_time)
        )
    db.add(trip)
    db.commit()
    db.refresh(trip)
    return trip

#update trip details
def update_trip(db: Session,request: TripBase, creator_id: int , trip_id: int):
    trip = db.query(DbTrip).filter(DbTrip.creator_id == creator_id, DbTrip.id == trip_id)
    if not trip.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f'There is no trip with id {trip_id}')
    
    if request.departure_time >= request.arrival_time:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= 'The arrival time should be after the departure time')

    trip.update({ 
        DbTrip.departure_location : request.departure_location.lower(),
        DbTrip.destination_location : request.destination_location.lower(),
        DbTrip.departure_time : request.departure_time,
        DbTrip.arrival_time : request.arrival_time,
        DbTrip.available_adult_seats : request.available_adult_seats,
        DbTrip.available_children_seats : request.available_children_seats,
        DbTrip.cost: request.cost,
        DbTrip.updated_at : func.now(),
        DbTrip.duration: trip_duration(request.departure_time, request.arrival_time)
        })
    db.commit()
    return 'Your trip details has been updated successfully!'

#delete trip
def delete_trip(db: Session, user_id: int, trip_id: int):
    trip = db.query(DbTrip).filter(DbTrip.id == trip_id, DbTrip.creator_id == user_id).first()
    if not trip:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f'There is no trip with id {trip_id}')
    
    db.delete(trip)
    db.commit()
    return 'Your trip has been removed successfully!'

#get all trips that are related to a user
def get_all_user_trips(db: Session, user_id: int):
   trips=  db.query(DbTrip).filter(DbTrip.creator_id == user_id).all()
   if not trips:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='There are no trips found!')
   return trips

#search for trip
def search_trip(db: Session, departure_location: str, destination_location: str,
                departure_time: datetime, available_adult_seats: int, available_children_seats: int):
    trips=  db.query(DbTrip).filter(DbTrip.departure_location == departure_location.lower(),
                                    DbTrip.destination_location == destination_location.lower(),
                                    DbTrip.departure_time >= departure_time,
                                    DbTrip.available_adult_seats >= available_adult_seats,
                                    DbTrip.available_children_seats >= available_children_seats).all()
    if not trips:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='There are no trips match your request!')
    return trips

#update trip status
def update_trip_status(db: Session, user_id: int , trip_id: int, status: str):
    trip = db.query(DbTrip).filter(DbTrip.id == trip_id, DbTrip.creator_id == user_id)
    if not trip.first():
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f'There is no trip with id {trip_id}')
    
    trip.update({ 
       DbTrip.status : status
       })
    car_id = trip.first().car_id

    car_status = ""
    if status == "Ongoing":
        car_status = "In Use"
        cars.update_car_availability_status(db, user_id, car_id , car_status)

    elif status == "Cancelled" or status == "Scheduled" or status == "Completed":
        car_status = "Available"
        cars.update_car_availability_status(db, user_id, car_id , "Available")
    db.commit()
    return f'Your trip status has been updated to {status} and your car availability status has been updated to {car_status}'
    