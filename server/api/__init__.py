from fastapi import FastAPI
from .routes import init_routes
from .database import init_db
from contextlib import asynccontextmanager
from starlette.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize application services."""
    await init_db()
    yield


def create_app() -> FastAPI:
    """Creating FastAPI application."""
    app = FastAPI(title="Farm Stack Template", lifespan=lifespan)

    # Cors
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    init_routes(app)
    return app


app = create_app()
