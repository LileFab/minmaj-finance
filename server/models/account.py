from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID, uuid4
from enum import Enum


class AccountType(str, Enum):
    pea = "pea"
    cto = "cto"
    crypto_wallet = "crypto_wallet"
    other = "autre"


class AccountBase(SQLModel):
    name: str
    type: AccountType


class Account(AccountBase, table=True):  # Modèle SQLModel/DB
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)


class AccountCreate(AccountBase):  # Schéma d'entrée (POST)
    pass

