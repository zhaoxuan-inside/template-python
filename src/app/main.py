from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

from app.config import settings
from app.interface.api.v1.router import router as v1_router
from app.logger import configure_logging

configure_logging()

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="{{ project_description }}",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(v1_router, prefix="/api/v1")

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": settings.app_name, "version": "1.0.0"}

if settings.app_env != "development":
    FastAPIInstrumentor.instrument_app(app)
