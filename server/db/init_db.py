from sqlmodel import SQLModel
from db.session import engine

from models.account import Account
from models.asset import Asset
from models.transaction import Transaction
# from models.dividend import DividendSchedule
# from models.price import PriceSnapshot

def init_db():
    SQLModel.metadata.create_all(engine)
