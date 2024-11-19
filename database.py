from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# input database name and password
DATABASE_URL = "postgresql://postgres:matthew@localhost/postgres"

# Create engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
