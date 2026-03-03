#!/bin/bash
set -e

PROJECT_DIR="data_collector_service"

echo "Kiểm tra và xóa cấu trúc cũ (nếu có)..."
rm -rf "$PROJECT_DIR"

echo "Tạo cấu trúc thư mục mới..."
mkdir -p "$PROJECT_DIR"/{core,providers,parsers,storage,models,utils}

echo "Tạo các file với nội dung khởi tạo..."

# Thư mục gốc
cat > "$PROJECT_DIR"/main.py << 'EOF'
# Entry point to run the collection jobs
def main():
    print("Data Collector Service is running...")

if __name__ == "__main__":
    main()
EOF

cat > "$PROJECT_DIR"/config.py << 'EOF'
# Configuration (API keys, DB connection, etc.)
DATABASE_URL = "sqlite:///./data.db"
API_KEYS = {
    "VNDIRECT": "YOUR_VNDIRECT_API_KEY",
    "FIREANT": "YOUR_FIREANT_API_KEY"
}
EOF

cat > "$PROJECT_DIR"/scheduler.py << 'EOF'
# Defines and schedules the jobs
import schedule
import time

def job():
    print("Scheduling a job...")

# schedule.every(1).minutes.do(job)

# while True:
#     schedule.run_pending()
#     time.sleep(1)
EOF

# Core
cat > "$PROJECT_DIR"/core/job_manager.py << 'EOF'
# The main orchestrator for a collection task
class JobManager:
    def run(self):
        print("Job manager is running a task.")
EOF

cat > "$PROJECT_DIR"/core/enums.py << 'EOF'
# Enumerations (e.g., DataType, ProviderName)
from enum import Enum

class ProviderName(Enum):
    VNDIRECT = "vndirect"
    FIREANT = "fireant"
EOF

# Providers
touch "$PROJECT_DIR"/providers/__init__.py
cat > "$PROJECT_DIR"/providers/base_provider.py << 'EOF'
# Abstract base class for all data providers
from abc import ABC, abstractmethod

class BaseProvider(ABC):
    @abstractmethod
    def fetch_data(self, symbol: str):
        pass
EOF

cat > "$PROJECT_DIR"/providers/vndirect_provider.py << 'EOF'
# Implementation for VNDIRECT API
from .base_provider import BaseProvider

class VNDirectProvider(BaseProvider):
    def fetch_data(self, symbol: str):
        print(f"Fetching data for {symbol} from VNDIRECT")
        return {}
EOF

cat > "$PROJECT_DIR"/providers/fireant_provider.py << 'EOF'
# Implementation for Fireant API
from .base_provider import BaseProvider

class FireantProvider(BaseProvider):
    def fetch_data(self, symbol: str):
        print(f"Fetching data for {symbol} from Fireant")
        return {}
EOF

# ==============================================================================
# === BẮT ĐẦU SAO CHÉP TỪ ĐÂY ===
# ==============================================================================

# Cập nhật lại main.py và core/job_manager.py để kết nối logic
echo "Cập nhật các file cốt lõi để tạo luồng chạy hoàn chỉnh..."

cat > "$PROJECT_DIR"/main.py << 'EOF'
# Entry point to run the collection jobs
from core.job_manager import JobManager
from core.enums import ProviderName
from storage.database import SessionLocal
from utils.logger import get_logger

logger = get_logger(__name__)

def run_collection_flow():
    """
    Simulates a full data collection flow for a single stock.
    """
    logger.info("Khởi tạo phiên làm việc với cơ sở dữ liệu.")
    db_session = SessionLocal()
    try:
        # Khởi tạo JobManager với session DB
        job_manager = JobManager(db_session=db_session)

        # Chạy tác vụ thu thập cho mã FPT từ VNDIRECT
        logger.info("Bắt đầu tác vụ thu thập cho mã FPT từ VNDIRECT...")
        job_manager.run_collection(symbol="FPT", provider_name=ProviderName.VNDIRECT)

        logger.info("-" * 20)

        # Chạy tác vụ thu thập cho mã VNM từ FIREANT
        logger.info("Bắt đầu tác vụ thu thập cho mã VNM từ FIREANT...")
        job_manager.run_collection(symbol="VNM", provider_name=ProviderName.FIREANT)

    except Exception as e:
        logger.error(f"Đã xảy ra lỗi trong luồng chính: {e}")
    finally:
        logger.info("Đóng phiên làm việc với cơ sở dữ liệu.")
        db_session.close()

if __name__ == "__main__":
    logger.info("===== Bắt đầu dịch vụ thu thập dữ liệu =====")
    run_collection_flow()
    logger.info("===== Dịch vụ đã hoàn thành tác vụ =====")
EOF

cat > "$PROJECT_DIR"/core/job_manager.py << 'EOF'
# The main orchestrator for a collection task
from .enums import ProviderName
from providers.vndirect_provider import VNDirectProvider
from providers.fireant_provider import FireantProvider
from parsers.stock_data_parser import StockDataParser
from storage.repository import StockRepository
from utils.logger import get_logger

logger = get_logger(__name__)

