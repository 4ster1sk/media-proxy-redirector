from app.config import (
    IS_ALLOW_SENSITIVE_FILE,
    IS_ALLOW_REMOTE_FILE,
    IS_ALLOW_FEDERATED_DOMAIN,
    ALLOWED_DOMAINS,
)
from fastapi import Depends, FastAPI, HTTPException, Request
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse

from urllib.parse import urlparse
from app.database import get_db
from app.model.db.drive_file import DriveFile
from app.model.db.emoji import Emoji
from app.model.db.instance import MiInstance
from app.exception import (
    SensitiveFileNotAllowedException,
    RemoteFileNotAllowedException,
)

app = FastAPI()


def is_allowed_domain(url: str) -> bool:
    """
    URLのホストが許可されたドメインまたはそのサブドメインに含まれているかを確認する。
    """
    parsed_url = urlparse(url)
    host = parsed_url.netloc.lower()

    # 許可されたドメインのリストをチェック
    for allowed_domain in ALLOWED_DOMAINS:
        # 許可されたドメインも正規化
        normalized_allowed_domain = allowed_domain.lower()
        # ドメインが完全に一致するか、またはサブドメインであるかを確認
        if host == normalized_allowed_domain or host.endswith(
            "." + normalized_allowed_domain
        ):
            return True

    return False


def is_federated_domain(url: str, db: Session) -> bool:
    """
    URLのホストが連合しているかDBで確認する(完全一致)。
    """
    parsed_url = urlparse(url)
    host = parsed_url.netloc.lower()

    if not host:
        return False

    result = db.query(MiInstance).filter(MiInstance.host == host).first()
    if result:
        return True

    return False


def is_exist_emoji(url: str, db: Session) -> bool:
    parsed = urlparse(url)
    emoji = db.query(Emoji).filter(Emoji.publicUrl == parsed.geturl()).first()
    if emoji:
        return True

    return False


def get_file(web_public_access_key: str, db: Session) -> str | None:
    file = (
        db.query(DriveFile)
        .filter(DriveFile.webpublicAccessKey == web_public_access_key)
        .first()
    )

    if file:
        if (file.isSensitive) and (not IS_ALLOW_SENSITIVE_FILE):
            raise SensitiveFileNotAllowedException()

        if (file.userHost is not None) and (not IS_ALLOW_REMOTE_FILE):
            raise RemoteFileNotAllowedException()

        return file.url
    return None


@app.get("/proxy/{proxy_path:path}")
async def proxy_any(proxy_path: str, request: Request, db: Session = Depends(get_db)):
    print("=== proxy_path:", proxy_path)
    if "url" not in request.query_params.keys():
        raise HTTPException(
            status_code=403, detail="'url' query parameter is required"
        )

    url = request.query_params.get("url", "")
    try:
        if is_allowed_domain(url):
            return RedirectResponse(url=url, status_code=302)

        elif IS_ALLOW_FEDERATED_DOMAIN and is_federated_domain(url, db):
            return RedirectResponse(url=url, status_code=302)

        elif (
            proxy_path in ["emoji.webp", "image.webp", "static.webp", "avatar.webp"]
        ) and is_exist_emoji(url, db):
            return RedirectResponse(url=url, status_code=302)

        raise HTTPException(
            status_code=403, detail="Forbidden domain or recursive proxy redirect"
        )
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500)


@app.get("/files/{web_public_access_key:path}")
async def proxy_files(
    web_public_access_key: str, request: Request, db: Session = Depends(get_db)
):
    print("=== key_path:", web_public_access_key)

    try:
        path = get_file(web_public_access_key, db)
        if path:
            return RedirectResponse(url=path, status_code=302)

    except SensitiveFileNotAllowedException:
        raise HTTPException(
            status_code=403, detail="Sensitive file access is not allowed."
        )
    except RemoteFileNotAllowedException:
        raise HTTPException(
            status_code=403, detail="Remote file access is not allowed."
        )
    except Exception:
        raise HTTPException(status_code=500)

    raise HTTPException(status_code=404, detail="Not Found")
