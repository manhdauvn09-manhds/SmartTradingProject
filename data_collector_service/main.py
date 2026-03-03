import logging
from core.job_manager import JobManager
from providers.vndirect_provider import YahooFinanceProvider # Đổi tên import
# from providers.fireant_provider import FireantProvider # Tạm thời không dùng
from parsers.stock_data_parser import StockDataParser
from storage.repository import StockRepository
from scheduler import Scheduler

# Cấu hình logging cơ bản
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def main():
    logging.info("======== Bắt đầu dịch vụ thu thập dữ liệu ========")
    
    # 1. Khởi tạo các thành phần
    parser = StockDataParser()
    repository = StockRepository()
    
    # 2. Tạo danh sách các providers
    providers = {
        "yahoo": YahooFinanceProvider(),
        # "fireant": FireantProvider() # Tạm thời vô hiệu hóa
    }
    
    # 3. Khởi tạo JobManager
    job_manager = JobManager(providers, parser, repository)
    
    # 4. Danh sách các mã cổ phiếu cần lấy dữ liệu
    symbols = ["FPT", "VNM", "HPG", "ACB"]
    
    # 5. Khởi tạo và chạy Scheduler
    scheduler = Scheduler(job_manager, symbols)
    scheduler.run_all_jobs_once() # Chạy tất cả các job một lần để kiểm tra
    
    # Nếu muốn chạy định kỳ, bạn có thể dùng scheduler.start()
    # logging.info("Scheduler đã bắt đầu, sẽ chạy các tác vụ theo lịch trình.")
    # scheduler.start()

    logging.info("======== Dịch vụ đã hoàn thành tác vụ ========")


if __name__ == "__main__":
    main()
