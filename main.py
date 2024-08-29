from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware

from database import drop_db
from routing import routers

@asynccontextmanager
async def lifespan(app: FastAPI):
    # await drop_db()
    yield
    pass


app = FastAPI(
    openapi_url="/docs/openapi.json",
    docs_url="/docs",
    lifespan=lifespan
)
app.add_middleware(GZipMiddleware, minimum_size=500)

for router in routers:
    app.include_router(router)
