from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_PATH = Path("data/freelancer_tracker.db")
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)