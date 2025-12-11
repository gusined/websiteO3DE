from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import os

from backend.app.config import settings
from backend.app.data_base.database import create_tables
from app.routers import auth, users, posts, admin
from backend.app.middlware.security import SecurityMiddleware
from app.core.logging import setup_logging
from backend.app.core.logging import get_password_hash, validate_password_strength

setup_logging()

limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title=settings.APP_NAME,
    description=settings.DESCRIPTION,
    version=settings.VERSION,
    docs_url="/docs" if settings.DEBUG else None,  
    redoc_url="/redoc" if settings.DEBUG else None,
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(SecurityMiddleware)

if not settings.DEBUG:
    app.add_middleware(HTTPSRedirectMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1/auth")
app.include_router(users.router, prefix="/api/v1")
app.include_router(posts.router, prefix="/api/v1")
app.include_router(admin.router, prefix="/api/v1")

@app.on_event("startup")
async def startup_event():
    await create_tables()
    print("✅ Application started with security features")

@app.get("/")
@limiter.limit("100/minute")
async def root(request: Request):
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": settings.VERSION,
        "security": "enabled"
    }

@app.get("/health")
@limiter.limit("30/minute")
async def health_check(request: Request):
    return {
        "status": "healthy", 
        "timestamp": "2024-01-01T00:00:00Z",
        "security": "active"
    }

@app.post("/api/v1/security/password-strength")
async def check_password_strength(password: str):
    """Проверка сложности пароля"""
    return validate_password_strength(password)

if __name__ == "__main__":
    import uvicorn
    
    ssl_config = {}
    if not settings.DEBUG:
        ssl_config = {
            "ssl_keyfile": "/path/to/private.key",
            "ssl_certfile": "/path/to/certificate.crt"
        }
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        **ssl_config
    )