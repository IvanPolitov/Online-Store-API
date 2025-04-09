from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
#import psycopg2

from config import DB_DRIVER, DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER


#SQL_DB_URL = 'sqlite:///./store.db'

SQL_DB_URL = f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'


engine = create_engine(
    url=SQL_DB_URL,
    #connect_args={'check_same_thread': False}
    )


SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
    )
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
