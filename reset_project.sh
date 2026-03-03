#!/bin/bash

# Dừng script nếu có lỗi xảy ra
set -e

PROJECT_DIR="data_collector_service"

# Kiểm tra nếu thư mục đã tồn tại thì xóa nó đi
if [ -d "$PROJECT_DIR" ]; then
    echo "Thư mục '$PROJECT_DIR' đã tồn tại. Đang xóa..."
    rm -rf "$PROJECT_DIR"
    echo "Đã xóa thư mục cũ thành công."
fi

echo "Bắt đầu tạo lại cấu trúc dự án '$PROJECT_DIR'..."

# Tạo lại thư mục gốc và các thư mục con
mkdir -p "$PROJECT_DIR"/{core,providers,parsers,storage,models,utils}

# Tạo các file rỗng
touch "$PROJECT_DIR"/{main.py,config.py,scheduler.py}
touch "$PROJECT_DIR"/core/{job_manager.py,enums.py}
touch "$PROJECT_DIR"/providers/{__init__.py,base_provider.py,vndirect_provider.py,fireant_provider.py}
touch "$PROJECT_DIR"/parsers/{__init__.py,base_parser.py,stock_data_parser.py}
touch "$PROJECT_DIR"/storage/{__init__.py,database.py,repository.py}
touch "$PROJECT_DIR"/models/{__init__.py,stock_data.py}
touch "$PROJECT_DIR"/utils/{__init__.py,http_client.py,logger.py}

echo "Cấu trúc dự án đã được tạo lại thành công!"
