from pydantic import BaseModel
from datetime import datetime

class StockData(BaseModel):
    """
    Mô hình dữ liệu đơn giản cho thông tin cổ phiếu.
    Chỉ chứa các thông tin cần thiết mà chúng ta đang thu thập.
    """
    symbol: str
    closing_price: float
    timestamp: datetime
