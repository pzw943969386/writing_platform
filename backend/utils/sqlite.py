import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, delete, update
from backend.models.article_model import Article, Base


class SqliteService:
    def __init__(self, db_path):
        db_dir = os.path.dirname(db_path)
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)

        self.engine = create_async_engine(f"sqlite+aiosqlite:///{db_path}")
        self.async_session = sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=True
        )

    async def create_table(self):
        try:
            async with self.engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
        except Exception as e:
            pass

    async def get_all_article_data(self):
        async with self.async_session() as session:
            result = await session.execute(select(Article))
            return result.scalars().all()

    async def get_article_by_id(self, id):
        async with self.async_session() as session:
            result = await session.execute(select(Article).where(Article.id == id))
            return result.scalar_one_or_none()

    async def update_article_content(self, article_id, content):
        async with self.async_session() as session:
            await session.execute(
                update(Article).where(Article.id == article_id).values(content=content)
            )
            await session.commit()

    async def delete_table_by_id(self, id):
        async with self.async_session() as session:
            await session.execute(delete(Article).where(Article.id == id))
            await session.commit()

    async def delete_table_all_data(self):
        async with self.async_session() as session:
            await session.execute(delete(Article))
            await session.commit()

    async def add_article_data(self, **kwargs):
        async with self.async_session() as session:
            article = Article(**kwargs)
            session.add(article)
            await session.commit()
            await session.refresh(article)


sqlite_service = SqliteService(db_path="backend/db/data.db")
