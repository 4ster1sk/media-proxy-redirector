# media-proxy-redirector

## アーキテクチャ

```
+-------+        +----------------------------+        +-------------+
|       |        |                            |        |             |
| nginx +------->+ media-proxy-redirector     +------->+ media-proxy |
|       |        | (FastAPI / DBチェック)      |        |             |
+-------+        +----------------------------+        +-------------+
```

リクエストの流れ：

1. **nginx** がリクエストを受け取り、FastAPIに転送
2. **media-proxy-redirector** がDBを参照し、DB内に存在するかを確認
   - 未登録なら `403` を返す
   - 登録済みなら `X-Accel-Redirect` ヘッダを付与して返す
3. **nginx** が `X-Accel-Redirect` を受け取り、内部で **media-proxy** に転送
4. **media-proxy** のレスポンスがそのままクライアントに返る

---

## nginx設定例

```nginx
server {
    server_name example.com;

    location /files {
        proxy_pass http://unix:/var/run/proxy/uvicorn.sock:;
    }

    location /media-proxy-internal/ {
        internal;
        resolver 127.0.0.11 valid=30s;
        proxy_pass http://media-proxy/;
    }
}
```

---

## 環境変数 (.env)

| 変数名 | 説明 | デフォルト |
|--------|------|------------|
| `DB_NAME` | DB名 | - |
| `DB_USER` | DBユーザー | - |
| `DB_PASSWORD` | DBパスワード | - |
| `DB_HOST` | DBホスト | - |
| `DB_PORT` | DBポート | `5432` |
| `ALLOWED_DOMAINS` | プロキシを許可するドメイン（カンマ区切り） | - |
| `IS_ALLOW_SENSITIVE_FILE` | センシティブファイルを許可するか | `False` |
| `IS_ALLOW_REMOTE_FILE` | リモートファイルを許可するか | `False` |
| `IS_ALLOW_FEDERATED_DOMAIN` | 連合ドメインを許可するか | `False` |
| `MEDIA_PROXY_PATH` | X-Accel-Redirect用内部パス | `media-proxy` |

---