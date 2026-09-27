import sys
import types

# app.config は import 時に .env を必須とし DB 接続設定を読むため、
# テストでは必要な値だけを持つダミーモジュールに差し替える
config = types.ModuleType("app.config")
config.IS_ALLOW_SENSITIVE_FILE = False
config.IS_ALLOW_REMOTE_FILE = False
config.IS_ALLOW_FEDERATED_DOMAIN = False
config.ALLOWED_DOMAINS = ["tomadoi.com"]
config.MEDIA_PROXY_PATH = "media-proxy"
config.SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://user:pass@localhost/test"
sys.modules["app.config"] = config
