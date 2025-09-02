FROM python:3.12-slim

ARG UID="1000"
ARG GID="1000"

# 作業ディレクトリを /app に設定
WORKDIR /app

COPY requirements.txt .

# 依存関係をインストール
RUN pip install --no-cache-dir --upgrade -r requirements.txt

RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

RUN groupadd -g "${GID}" user \
    && useradd -l -u "${UID}" -g "${GID}" -m -s /bin/bash user

COPY app ./app

USER user
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port 3000 --workers ${WORKERS:-5}"]