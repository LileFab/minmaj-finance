from typing import Optional
from sqlmodel import Session, select
from models.asset import Asset
import yfinance as yf

from services.providers.yahoo import parse_asset_from_yahoo

def get_stock_infos_yahoo(symbol: str) -> Optional[object]:
    """
    Récupère le prix actuel d'une action via Yahoo Finance (ex: "AIR.PA", "AAPL").
    """
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        return info if info is not None else None
    except Exception as e:
        print(f"[Yahoo] Error fetching {symbol}: {e}")
        return None


def create_asset_from_symbol(symbol: str, session: Session) -> Asset:
    # 1. Vérifie si déjà en base
    existing = session.exec(select(Asset).where(Asset.symbol == symbol)).first()
    if existing:
        return existing

    # 2. Va chercher les infos chez Yahoo
    data = get_stock_infos_yahoo(symbol)
    asset_in = parse_asset_from_yahoo(data)

    # 3. Enregistre en base
    asset = Asset.from_orm(asset_in)
    session.add(asset)
    session.commit()
    session.refresh(asset)
    return asset