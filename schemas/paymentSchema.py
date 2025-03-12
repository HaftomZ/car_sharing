from pydantic import BaseModel
from typing import Optional
from datetime import datetime
class Paymentbase(BaseModel):
    booking_id: int
    user_id: int
    amount: float
    currency: str
    payment_method: str

class PaymentResponse(BaseModel):
    payment_id: int
    booking_id: Optional[int ]
    user_id: int
    amount: float
    currency: str
    status: str
    payment_method: str
    transaction_reference: str
    created_at : datetime
    refund_status: bool = False
   
