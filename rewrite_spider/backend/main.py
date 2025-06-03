from fastapi import FastAPI
from routes.article import article_router
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from services.service_sqlite import service_sqlite

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await service_sqlite.create_table()
        yield
    finally:
        await service_sqlite.close()

app = FastAPI(lifespan=lifespan)

app.include_router(article_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8888)