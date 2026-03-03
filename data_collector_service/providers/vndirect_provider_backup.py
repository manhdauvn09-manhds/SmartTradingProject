# Implementation for VNDIRECT API
from .base_provider import BaseProvider

class VNDirectProvider(BaseProvider):
    # Dòng 6
    def fetch_data(self, symbol):
        # Dòng 7 (Đã được thụt vào 4 dấu cách)
        url = f"https://api.vndirect.com.vn/v4/stock_data?code={symbol}"
        print(f"--- DEBUG VNDIRECT ---")
        print(f"Đang gọi URL: {url}")
        try:
            # Giả sử bạn dùng thư viện requests
            import requests 
            # Đoạn code dưới đây cũng phải thụt vào
            response = requests.get(url, timeout=10) 
            print(f"Status Code nhận được: {response.status_code}")
            print(f"Nội dung phản hồi (dạng text): {response.text}")
            if response.status_code == 200:
                return response.json()
            else:
                return {}
        except Exception as e:
            # Dòng này cũng phải thụt vào
            print(f"Đã xảy ra lỗi khi gọi API: {e}")
            return {}
