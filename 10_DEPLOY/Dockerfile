# AI Factory OS — Deployment Layer
FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEPLOY_HOST=0.0.0.0 \
    DEPLOY_PORT=8080

# 系统依赖（pandas/openpyxl 可能需要）
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 复制项目
COPY requirements.txt /app/requirements.txt
COPY 10_DEPLOY/requirements.txt /app/10_DEPLOY/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir -r 10_DEPLOY/requirements.txt

COPY . /app

# 数据与日志目录
RUN mkdir -p /app/data /app/logs/deploy /app/output

EXPOSE 8080

WORKDIR /app/10_DEPLOY

CMD ["python", "-m", "uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8080"]
