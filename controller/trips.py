from models.Trips import DbTrip
from sqlalchemy.orm.session import Session
from schemas.tripSchema import TripBase, TripResponse
def create_Trips(db: Session, request: TripBase):
    trips = DbTrip(
        triper_id=request.triper_id,
        car_id=request.car_id,
        available_adult_seats=request.available_adult_seats,
        available_children_seats=request.available_children_seats,
        status=request.status,
        departure_location=request.departure_location,
        destination_location=request.destination_location,
        departure_time=request.departure_time
        )
    db.add(trips)
    db.commit()
    db.refresh(trips)
    return TripResponse(
        status=trips.status,
        created_at=trips.created_at,
        updated_at=trips.updated_at,
        departure_time=trips.departure_time,
        message="Trip created successfully"
    )