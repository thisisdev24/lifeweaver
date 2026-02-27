from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

import os

BASE_DIR = "/workspaces/lifeweaver/data/ingest"
os.makedirs(BASE_DIR, exist_ok=True)

DATABASE_URL = f"sqlite:///{BASE_DIR}/files.db"
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

Base = declarative_base()