from dataclasses import dataclass


@dataclass
class TradingResultDTO:
    exchange_product_id: str
    exchange_product_name: str
    delivery_basis_name: str
    volume: int
    total: int
    count: int




