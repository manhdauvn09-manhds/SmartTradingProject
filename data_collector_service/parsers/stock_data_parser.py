import logging
from datetime import datetime
from models.stock_data import StockData

logger = logging.getLogger(__name__)

class StockDataParser:
    def parse(self, raw_data: dict, symbol: str) -> StockData:
        """
        Phân tích dữ liệu thô từ API Yahoo Finance.
        """
        try:
            # Kiểm tra cấu trúc dữ liệu cơ bản
            if not raw_data or 'chart' not in raw_data or 'result' not in raw_data['chart']:
                logger.warning(f"[{symbol}] Dữ liệu thô từ Yahoo Finance không hợp lệ hoặc rỗng.")
                return self._create_default_stock_data(symbol)

            result = raw_data['chart']['result']
            if not result or result[0] is None:
                logger.warning(f"[{symbol}] Không tìm thấy 'result' trong dữ liệu Yahoo Finance.")
                return self._create_default_stock_data(symbol)

            # Lấy dữ liệu từ phần tử đầu tiên trong 'result'
            data = result[0]
            timestamps = data.get('timestamp', [])
            indicators = data.get('indicators', {}).get('quote', [{}])[0]
            closing_prices = indicators.get('close', [])

            if not timestamps or not closing_prices:
                logger.warning(f"[{symbol}] Không có dữ liệu timestamp hoặc giá đóng cửa.")
                return self._create_default_stock_data(symbol)
            
            # Lấy giá trị cuối cùng (gần nhất) trong danh sách
            # Yahoo có thể trả về giá trị null cho phiên chưa kết thúc, cần lọc bỏ
            latest_price = None
            latest_timestamp = None
            for i in range(len(closing_prices) - 1, -1, -1):
                if closing_prices[i] is not None:
                    latest_price = closing_prices[i]
                    latest_timestamp = timestamps[i]
                    break
            
            if latest_price is None:
                logger.warning(f"[{symbol}] Không tìm thấy giá hợp lệ trong danh sách.")
                return self._create_default_stock_data(symbol)

            trade_date = datetime.fromtimestamp(latest_timestamp)

            logger.info(f"[{symbol}] Phân tích Yahoo Finance thành công: Giá={latest_price}, Thời gian={trade_date}")
            
            return StockData(
                symbol=symbol,
                closing_price=float(latest_price),
                timestamp=trade_date
            )

        except (KeyError, IndexError, TypeError, ValueError) as e:
            logger.error(f"[{symbol}] Xảy ra lỗi khi phân tích dữ liệu Yahoo Finance: {e}")
            return self._create_default_stock_data(symbol)

    def _create_default_stock_data(self, symbol: str) -> StockData:
        """Tạo đối tượng StockData mặc định khi có lỗi."""
        logger.error(f"[{symbol}] Tạo dữ liệu mặc định do lỗi phân tích.")
        return StockData(
            symbol="UNKNOWN",
            closing_price=0.0,
            timestamp=datetime(1970, 1, 1)
        )
