import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Render will provide DATABASE_URL environment variable
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://ehrms_user:6stI2ijZBVC5SiiV6DypkEM89yekXREO@dpg-d5lkmf1r0fns73ed5eb0-a:5432/ehrms")

# For Render PostgreSQL compatibility
if DATABASE_URL and DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://", 1)

engine = create_engine(
    DATABASE_URL, 
    pool_pre_ping=True,
    echo=False,
    pool_size=5,
    max_overflow=10
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
