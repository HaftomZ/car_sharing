from schemas.paymentSchema import*
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from config.db_connect import get_db
from controller import payment

router = APIRouter(
    prefix="/payments", 
    tags=["Payments"]
    )

@router.post('/')
def payment_process(req:Paymentbase, db: Session= Depends(get_db)):
 return payment.process_payment(db,req)