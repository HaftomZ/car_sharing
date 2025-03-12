from models.Payment import DbPayment
from models.Trips import DbTrip
from models.Booking import DbBooking
from models.Users import DbUser
from sqlalchemy.orm.session import Session
from schemas.paymentSchema import *
from fastapi import HTTPException, status
import uuid
from datetime import datetime,timezone
from schemas.userSchema import UserBase,userDisplay 
from controller.authentication import get_current_user

payment_status_toggle = True
payment_methods =["visa","paypal","apple pay","google pay","ideal"]
def create_payment(db:Session, request:Paymentbase):
    global payment_status_toggle
    temp_bookings = db.query(DbBooking).filter(DbBooking.booking_id == request.booking_id, DbBooking.booker_id == request.user_id).with_for_update().first()

    if temp_bookings:
     
     trip = db.query(DbTrip).filter(DbTrip.id == temp_bookings.trip_id).first()
     if trip.status=="cancelled":
         raise  HTTPException(status_code= status.HTTP_404_NOT_FOUND,detail= "trip is cancelled")
     total_cost = trip.cost *(temp_bookings.adult_seats + temp_bookings.children_seats)
     if request.amount != total_cost:
          raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,detail=f"Incorrect payment amount. Expected {total_cost} but received {request.amount}.")
     if request.payment_method.lower() not in payment_methods:
          raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Invalid payment method.")

     transaction_status = "completed" if payment_status_toggle else "failed"
     payment_status_toggle = not payment_status_toggle
     if transaction_status == "failed":
         raise HTTPException(status_code= status.HTTP_402_PAYMENT_REQUIRED, detail="Payment process failed")
     
     transaction_id = f"TXN-{uuid.uuid4().hex[:10].upper()}"
     new_payment = DbPayment(
        booking_id=request.booking_id,
        user_id=request.user_id,
        amount=request.amount,
        currency=request.currency,
        status=transaction_status,
        payment_method=request.payment_method,
        transaction_reference=transaction_id,
        created_at = datetime.now(timezone.utc)
       
        )
    
     temp_bookings.status= "Confirmed"
     db.add(new_payment)
     db.commit()
     db.refresh(new_payment)
     if new_payment.booking_id == None:
         new_payment.refund_status=True

    else:
        raise  HTTPException(status_code= status.HTTP_404_NOT_FOUND,detail= "No booking found")

    return new_payment

def get_payments(db:Session,user_id:int,current_user:userDisplay):
    payments = db.query(DbPayment)
    if user_id is not None:
      users = db.query(DbUser).filter(DbUser.id==user_id).first()
      if user_id != current_user.id and current_user.is_admin != True:
          raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail="Not allowed")
      if not users:
          raise  HTTPException(status_code = status.HTTP_404_NOT_FOUND) 
      payments = payments.filter(DbPayment.user_id == user_id)
    else:
        if current_user.is_admin != True:
             raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail="You must be an admin")
    return payments.all()
def get_a_payment(db:Session,payment_id:int,current_user:userDisplay):
    payments = db.query(DbPayment).filter(DbPayment.payment_id == payment_id).first()
    if current_user is None: 
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not logged in")
    if not payments:
        raise  HTTPException(status_code = status.HTTP_404_NOT_FOUND) 
    if payments.user_id != current_user.id:
         raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail="Not allowed")
    return payments