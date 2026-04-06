# ========================================================================
# BİLGE AI - DOCKERFILE
# Temel Imaj: Python 3.9-slim (Hafif ve Güvenli)
# ========================================================================
FROM python:3.9-slim


WORKDIR /app


RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*


COPY gereksinimler.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r gereksinimler.txt


COPY . .


RUN mkdir -p data logs ayarlar


EXPOSE 8000


ENV PYTHONUNBUFFERED=1
ENV APP_ENV=production


CMD ["uvicorn", "src.arayuz.web_sunucu:app", "--host", "0.0.0.0", "--port", "8000"]
