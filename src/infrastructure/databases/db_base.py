from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from src.config import settings

class Base(DeclarativeBase):
    pass

engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    pool_pre_ping=True,          # tự động kiểm tra kết nối chết
    pool_recycle=3600,           # tránh MySQL server has gone away
    echo=False                   # True nếu muốn log SQL
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