class JobManager:
    def __init__(self, db_session):
        self.db_session = db_session
        self.providers = {
            ProviderName.VNDIRECT: VNDirectProvider(),
            ProviderName.FIREANT: FireantProvider(),
        }
        self.parser = StockDataParser()
        self.repository = StockRepository(session=self.db_session)

    def run_collection(self, symbol: str, provider_name: ProviderName):
        """
        Executes a single data collection task for a given symbol and provider.
        """
        logger.info(f"Bắt đầu chạy tác vụ cho: {symbol} sử dụng {provider_name.value}")

        # 1. Chọn provider và lấy dữ liệu thô
        provider = self.providers.get(provider_name)
        if not provider:
            logger.error(f"Không tìm thấy provider: {provider_name.value}")
            return

        logger.info(f"[{symbol}] Đang lấy dữ liệu từ provider...")
        raw_data = provider.fetch_data(symbol)

        # 2. Phân tích (parse) dữ liệu thô thành mô hình chuẩn
        logger.info(f"[{symbol}] Đang phân tích dữ liệu thô...")
        parsed_data = self.parser.parse(raw_data)

        if not parsed_data:
            logger.error(f"[{symbol}] Phân tích dữ liệu thất bại.")
            return

        # 3. Lưu dữ liệu đã phân tích vào cơ sở dữ liệu
        logger.info(f"[{symbol}] Đang lưu dữ liệu vào repository...")
        self.repository.save(stock_data=parsed_data)

        logger.info(f"Tác vụ cho {symbol} hoàn tất thành công!")
EOF


# Parsers
echo "Tạo các file Parsers..."
touch "$PROJECT_DIR"/parsers/__init__.py

cat > "$PROJECT_DIR"/parsers/base_parser.py << 'EOF'
# Abstract base class for data parsers
from abc import ABC, abstractmethod
from typing import Optional
from models.stock_data import StockData

class BaseParser(ABC):
    @abstractmethod
    def parse(self, raw_data: dict) -> Optional[StockData]:
        """Parses raw data dictionary into a structured StockData model."""
        pass
EOF

cat > "$PROJECT_DIR"/parsers/stock_data_parser.py << 'EOF'
# Logic to parse raw data into our standard models
from datetime import datetime
from typing import Optional

from .base_parser import BaseParser
from models.stock_data import StockData
from utils.logger import get_logger

logger = get_logger(__name__)

class StockDataParser(BaseParser):
    def parse(self, raw_data: dict) -> Optional[StockData]:
        try:
            # Đây là logic giả lập, trong thực tế bạn sẽ ánh xạ các trường
            # từ raw_data (ví dụ: 's', 't', 'o', 'h', 'l', 'c', 'v')
            # sang mô hình StockData của bạn.
            parsed = StockData(
                symbol=raw_data.get("symbol", "UNKNOWN"),
                timestamp=datetime.fromtimestamp(raw_data.get("timestamp", 0)),
                open=raw_data.get("open", 0.0),
                high=raw_data.get("high", 0.0),
                low=raw_data.get("low", 0.0),
                close=raw_data.get("close", 0.0),
                volume=raw_data.get("volume", 0)
            )
            logger.info(f"Phân tích dữ liệu cho mã {parsed.symbol} thành công.")
            return parsed
        except Exception as e:
            logger.error(f"Lỗi khi phân tích dữ liệu: {raw_data}. Lỗi: {e}")
            return None
EOF

# Storage
echo "Tạo các file Storage..."
touch "$PROJECT_DIR"/storage/__init__.py

cat > "$PROJECT_DIR"/storage/database.py << 'EOF'
# Database connection and session management
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL

# engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}) # for SQLite
# Dùng in-memory SQLite cho ví dụ này để không tạo file vật lý
engine = create_engine("sqlite:///:memory:")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
EOF

cat > "$PROJECT_DIR"/storage/repository.py << 'EOF'
# Handles all database operations (CRUD)
from models.stock_data import StockData
from utils.logger import get_logger

logger = get_logger(__name__)

class StockRepository:
    def __init__(self, session):
        self.session = session

    def save(self, stock_data: StockData):
        # Trong một ứng dụng thực tế, bạn sẽ dùng SQLAlchemy model ở đây
        # và thực hiện self.session.add(db_object) và self.session.commit()
        logger.info(
            f"Đang LƯU (giả lập) dữ liệu vào DB cho mã: {stock_data.symbol} "
            f"với giá đóng cửa {stock_data.close} tại thời điểm {stock_data.timestamp}"
        )
        # self.session.add(stock_data)
        # self.session.commit()
        # self.session.refresh(stock_data)
        return stock_data
EOF

# Models
echo "Tạo các file Models..."
touch "$PROJECT_DIR"/models/__init__.py

cat > "$PROJECT_DIR"/models/stock_data.py << 'EOF'
# Pydantic or SQLAlchemy models for our data
from pydantic import BaseModel
from datetime import datetime

class StockData(BaseModel):
    """
    Mô hình dữ liệu chuẩn hóa cho thông tin chứng khoán.
    """
    symbol: str
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int
EOF

# Utils
echo "Tạo các file Utils..."
touch "$PROJECT_DIR"/utils/__init__.py

cat > "$PROJECT_DIR"/utils/http_client.py << 'EOF'
# A resilient HTTP client with retry logic
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def get_http_client() -> requests.Session:
    """
    Tạo một HTTP session với cơ chế retry có sẵn.
    """
    session = requests.Session()
    retry = Retry(
        total=3,
        read=3,
        connect=3,
        backoff_factor=0.3,
        status_forcelist=(500, 502, 504)
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session
EOF

cat > "$PROJECT_DIR"/utils/logger.py << 'EOF'
# Centralized logging setup
import logging
import sys

def get_logger(name: str) -> logging.Logger:
    """
    Thiết lập và trả về một logger tập trung.
    """
    logger = logging.getLogger(name)
    if not logger.handlers: # Tránh thêm handler nhiều lần
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger
EOF

echo "Hoàn tất! Cấu trúc dự án đã được tạo với nội dung khởi tạo đầy đủ."
