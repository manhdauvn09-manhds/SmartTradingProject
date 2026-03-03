# Database connection and session management
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL

# engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}) # for SQLite
# Dùng in-memory SQLite cho ví dụ này để không tạo file vật lý
engine = create_engine("sqlite:///:memory:")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
