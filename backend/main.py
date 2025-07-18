from fastapi import FastAPI
from routes.article import article_router
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from routes.splite import other_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        yield
    finally:
        pass


app = FastAPI(lifespan=lifespan)

app.include_router(article_router, prefix="/article")
app.include_router(other_router, prefix="/other")

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
