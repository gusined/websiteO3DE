from fastapi import Depends, HTTPException, status, UploadFile, File
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError, jwt
from typing import Optional

from backend.app.data_base.database import get_async_db
from app.config import settings
from app import crud, models

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_async_db)
) -> models.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(
            credentials.credentials, 
            settings.SECRET_KEY, 
            algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = await crud.get_user_by_username(db, username=username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(
    current_user: models.User = Depends(get_current_user)
) -> models.User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

async def get_current_admin_user(
    current_user: models.User = Depends(get_current_active_user)
) -> models.User:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user

# File validation
async def validate_file(
    file: UploadFile = File(...),
    max_size: int = settings.MAX_FILE_SIZE,
    allowed_types: list = None
):
    if allowed_types is None:
        allowed_types = ["image/jpeg", "image/png", "image/gif", "application/pdf"]
    
    # Check file size
    if hasattr(file, 'size') and file.size > max_size:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File too large. Max size: {max_size} bytes"
        )
    
    # Check file type
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"File type not allowed. Allowed types: {', '.join(allowed_types)}"
        )
    
    return file