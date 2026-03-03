import sqlite3
import logging
from models.stock_data import StockData

logger = logging.getLogger(__name__)
DB_FILE = "stock_data.db"

class StockRepository:
    def __init__(self):
        self.conn = sqlite3.connect(DB_FILE, check_same_thread=False)
        self._create_table()
        logger.info(f"StockRepository đã kết nối tới database SQLite tại: {DB_FILE}")

    def _create_table(self):
        """Tạo bảng 'stocks' nếu nó chưa tồn tại."""
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS stocks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT NOT NULL,
                closing_price REAL NOT NULL,
                timestamp TEXT NOT NULL,
                UNIQUE(symbol, timestamp)
            )
        """)
        self.conn.commit()

    def save(self, stock_data: StockData):
        """Lưu dữ liệu vào database, nếu bị trùng thì bỏ qua."""
        sql = ''' INSERT OR IGNORE INTO stocks(symbol, closing_price, timestamp)
                  VALUES(?,?,?) '''
        cursor = self.conn.cursor()
        try:
            cursor.execute(sql, (
                stock_data.symbol,
                stock_data.closing_price,
                stock_data.timestamp.isoformat()
            ))
            self.conn.commit()
            logger.info(f"Đã LUU vào DB cho mã: {stock_data.symbol}")
        except Exception as e:
            logger.error(f"Lỗi khi lưu vào DB cho mã {stock_data.symbol}: {e}")
