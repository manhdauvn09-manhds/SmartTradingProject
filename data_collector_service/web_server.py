from flask import Flask, jsonify
import sqlite3

DB_FILE = "stock_data.db"
app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return "<h1>Chào mừng đến với API Dữ liệu Chứng khoán!</h1><p>Truy cập /api/stocks để xem dữ liệu.</p>"

@app.route('/api/stocks', methods=['GET'])
def get_stocks():
    """Lấy 100 bản ghi gần nhất từ database."""
    conn = get_db_connection()
    stocks = conn.execute('SELECT * FROM stocks ORDER BY timestamp DESC LIMIT 100').fetchall()
    conn.close()
    # Chuyển đổi dữ liệu sang dạng list của dictionary để trả về JSON
    return jsonify([dict(ix) for ix in stocks])

if __name__ == '__main__':
    # Chạy server, lắng nghe trên tất cả các địa chỉ IP ở cổng 5000
    app.run(host='0.0.0.0', port=5000, debug=True)
