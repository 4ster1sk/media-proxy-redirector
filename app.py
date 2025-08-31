import os
import psycopg2
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import RedirectResponse
import urllib.parse

# アプリケーション起動時に一度だけ.envを読み込む
load_dotenv()

# 環境変数をグローバル変数として取得
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

ALLOWED_DOMAINS = os.getenv("ALLOWED_DOMAINS", "").split(',')

# FastAPIアプリケーションの初期化
app = FastAPI()

def get_emoji_url(name: str, host: str | None) -> str | None:
    """
    指定されたnameとhostに一致する絵文字のoriginalUrlをデータベースから取得する。
    hostがNoneの場合、'host IS NULL' を条件として検索する。
    """
    conn = None

    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        
        cur = conn.cursor()
        
        if host is None:
            sql_query = "SELECT \"originalUrl\" FROM emoji WHERE name = %s AND host IS NULL;"
            params = (name,)
        else:
            sql_query = "SELECT \"originalUrl\" FROM emoji WHERE name = %s AND host = %s;"
            params = (name, host)
        
        cur.execute(sql_query, params)
        result = cur.fetchone()
        
        if result:
            return result[0]
        
    except Exception as e:
        print(f"An error occurred: {e}")
        # 例外発生時は None を返す
        return None
        
    finally:
        if conn:
            cur.close()
            conn.close()
            
    # レコードが見つからない場合はNoneを返す
    return None

def is_allowed_domain(url: str) -> bool:
    """
    URLのホストが許可されたドメインまたはそのサブドメインに含まれているかを確認する。
    """
    try:
        parsed_url = urllib.parse.urlparse(url)
        host = parsed_url.netloc.lower()

        # 許可されたドメインのリストをチェック
        for allowed_domain in ALLOWED_DOMAINS:
            # 許可されたドメインも正規化
            normalized_allowed_domain = allowed_domain.lower()
            # ドメインが完全に一致するか、またはサブドメインであるかを確認
            if host == normalized_allowed_domain or host.endswith('.' + normalized_allowed_domain):
                return True
    except Exception:
        return False
        
    return False

# 任意のパスを受け取るエンドポイント
@app.get("/{path:path}")
async def redirect_media_url(
    url: str | None = Query(None),
    host: str | None = Query(None),
    isLocal: bool | None = Query(None),
    customEmojiName: str | None = Query(None)):

    # 1. urlが与えられた場合の処理
    if url:
        url = urllib.parse.unquote(url)
        if is_allowed_domain(url):
            return RedirectResponse(url=url, status_code=302)

    # 2. customEmojiNameが与えられた場合の処理
    if customEmojiName:
        name = customEmojiName
        parts = urllib.parse.unquote(name).split('@')
        if len(parts) >=2:
            name, host = parts[:2]
        else:
            host = None if isLocal else host

        emoji_url = get_emoji_url(name=name, host=host)

        if emoji_url:
            return RedirectResponse(url=emoji_url, status_code=302)

    raise HTTPException(status_code=403, detail="Forbidden")
