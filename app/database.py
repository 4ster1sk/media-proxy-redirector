from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import SQLALCHEMY_DATABASE_URL

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, pool_size=10, max_overflow=20, pool_timeout=5
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
