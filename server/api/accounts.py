from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from db.session import engine
from models.account import Account, AccountCreate

router = APIRouter()


def get_session():
    with Session(engine) as session:
        yield session


@router.get("/", response_model=list[Account])
def get_accounts(session: Session = Depends(get_session)):
    return session.exec(select(Account)).all()


@router.post("/", response_model=Account, status_code=status.HTTP_201_CREATED)
def create_account(account_in: AccountCreate, session: Session = Depends(get_session)):
    existing = session.exec(select(Account).where(Account.name == account_in.name)).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this name already exists."
        )
    
    account = Account.from_orm(account_in)
    session.add(account)
    session.commit()
    session.refresh(account)
    return account


@router.get("/{account_id}", response_model=Account)
def get_account(account_id: str, session: Session = Depends(get_session)):
    account = session.get(Account, account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account
