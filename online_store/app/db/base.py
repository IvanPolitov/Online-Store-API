from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs, AsyncSession
from online_store.app.config import settings

# работа с sqlite
#SQL_DB_URL = 'sqlite:///./store.db'
'''
SQL_DB_URL = f'{DB_DRIVER}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'


синхронный движок
engine = create_engine(url=SQL_DB_URL)


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
'''

async_engine = create_async_engine(settings.get_db_url())
async_session_maker = async_sessionmaker(async_engine, expire_on_commit=True)

class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True


async def get_db() -> AsyncSession:
    async with async_session_maker() as session:
        yield session


async def create_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)