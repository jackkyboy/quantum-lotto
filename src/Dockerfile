# ---- Builder ----
FROM python:3.11-slim AS builder
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
RUN apt-get update && apt-get install -y --no-install-recommends build-essential && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ---- Runtime ----
FROM python:3.11-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 \
    ENV=production \
    PYTHONPATH=/app
# (ถ้าใช้ SQLite) เตรียมโฟลเดอร์สำหรับไฟล์ฐานข้อมูล
RUN mkdir -p /app/storage
# คัดลอกไลบรารีจาก builder
COPY --from=builder /install /usr/local
# คัดลอกซอร์สโค้ด
COPY . .
EXPOSE 8000
# คำสั่งรันโปรดักชัน: Gunicorn + Uvicorn worker
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "-w", "2", "-b", "0.0.0.0:8000", "src.api.app:app"]
