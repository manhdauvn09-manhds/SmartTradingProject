import logging
from parsers.stock_data_parser import StockDataParser
from storage.repository import StockRepository

logger = logging.getLogger(__name__)

class JobManager:
    def __init__(self, providers: dict, parser: StockDataParser, repository: StockRepository):
        """
        Khởi tạo JobManager với các thành phần cần thiết.
        - providers: Một dictionary chứa các provider, ví dụ {'yahoo': YahooProvider()}
        - parser: Một đối tượng parser để phân tích dữ liệu.
        - repository: Một đối tượng repository để lưu trữ dữ liệu.
        """
        self.providers = providers
        self.parser = parser
        self.repository = repository
        logger.info(f"JobManager đã được khởi tạo với các providers: {list(self.providers.keys())}")

    def run_job(self, symbol: str, provider_name: str):
        """
        Thực thi một tác vụ thu thập dữ liệu cho một mã cổ phiếu từ một provider cụ thể.
        """
        logger.info(f"====== Bắt đầu tác vụ cho [{symbol}] từ [{provider_name}] ======")
        
        provider = self.providers.get(provider_name)
        if not provider:
            logger.error(f"Không tìm thấy provider với tên '{provider_name}'. Bỏ qua tác vụ.")
            return

        try:
            # 1. Lấy dữ liệu thô
            logger.info(f"[{symbol}] Đang lấy dữ liệu từ {provider.name}...")
            raw_data = provider.fetch_data(symbol)

            if not raw_data:
                logger.warning(f"[{symbol}] Không nhận được dữ liệu từ {provider.name}.")
                return

            # 2. Phân tích dữ liệu
            logger.info(f"[{symbol}] Đang phân tích dữ liệu thô...")
            stock_data = self.parser.parse(raw_data, symbol)

            # 3. Lưu trữ dữ liệu
            if stock_data and stock_data.symbol != "UNKNOWN":
                logger.info(f"[{symbol}] Đang lưu dữ liệu vào repository...")
                self.repository.save(stock_data)
                logger.info(f"[{symbol}] Đã lưu dữ liệu thành công.")
            else:
                logger.error(f"[{symbol}] Phân tích dữ liệu thất bại hoặc dữ liệu không hợp lệ.")

        except Exception as e:
            logger.critical(f"[{symbol}] Đã xảy ra lỗi nghiêm trọng trong quá trình chạy job: {e}", exc_info=True)
        finally:
            logger.info(f"====== Kết thúc tác vụ cho [{symbol}] từ [{provider_name}] ======")
