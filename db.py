"""
Single source of truth for the database connection.
Everything else (queries.py, load_real_data.py) imports `engine` from here
instead of creating its own raw connection -- this is what fixes the
pandas "only supports SQLAlchemy connectable" warning.
"""

import os
from sqlalchemy import create_engine 

DB_HOST = os.environ.get("DB_HOST", "db")
DB_PORT = os.environ.get("DB_PORT", "3306")
DB_USER = os.environ.get("DB_USER", "root")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "rootpass")
DB_NAME = os.environ.get("DB_NAME", "retail")

DB_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DB_URL, pool_pre_ping=True)
