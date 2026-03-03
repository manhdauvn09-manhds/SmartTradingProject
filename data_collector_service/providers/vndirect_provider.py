import requests
import logging

logger = logging.getLogger(__name__)

class YahooFinanceProvider:
    def __init__(self):
        self.name = "YahooFinance"
        # URL cơ bản của API Yahoo Finance
        self.base_url = "https://query1.finance.yahoo.com/v8/finance/chart"

    def fetch_data(self, symbol: str) -> dict:
        """
        Lấy dữ liệu từ API của Yahoo Finance.
        Lưu ý: Mã cổ phiếu Việt Nam trên Yahoo cần có hậu tố .VN (ví dụ: FPT.VN)
        """
        yahoo_symbol = f"{symbol.upper()}.VN"
        url = f"{self.base_url}/{yahoo_symbol}"
        
        # Các tham số cho request: lấy dữ liệu 1 ngày gần nhất, interval 15 phút
        params = {
            'range': '1d',
            'interval': '15m'
        }
        
        # Header User-Agent là cần thiết để tránh bị chặn
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        logger.info(f"[{self.name}] Đang gọi URL: {url} với mã: {yahoo_symbol}")
        
        try:
            response = requests.get(url, params=params, headers=headers, timeout=15)
            
            # Kiểm tra nếu request không thành công
            response.raise_for_status() 
            
            logger.info(f"[{self.name}] Nhận được Status Code: {response.status_code}")
            return response.json()

        except requests.exceptions.HTTPError as http_err:
            logger.error(f"[{self.name}] Lỗi HTTP: {http_err} - Nội dung: {response.text}")
            return {}
        except Exception as e:
            logger.error(f"[{self.name}] Đã xảy ra lỗi khi gọi API Yahoo Finance: {e}")
            return {}
