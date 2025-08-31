FROM python:3.11-slim

# 作業ディレクトリを /app に設定
WORKDIR /app

# プロジェクトに必要なファイルをコピー
COPY app.py .
COPY requirements.txt .

# 依存関係をインストール
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# ポストグレスのクライアントライブラリをインストール
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# entrypoint.shをコピーして実行権限を付与
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

# Unixソケットをリッスンするディレクトリを作成
RUN mkdir -p /var/run/redirect-restrictor

# エントリーポイントを設定
ENTRYPOINT ["/app/entrypoint.sh"]

# アプリケーションを起動
# sh -c '...' を使うことで、ENTRYPOINTで設定された環境変数($WORKERS)を展開する
CMD ["sh", "-c", "uvicorn app:app --uds /var/run/redirect-restrictor/http.sock --workers $WORKERS"]
