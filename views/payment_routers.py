from schemas.paymentSchema import*
from fastapi import APIRouter, Depends,status
from sqlalchemy.orm import Session
from config.db_connect import get_db
from controller import payment
from schemas.userSchema import userDisplay 
from controller.authentication import get_current_user
router = APIRouter(
    prefix="/payments", 
    tags=["payments"]
    )

@router.post('/',response_model=PaymentResponse,status_code=status.HTTP_201_CREATED)
def payment_process(req:Paymentbase, db: Session= Depends(get_db)):
 return payment.create_payment(db,req)
@router.get('/', response_model=list[PaymentResponse])
def get_payments(user_id:int=None,db: Session= Depends(get_db),current_user: userDisplay = Depends(get_current_user)):
 return payment.get_payments(db,user_id,current_user)
@router.get('/{id}',response_model=PaymentResponse)
def get_a_payment(id : int, db: Session= Depends(get_db),current_user: userDisplay = Depends(get_current_user)):
 return payment.get_a_payment(db,id,current_user)