from uuid import UUID
from datetime import datetime
from pydantic import BaseModel

class TransactionInit(BaseModel):
    account_id: UUID
    symbol: str
    quantity: float
    avg_price: float
    date: datetime
