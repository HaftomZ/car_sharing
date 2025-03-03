from schemas.paymentSchema import*
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from config.db_connect import get_db
from controller import payment
from enum import Enum
import random

router = APIRouter(
    prefix="/payments", 
    tags=["Payments"]
    )

class PaymentStatus(str,Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
class PaymentMethod(str, Enum):
    CREDIT_CARD = "Credit Card"
    PAYPAL = "PayPal"
    CASH = "Cash"


