from sqlmodel import SQLModel, Field
from uuid import uuid4, UUID
from enum import Enum
from datetime import datetime

class TransactionType(str, Enum):
    buy = "buy"
    sell = "sell"

class TransactionBase(SQLModel):
    asset_id: UUID
    account_id: UUID
    date: datetime = Field(default_factory=datetime.now)
    type: TransactionType
    quantity: float
    price: float
    fee: float = 0.0
    is_initial: bool = False  # 👈 ajouté pour marquer une ligne d'init

class Transaction(TransactionBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)

class TransactionCreate(TransactionBase):
    pass