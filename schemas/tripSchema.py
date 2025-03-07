from pydantic import BaseModel , Field ,  field_validator , model_validator
from datetime import datetime
from typing import Optional
from typing import List
from enum import Enum

class TripStatus(str, Enum):
    scheduled = "scheduled"
    ongoing = "ongoing"
    completed = "completed"
    cancelled = "cancelled"


class TripBase(BaseModel):
    departure_location: str
    destination_location: str
    departure_time : datetime
    arrival_time: datetime
    available_adult_seats: int
    available_children_seats: int
    status: TripStatus #= Field(..., description ="scheduled, ongoing, completed, or cancelled")
    cost: float
    creator_id: int
    car_id : int

    # @model_validator(mode="before")
    # def parse_datetime_fields(cls, values):
    #     # Custom format for parsing datetime fields
    #     departure_time_str = values.get('departure_time')
    #     arrival_time_str = values.get('arrival_time')

    #     # Define the format used in the input (DD-MM-YYYY HH:MM)
    #     datetime_format = '%d-%m-%Y %H:%M'

    #     # Convert string to datetime
    #     if departure_time_str:
    #         try:
    #             values['departure_time'] = datetime.strptime(departure_time_str, datetime_format)
    #         except ValueError:
    #             raise ValueError(f"Invalid format for departure_time. Expected format: {datetime_format}")
        
    #     if arrival_time_str:
    #         try:
    #             values['arrival_time'] = datetime.strptime(arrival_time_str, datetime_format)
    #         except ValueError:
    #             raise ValueError(f"Invalid format for arrival_time. Expected format: {datetime_format}")

    #     return values

    # class Config:
    #     # This will control how the datetime is serialized in the response
    #     json_encoders = {
    #         datetime: lambda v: v.strftime('%d-%m-%Y %H:%M')  # Custom format for datetime
    #     }

   
class Booking(BaseModel):
    booker_id: int 
    status: str
    adult_seats: int
    children_seats: int 
    pickup_location: str
    class Config:
        orm_mode =True

class TripDisplay(BaseModel): 
    id: int 
    departure_location: str
    destination_location: str
    departure_time: datetime
    arrival_time: datetime
    duration: float
    available_adult_seats: int
    available_children_seats: int
    cost: float
    passengers_count: int | None = None
    status: str | None = None
    created_at: str
    updated_at: str | None = None
    car_id: int
    creator_id: int
    trip_booked: List[Booking] = []
   # trip_booked  : Booking
    class Config:
        orm_mode =True
    