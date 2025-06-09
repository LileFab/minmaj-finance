from datetime import datetime
from sqlmodel import SQLModel, Field, Column, String
import uuid
from enum import Enum

class AssetType(str, Enum):
    stock = "stock"
    etf = "etf"
    crypto = "crypto"

class CurrencyType(str, Enum):
    EUR = "EUR"
    USD = "USD"
    crypto = "crypto"

class AssetBase(SQLModel):
    symbol: str = Field(sa_column=Column("symbol", String, unique=True))
    name: str
    type: AssetType
    currency: CurrencyType
    exchange: str
    sector: str
    industry: str
    provider_id: str
    description: str | None = None
    country: str | None = None

class Asset(AssetBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)

class AssetCreate(AssetBase):
    pass
