from fastapi import APIRouter

from api.accounts import router as accounts_router
from api.assets import router as assets_router
from api.transactions import router as transactions_router
# from api.prices import router as prices_router
# from api.dividends import router as dividends_router

router = APIRouter()

router.include_router(accounts_router, prefix="/accounts", tags=["Accounts"])
router.include_router(assets_router, prefix="/assets", tags=["Assets"])
router.include_router(transactions_router, prefix="/transactions", tags=["Transactions"])
# router.include_router(prices_router, prefix="/prices", tags=["Prices"])
# router.include_router(dividends_router, prefix="/dividends", tags=["Dividends"])
