from sqlalchemy.orm.session import Session
from schemas.carSchema import CarBase
from models.Cars import DbCar
from fastapi import HTTPException , status

#create car
def create_car(db: Session, request: CarBase , user_id: int):
    new_car=DbCar(
        model = request.model,
        year = request.year,
        adult_seats = request.adult_seats,
        childern_seats = request.childern_seats,
        smoking_allowed = request.smoking_allowed,
        wifi_available = request.wifi_available,
        air_conditioning = request.air_conditioning,
        pet_friendly = request.pet_friendly,
        owner_id = user_id
    )
    db.add(new_car)
    db.commit()
    db.refresh(new_car)
    return new_car

#get all cars that are related to a user
def get_all_user_cars(db: Session, user_id: int):
   cars=  db.query(DbCar).filter(DbCar.owner_id == user_id).all()
   if not cars:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No cars are found')
   return cars

#update car details
def update_user_car(db: Session, user_id: int , car_id: int, request: CarBase):
    car = db.query(DbCar).filter(DbCar.id == car_id, DbCar.owner_id == user_id)
    if not car.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f'There is no car with id {car_id}')
    
    car.update({ 
        DbCar.model : request.model,
        DbCar.year : request.year,
        DbCar.adult_seats : request.adult_seats,
        DbCar.childern_seats : request.childern_seats,
        DbCar.smoking_allowed : request.smoking_allowed,
        DbCar.wifi_available : request.wifi_available,
        DbCar.air_conditioning : request.air_conditioning,
        DbCar.pet_friendly : request.pet_friendly,
        DbCar.owner_id : user_id
        })
    db.commit()
    return 'Your car information has been updated successfully!'

#delete car
def delete_user_car(db: Session, user_id: int, car_id: int):
    car = db.query(DbCar).filter(DbCar.id == car_id, DbCar.owner_id == user_id).first()
    if not car:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f'There is no car with id {car_id}')
    
    db.delete(car)
    db.commit()
    return 'Your car has been removed successfully!'

#update car availability status
def update_car_availability_status(db: Session, user_id: int , car_id: int, status: str):
    car = db.query(DbCar).filter(DbCar.id == car_id, DbCar.owner_id == user_id)
    if not car.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f'There is no car with id {car_id}')
    
    car.update({ 
       DbCar.car_availability_status : status
        })
    db.commit()
    return f'Your car availability status has been updated successfully!'