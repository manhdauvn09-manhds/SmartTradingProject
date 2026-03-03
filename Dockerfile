# Bước 1: Chọn image Python cơ sở
FROM python:3.10-slim

# Bước 2: Thiết lập thư mục làm việc bên trong container
WORKDIR /app

# Bước 3: Sao chép file requirements và cài đặt thư viện
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Bước 4: Sao chép toàn bộ mã nguồn của ứng dụng vào container
COPY ./data_collector_service ./data_collector_service

# Bước 5: Mở cổng 5000 để có thể truy cập từ bên ngoài
EXPOSE 5000

# Bước 6: Định nghĩa lệnh sẽ được chạy khi container khởi động
CMD ["python", "data_collector_service/web_server.py"]
