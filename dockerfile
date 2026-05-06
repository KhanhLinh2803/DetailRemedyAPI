# Sử dụng Python 3.10 bản rút gọn (slim) để nhẹ và ổn định
FROM python:3.10-slim

# Thiết lập thư mục làm việc trong container
WORKDIR /app

# Sao chép file danh sách thư viện vào trước để tận dụng cache
COPY requirements.txt .

# Cài đặt các thư viện cần thiết
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép toàn bộ mã nguồn vào container
COPY . .

# Render yêu cầu ứng dụng chạy trên port do họ cấp qua biến $PORT
# Nếu không có $PORT thì mặc định là 8000
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]