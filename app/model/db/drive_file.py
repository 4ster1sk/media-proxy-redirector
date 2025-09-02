from sqlalchemy import Boolean, Column, Integer, String, text
from sqlalchemy.dialects.postgresql import JSONB

from .base import Base


class DriveFile(Base):
    __tablename__ = "drive_file"

    # Columns
    id = Column(String(32), primary_key=True, nullable=False)
    userId = Column(String(32), nullable=True)
    userHost = Column(String(128), nullable=True)
    md5 = Column(String(32), nullable=False)
    name = Column(String(256), nullable=False)
    column_type = Column("type", String(128), nullable=False)
    size = Column(Integer, nullable=False)
    comment = Column(String(512), nullable=True)
    properties = Column(JSONB, nullable=False, server_default=text("'{}'::jsonb"))
    storedInternal = Column(Boolean, nullable=False)
    url = Column(String(1024), nullable=False)
    thumbnailUrl = Column(String(512), nullable=True)
    webpublicUrl = Column(String(512), nullable=True)
    accessKey = Column(String(256), nullable=True)
    thumbnailAccessKey = Column(String(256), nullable=True)
    webpublicAccessKey = Column(String(256), nullable=True)
    uri = Column(String(1024), nullable=True)
    src = Column(String(1024), nullable=True)
    folderId = Column(String(32), nullable=True)
    isSensitive = Column(Boolean, nullable=False, server_default=text("false"))
    isLink = Column(Boolean, nullable=False, server_default=text("false"))
    blurhash = Column(String(128), nullable=True)
    webpublicType = Column(String(128), nullable=True)
    requestHeaders = Column(JSONB, nullable=True, server_default=text("'{}'::jsonb"))
    requestIp = Column(String(128), nullable=True)
    maybeSensitive = Column(Boolean, nullable=False, server_default=text("false"))
    maybePorn = Column(Boolean, nullable=False, server_default=text("false"))

    def __repr__(self):
        return f"<DriveFile(id='{self.id}', name='{self.name}')>"
