from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, Text, select
from models.aritcle_model import Article, Base


class ServiceSqlite:
    def __init__(self, db_path):
        self.engine = create_async_engine(f"sqlite+aiosqlite:///{db_path}", echo=True)
        self.async_session = sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=True
        )

    async def create_table(self):
        try:
            async with self.engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
        except Exception as e:
            pass

    async def save_article_by_current_date(self, current_date, title, content, url):
        async with self.async_session() as session:
            article = Article(
                current_date=current_date, title=title, content=content, url=url
            )
            session.add(article)
            await session.commit()

    async def update_article_by_url(self, url, content):
        async with self.async_session() as session:
            stmt = select(Article).where(Article.url == url)
            result = await session.execute(stmt)
            article = result.scalar_one_or_none()
            if article:
                article.content = content
                await session.commit()
            await session.commit()

    async def get_article_list(self, current_date):
        async with self.async_session() as session:
            stmt = select(Article).where(Article.current_date == current_date)
            result = await session.execute(stmt)
            articles = result.scalars().all()
            return [
                {
                    "id": a.id,
                    "current_date": a.current_date,
                    "title": a.title,
                    "content": a.content,
                    "url": a.url,
                }
                for a in articles
            ]

    async def get_article_content_by_url(self, title_url):
        async with self.async_session() as session:
            stmt = select(Article).where(Article.url == title_url)
            result = await session.execute(stmt)
            article = result.scalar_one_or_none()
            return article.content if article else None

    async def close(self):
        await self.engine.dispose()


service_sqlite = ServiceSqlite(db_path="db/data.sqlite")
