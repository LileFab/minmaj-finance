from models.asset import AssetCreate, AssetType


def parse_asset_from_yahoo(data: dict) -> AssetCreate:
    try:
        symbol = data["symbol"]
        name = data.get("longName") or data.get("shortName") or symbol
        currency = data["currency"]
        exchange = data["exchange"]
        sector = data["sector"]
        industry = data["industry"]
        quote_type = data.get("quoteType", "").lower()

        if quote_type == "equity":
            asset_type = AssetType.stock
        elif quote_type == "etf":
            asset_type = AssetType.etf
        elif quote_type == "crypto":
            asset_type = AssetType.crypto
        else:
            raise ValueError(f"Unsupported quoteType: {quote_type}")

        description = data.get("longBusinessSummary")
        country = data.get("country")

        return AssetCreate(
            symbol=symbol,
            name=name,
            currency=currency,
            type=asset_type,
            exchange=exchange,
            sector=sector,
            industry=industry,
            provider_id=symbol,
            description=description,
            country=country,
        )

    except KeyError as e:
        raise ValueError(f"Missing required key in Yahoo data: {e}")
