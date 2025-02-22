from pydantic import BaseModel

class CarBase(BaseModel): 
    model : str
    year : int
    adult_seats : int
    childern_seats : int
    smoking_allowed : bool
    wifi_available : bool
    air_conditioning : bool
    pet_friendly : bool
    #owner_id : int

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
    model : str
    year : int
    adult_seats : int
    childern_seats : int
    smoking_allowed : bool
    wifi_available : bool
    air_conditioning : bool
    pet_friendly : bool
    #user : User   #no need now to show the user details , we need it for admin later
    class Config():
        orm_mode = True