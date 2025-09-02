import enum
import uuid
from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum as EnumType,
    Integer,
    String,
)

from .base import Base


class SuspensionState(str, enum.Enum):
    NONE = "none"
    MANUALLY_SUSPENDED = "manuallySuspended"
    GONE_SUSPENDED = "goneSuspended"
    AUTO_SUSPENDED_FOR_NOT_RESPONDING = "autoSuspendedForNotResponding"


class MiInstance(Base):
    __tablename__ = "instance"

    # PrimaryColumn(id())
    # TypeORMのid()が何をするかによるが、ここではUUIDを文字列として生成することにする
    id: str = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    # このインスタンスを捕捉した日時
    # @Index()
    # @Column('timestamp with time zone', ...)
    firstRetrievedAt: datetime = Column(
        DateTime(timezone=True),
        index=True,
        default=datetime.now,
        comment="The caught date of the Instance.",
    )

    # ホスト
    # @Index({ unique: true })
    # @Column('varchar', ...)
    host: str = Column(
        String(128),
        unique=True,
        index=True,
        comment="The host of the Instance.",
    )

    # インスタンスのユーザー数
    # @Column('integer', ...)
    usersCount: int = Column(
        Integer,
        default=0,
        comment="The count of the users of the Instance.",
    )

    # インスタンスの投稿数
    # @Column('integer', ...)
    notesCount: int = Column(
        Integer,
        default=0,
        comment="The count of the notes of the Instance.",
    )

    # このインスタンスのユーザーからフォローされている、自インスタンスのユーザーの数
    # @Column('integer', ...)
    followingCount: int = Column(Integer, default=0)

    # このインスタンスのユーザーをフォローしている、自インスタンスのユーザーの数
    # @Column('integer', ...)
    followersCount: int = Column(Integer, default=0)

    # 直近のリクエスト受信日時
    # @Column('timestamp with time zone', ...)
    latestRequestReceivedAt: datetime | None = Column(
        DateTime(timezone=True),
        nullable=True,
    )

    # このインスタンスと不通かどうか
    # @Column('boolean', ...)
    isNotResponding: bool = Column(Boolean, default=False)

    # このインスタンスと不通になった日時
    # @Column('timestamp with time zone', ...)
    notRespondingSince: datetime | None = Column(
        DateTime(timezone=True),
        nullable=True,
    )

    # このインスタンスへの配信状態
    # @Index()
    # @Column('enum', ...)
    suspensionState: SuspensionState = Column(
        EnumType(
            SuspensionState, native_enum=False
        ),  # native_enum=FalseでVARCHARとして扱う
        default=SuspensionState.NONE,
        index=True,
    )

    # @Column('varchar', ...)
    softwareName: str | None = Column(
        String(64),
        nullable=True,
        comment="The software of the Instance.",
    )

    # @Column('varchar', ...)
    softwareVersion: str | None = Column(String(64), nullable=True)

    # @Column('boolean', ...)
    openRegistrations: bool | None = Column(Boolean, nullable=True)

    # @Column('varchar', ...)
    name: str | None = Column(String(256), nullable=True)

    # @Column('varchar', ...)
    description: str | None = Column(String(4096), nullable=True)

    # @Column('varchar', ...)
    maintainerName: str | None = Column(String(128), nullable=True)

    # @Column('varchar', ...)
    maintainerEmail: str | None = Column(String(256), nullable=True)

    # @Column('varchar', ...)
    iconUrl: str | None = Column(String(256), nullable=True)

    # @Column('varchar', ...)
    faviconUrl: str | None = Column(String(256), nullable=True)

    # @Column('varchar', ...)
    themeColor: str | None = Column(String(64), nullable=True)

    # @Column('timestamp with time zone', ...)
    infoUpdatedAt: datetime | None = Column(DateTime(timezone=True), nullable=True)

    # @Column('varchar', ...)
    moderationNote: str = Column(String(16384), default="")

    def __repr__(self) -> str:
        return f"<MiInstance(host='{self.host}', id='{self.id}')>"
