from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from db.session import engine
from models.asset import Asset
from services.asset import create_asset_from_symbol

router = APIRouter()

def get_session():
    with Session(engine) as session:
        yield session

@router.get("/", response_model=list[Asset])
def get_assets(session: Session = Depends(get_session)):
    return session.exec(select(Asset)).all()


@router.post("/", response_model=Asset, status_code=status.HTTP_201_CREATED)
def create_account(symbol_in: str, session: Session = Depends(get_session)):
    existing = session.exec(select(Asset).where(Asset.symbol == symbol_in)).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An asset with this symbol already exists."
        )
    
    asset = create_asset_from_symbol(symbol_in, session)

    return asset

@router.get("/{asset_symbol}", response_model=Asset)
def get_asset_by_symbol(asset_symbol: str, session: Session = Depends(get_session)):
    statement = select(Asset).where(Asset.symbol == asset_symbol)
    result = session.exec(statement).first()
    if not result:
        raise HTTPException(status_code=404, detail="Asset not found")
    return result
