import schedule
import time
import logging
from core.job_manager import JobManager

logger = logging.getLogger(__name__)

class Scheduler:  # <--- ĐẢM BẢO CHỮ 'S' ĐƯỢC VIẾT HOA
    def __init__(self, job_manager: JobManager, symbols: list):
        self.job_manager = job_manager
        self.symbols = symbols
        self._setup_schedule()

    def _setup_schedule(self):
        """Lên lịch cho các tác vụ. Hiện tại đang đặt lịch giả lập."""
        logger.info("Đang thiết lập lịch trình cho các tác vụ...")
        # Ví dụ: Chạy tác vụ cho FPT mỗi 10 giây
        # schedule.every(10).seconds.do(self.job_manager.run_job, symbol='FPT', provider_name='yahoo')
        
        # Ví dụ: Chạy tất cả các mã mỗi 5 phút
        # for symbol in self.symbols:
        #     schedule.every(5).minutes.do(self.job_manager.run_job, symbol=symbol, provider_name='yahoo')
        
        logger.info("Thiết lập lịch trình hoàn tất.")

    def run_all_jobs_once(self):
        """Chạy tất cả các tác vụ một lần ngay lập tức để kiểm tra."""
        logger.info("Bắt đầu chạy tất cả các tác vụ một lần...")
        for symbol in self.symbols:
            # Hiện tại chúng ta chỉ có provider 'yahoo'
            self.job_manager.run_job(symbol=symbol, provider_name='yahoo')
        logger.info("Đã hoàn thành chạy tất cả các tác vụ.")

    def start(self):
        """Bắt đầu vòng lặp của scheduler."""
        logger.info("Scheduler đang bắt đầu...")
        while True:
            schedule.run_pending()
            time.sleep(1)
