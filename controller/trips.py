from models.Trips import DbTrip
from sqlalchemy.orm.session import Session
from schemas.tripSchema import TripBase

def create_Trip(db: Session, request: TripBase, creator_id: int, car_id: int):
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
    