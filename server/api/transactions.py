from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from db.session import engine
from models.transaction import Transaction, TransactionType, TransactionCreate
from models.asset import Asset
from schemas.transaction import TransactionInit

router = APIRouter()

def get_session():
    with Session(engine) as session:
        yield session

@router.get("/", response_model=list[Transaction])
def get_all_transactions(session: Session = Depends(get_session)):
    return session.exec(select(Transaction)).all()

@router.post("/init", status_code=status.HTTP_201_CREATED)
def init_position(data: TransactionInit, session: Session = Depends(get_session)):
    asset = session.exec(select(Asset).where(Asset.symbol == data.symbol)).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")

    txn = Transaction(
        asset_id=asset.id,
        account_id=data.account_id,
        quantity=data.quantity,
        price=data.avg_price,
        date=data.date,
        type=TransactionType.buy,
        is_initial=True,
    )
    session.add(txn)
    session.commit()
    session.refresh(txn)
    return txn

@router.post("/", response_model=Transaction, status_code=status.HTTP_201_CREATED)
def create_transaction(
    data: TransactionCreate,
    session: Session = Depends(get_session)
):
    txn = Transaction(**data.dict())
    session.add(txn)
    session.commit()
    session.refresh(txn)
    return txn

@router.delete("/last", status_code=status.HTTP_204_NO_CONTENT)
def delete_last_transaction(session: Session = Depends(get_session)):
    last_txn = session.exec(
        select(Transaction).order_by(Transaction.date.desc())
    ).first()

    if not last_txn:
        raise HTTPException(status_code=404, detail="No transaction found")

    session.delete(last_txn)
    session.commit()