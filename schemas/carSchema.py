from pydantic import BaseModel

class CarBase(BaseModel): 
    model : str
    license_plate : str
    year : int
    total_seats : int
    smoking_allowed : bool
    wifi_available : bool
    air_conditioning : bool
    pet_friendly : bool
    car_availability_status: str
    owner_id : int

#User inside CarDispaly
class User(BaseModel):
    user_name: str
    email: str
    about: str | None = None
    avatar: str | None = None
    phone_number: str | None = None
    class Config():
        orm_mode= True

class CarDisplay(BaseModel): 
    id:int
    owner_id: int #this is instead of returning user object
    model : str
    license_plate : str
    year : int
    total_seats : int
    smoking_allowed : bool
    wifi_available : bool
    air_conditioning : bool
    pet_friendly : bool
    car_availability_status: str | None = None
    #user : User   #no need now to show the user details , we need it for admin later
    class Config():
        orm_mode = True