from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

@dataclass
class ReturnRecord:
    order_id: str
    product_id: str
    return_date: datetime
    return_reason: str
    refund_amount: float
    customer_comments: Optional[str] = None

@dataclass
class ProductReturnSummary:
    product_id: str
    return_rate: float
    total_returns: int
    total_orders: int
    common_reasons: List[tuple]
    total_refund_amount: float
    last_updated: datetime
