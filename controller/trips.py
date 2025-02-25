from models.Trips import DbTrip
from sqlalchemy.orm.session import Session
from schemas.tripSchema import TripBase
from fastapi import HTTPException , status

def create_trip(db: Session, request: TripBase, creator_id: int, car_id: int):
    #think about arrival time
    trip = DbTrip(
        creator_id = creator_id,
        car_id = car_id,
        departure_location = request.departure_location,
        destination_location = request.destination_location,
        departure_time = request.departure_time,
        available_adult_seats = request.available_adult_seats,
        available_children_seats = request.available_children_seats
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
    
    trip.update({ 
        DbTrip.departure_location : request.departure_location,
        DbTrip.destination_location : request.destination_location,
        DbTrip.departure_time : request.departure_time,
        DbTrip.available_adult_seats : request.available_adult_seats,
        DbTrip.available_children_seats : request.available_children_seats
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
    