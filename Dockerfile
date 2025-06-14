FROM python:3.12

# Tạo thư mục app và copy mã nguồn
WORKDIR /app
COPY . /app

# Cài đặt dependencies
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && pip install gunicorn uvicorn

# Mở port cho ứng dụng
EXPOSE 8000

# Lệnh chạy server production
CMD ["gunicorn", "app.main:app", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000", "--workers", "4", "--timeout", "60"]
