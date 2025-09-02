from sqlalchemy import Boolean, Column, String, DateTime

from .base import Base


class Emoji(Base):
    __tablename__ = "emoji"

    id = Column(String(32), nullable=False, primary_key=True)
    updatedAt = Column(DateTime)
    name = Column(String(128), nullable=False)
    host = Column(String(128))
    originalUrl = Column(String(512), nullable=False)
    uri = Column(String(512))
    column_type = Column("type", String(64))
    aliases = Column(String(128), nullable=False)
    category = Column(String(128))
    publicUrl = Column(String(512), nullable=False)
    license = Column(String(1024))
    localOnly = Column(Boolean, nullable=False)
    isSensitive = Column(Boolean, nullable=False)
    roleIdsThatCanBeUsedThisEmojiAsReaction = Column(String(128), nullable=False)
