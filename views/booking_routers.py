from schemas.bookingSchema import*
from fastapi import APIRouter, Depends,status
from sqlalchemy.orm import Session
from config.db_connect import get_db
from controller import booking
from schemas.userSchema import UserBase,userDisplay 
from controller.authentication import get_current_user


router = APIRouter(
    prefix="/bookings",
    tags=['booking']
)

@router.post('/', response_model=BookingDisplay, status_code=status.HTTP_201_CREATED)
def create_booking(req: BookingBase,db: Session= Depends(get_db),current_user: userDisplay = Depends(get_current_user)):
    return booking.create_booking(db,req,current_user.id)
  
@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def cancel_booking(id: int, db: Session= Depends(get_db),current_user: userDisplay = Depends(get_current_user)):
    return booking.cancel_booking(db,id,current_user.id)

@router.put('/{id}')
def update_my_bookings(id: int, req: BookingBase, db: Session= Depends(get_db),current_user: userDisplay = Depends(get_current_user)):
    return booking.update_my_bookings(db,id, req,current_user.id)

@router.get('/', response_model= list[listBookingResponse])
def list_of_bookings(user_id: int= None, db: Session= Depends(get_db),current_user: userDisplay = Depends(get_current_user)):
    return booking.list_of_bookings(db, user_id,current_user.id)

@router.get('/{id}')
def get_a_booking(id:int, db: Session= Depends(get_db),current_user: userDisplay = Depends(get_current_user)):
    return booking.get_a_booking(db,id,current_user.id)
