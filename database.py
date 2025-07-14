from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


SQLALCHEMY_DATABASE_URL = "postgresql://neondb_owner:npg_s6eCHyT9Rbfq@ep-broad-star-ab24y2uk-pooler.eu-west-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
