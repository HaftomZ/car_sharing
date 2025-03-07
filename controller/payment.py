from models.Payment import DbPayment
from models.Trips import DbTrip
from models.Booking import DbBooking
from sqlalchemy.orm.session import Session
from schemas.paymentSchema import *
from fastapi import HTTPException, status
import uuid
from datetime import datetime,timezone
payment_status_toggle = True
def process_payment(db:Session, request:Paymentbase):
    global payment_status_toggle
    temp_bookings = db.query(DbBooking).filter(DbBooking.booking_id == request.booking_id, DbBooking.booker_id == request.user_id).with_for_update().first()

    if temp_bookings:
     
     trip = db.query(DbTrip).filter(DbTrip.id == temp_bookings.trip_id).first()
     if request.amount != trip.cost:
          raise HTTPException(status_code= status.HTTP_402_PAYMENT_REQUIRED, detail="Amount doesn't match")
     
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
    
     temp_bookings.status= "Confirm"
     db.add(new_payment)
     db.commit()
     db.refresh(new_payment)
     if new_payment.booking_id == None:
         new_payment.refund_status=True

    else:
        raise  HTTPException(status_code= status.HTTP_404_NOT_FOUND)

    return new_payment