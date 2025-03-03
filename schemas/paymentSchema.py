from pydantic import BaseModel
from typing import Optional
class PaymentRequest(BaseModel):
    booking_id: int
    user_id: int
    amount: float
    currency: str
    payment_method: str

class PaymentResponse(BaseModel):
    message: str
    transaction_id: str
    status: str
