from sqlalchemy.orm.session import Session
from schemas.carSchema import CarBase
from models.Cars import DbCar
from models.Users import DbUser
from fastapi import HTTPException , status
import requests
import datetime
import re
from sqlalchemy.exc import IntegrityError
from schemas.carSchema import CarAvailability
from schemas.userSchema import UserBase , userDisplay

def car_validation(request: CarBase):

     #Check car model by calling api from interent which has all cars models
    response = requests.get("https://vpic.nhtsa.dot.gov/api/vehicles/GetMakesForVehicleType/car?format=json")
    car_models = response.json()
    valid_cars= []
    for i in range(0 , len(car_models.get("Results"))):
         valid_cars.append(car_models.get("Results")[i].get("MakeName"))

    if request.model.upper() not in valid_cars:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= f'Model car {request.model} is not a valid model')

    #check license plate according to Dutch patterns
    # XX-99-99 / 99-99-XX / 99-XX-99 / XX-99-XX / XX-XX-99 / 99-XX-XX / 99-XXX-9 / 9-XXX-99 / XX-999-X / X-999-XX / XXX-99-X / 9-XX-999
    # pattern = r"(\w{2}-\d{2}-\d{2})|(\d{2}-\d{2}-\w{2})|(\d{2}-\w{2}-\d{2})|(\w{2}-\d{2}-\w{2})|(\w{2}-\w{2}-\d{2})|(\d{2}-\w{2}-\w{2})|(\d{2}-\w{3}-\d{1})|(\d{1}-\w{3}-\d{2})|(\w{2}-\d{3}-\w{1})|(\w{1}-\d{3}-\w{2})|(\w{3}-\d{2}-\w{1})|(\d{1}-\w{2}-\d{3})"
    # if not re.match(pattern, request.license_plate):
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= f"Invalid license plate {request.license_plate}")
    

    # Check if the year is a 4 digit number within a valid range
    current_year = datetime.datetime.now().year
    if not (1900 <= request.year <= current_year):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= f"Invalid year {request.year}. Must be between 1900 and the current year.")

    #check the total seats
    if not (1 <= request.total_seats <= 7):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= f"Invalid total seats {request.total_seats}. Must be between 1 and 7")
    
    #check the availability status
    if request.car_availability_status.lower() not in [CarAvailability.available , CarAvailability.unavailable]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= f"Invalid availability {request.car_availability_status}, it should be available or unavailable")

    
#create car
def create_car(db: Session, request: CarBase , current_user: userDisplay):
    user = db.query(DbUser).filter(DbUser.id == request.owner_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Owner {request.owner_id} is not existed")
    
    if user.id != current_user.id and not current_user.is_admin: 
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    
    car_validation(request)

    try:
        new_car=DbCar(
            model = request.model,
            license_plate = request.license_plate,
            year = request.year,
            total_seats = request.total_seats,
            smoking_allowed = request.smoking_allowed,
            wifi_available = request.wifi_available,
            air_conditioning = request.air_conditioning,
            pet_friendly = request.pet_friendly,
            car_availability_status = request.car_availability_status,
            owner_id = request.owner_id
        )
        db.add(new_car)
        db.commit()
        db.refresh(new_car)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="License plate already exists")

    return new_car

#get all cars 
def get_all_cars(db: Session, user_id: int):
    car_query = db.query(DbCar)
    if user_id is not None:
        car_query = car_query.filter(DbCar.owner_id == user_id)
   
    return car_query.all()


#get car
def get_car(db: Session, id: int):
   car =  db.query(DbCar).filter(DbCar.id == id).first()
   if not car:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
   return car


#update car details
def update_car(db: Session , car_id: int, request: CarBase, current_user: userDisplay):
    car = db.query(DbCar).filter(DbCar.id == car_id)
    if not car.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    if car.first().owner_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    
    #check if the user that the current user wants to move this car for, is exsited
    new_user= db.query(DbUser).filter(DbUser.id == request.owner_id).first()
    if not new_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f'You can not update this car to be for user {request.owner_id} , because this user is not exsited')
    

    car_validation(request)

    car.update({ 
        DbCar.model : request.model,
        DbCar.license_plate : request.license_plate,
        DbCar.year : request.year,
        DbCar.total_seats : request.total_seats,
        DbCar.smoking_allowed : request.smoking_allowed,
        DbCar.wifi_available : request.wifi_available,
        DbCar.air_conditioning : request.air_conditioning,
        DbCar.pet_friendly : request.pet_friendly,
        DbCar.car_availability_status : request.car_availability_status.lower(),
        DbCar.owner_id : request.owner_id
        })
    db.commit()

    updated_car = db.query(DbCar).filter(DbCar.id == car_id).first()
    return updated_car

#delete car
def delete_car(db: Session, car_id: int, current_user: userDisplay):
    car = db.query(DbCar).filter(DbCar.id == car_id).first()
    if not car:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    if car.owner_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    
    db.delete(car)
    db.commit()
    return 

#update car availability status
def update_car_availability_status(db: Session, user_id: int , car_id: int, car_status: str):
    car = db.query(DbCar).filter(DbCar.id == car_id, DbCar.owner_id == user_id)
    if not car.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f'There is no car with id {car_id}')
    
    car.update({ 
       DbCar.car_availability_status : car_status.lower()
        })
    db.commit()
    return f'Your car availability status has been updated successfully to {car_status}'