from sqlalchemy import (
    Column,
    String,
    Integer,
    Boolean,
    DateTime,
    ForeignKey,
    JSON,
    ARRAY,
)

from .base import Base


class User(Base):
    __tablename__ = "user"

    id = Column(String, primary_key=True)

    updatedAt = Column(
        DateTime(timezone=True), nullable=True, comment="The updated date of the User."
    )
    lastFetchedAt = Column(DateTime(timezone=True), nullable=True)
    lastActiveDate = Column(DateTime(timezone=True), nullable=True)

    hideOnlineStatus = Column(Boolean, default=False)

    username = Column(String(128), nullable=False, comment="The username of the User.")
    usernameLower = Column(
        String(128), nullable=False, comment="The username (lowercased) of the User."
    )

    name = Column(String(128), nullable=True, comment="The name of the User.")

    followersCount = Column(Integer, default=0, comment="The count of followers.")
    followingCount = Column(Integer, default=0, comment="The count of following.")

    movedToUri = Column(
        String(512), nullable=True, comment="The URI of the new account of the User"
    )
    movedAt = Column(
        DateTime(timezone=True),
        nullable=True,
        comment="When the user moved to another account",
    )
    alsoKnownAs = Column(
        ARRAY(String), nullable=True, comment="URIs the user is known as too"
    )

    notesCount = Column(Integer, default=0, comment="The count of notes.")

    avatarId = Column(
        String,
        ForeignKey("drive_file.id", ondelete="SET NULL"),
        nullable=True,
        comment="The ID of avatar DriveFile.",
    )

    bannerId = Column(
        String,
        ForeignKey("drive_file.id", ondelete="SET NULL"),
        nullable=True,
        comment="The ID of banner DriveFile.",
    )

    avatarUrl = Column(String(1024), nullable=True)
    bannerUrl = Column(String(512), nullable=True)
    avatarBlurhash = Column(String(128), nullable=True)
    bannerBlurhash = Column(String(128), nullable=True)

    avatarDecorations = Column(JSON, default=list)

    tags = Column(ARRAY(String(128)), default=list)

    score = Column(Integer, default=0)

    isSuspended = Column(
        Boolean, default=False, comment="Whether the User is suspended."
    )
    isLocked = Column(Boolean, default=False, comment="Whether the User is locked.")
    isBot = Column(Boolean, default=False, comment="Whether the User is a bot.")
    isCat = Column(Boolean, default=False, comment="Whether the User is a cat.")
    isExplorable = Column(
        Boolean, default=True, comment="Whether the User is explorable."
    )
    isHibernated = Column(Boolean, default=False)
    requireSigninToViewContents = Column(Boolean, default=False)

    makeNotesFollowersOnlyBefore = Column(Integer, nullable=True)
    makeNotesHiddenBefore = Column(Integer, nullable=True)

    isDeleted = Column(Boolean, default=False, comment="Whether the User is deleted.")

    emojis = Column(ARRAY(String(128)), default=list)

    chatScope = Column(
        String(128), default="mutual"
    )  # everyone / followers / following / mutual / none

    host = Column(
        String(128), nullable=True, comment="The host of the User. Null if local."
    )
    inbox = Column(String(512), nullable=True)
    sharedInbox = Column(String(512), nullable=True)
    outbox = Column(String(512), nullable=True)
    featured = Column(String(512), nullable=True)

    uri = Column(String(512), nullable=True)
    followersUri = Column(String(512), nullable=True)

    token = Column(
        String(16),
        nullable=True,
        unique=True,
        comment="The native access token of the User.",
    )
