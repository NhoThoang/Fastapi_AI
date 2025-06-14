# Dockerfile cho ứng dụng FastAPI
FROM python:3.11-slim

# Cài các gói cần thiết
RUN apt-get update && apt-get install -y gcc libpq-dev curl netcat && rm -rf /var/lib/apt/lists/*

# Tạo thư mục làm việc
WORKDIR /app

# Sao chép và cài đặt yêu cầu
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép mã nguồn
COPY . .

# Cổng
EXPOSE 8000

# Lệnh mặc định khi container khởi chạy
CMD ["gunicorn", "app.main:app", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000", "--workers", "4", "--log-level", "warning", "--timeout", "60"]
