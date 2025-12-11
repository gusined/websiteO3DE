from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from backend.app.data_base.database import get_async_db
from app import schemas, crud
from app.dependencies import get_current_active_user, get_current_admin_user

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=List[schemas.UserResponse])
async def read_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_async_db),
    current_user: schemas.UserResponse = Depends(get_current_admin_user)
):
    users = await crud.get_users(db, skip=skip, limit=limit)
    return users

@router.post("/", response_model=schemas.UserResponse)
async def create_user(
    user: schemas.UserCreate,
    db: AsyncSession = Depends(get_async_db),
    current_user: schemas.UserResponse = Depends(get_current_admin_user)
):
    return await crud.create_user(db=db, user=user)

@router.get("/{user_id}", response_model=schemas.UserDetailResponse)
async def read_user(
    user_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: schemas.UserResponse = Depends(get_current_active_user)
):
    # Users can only read their own profile unless they're admin
    if user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    db_user = await crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.put("/{user_id}", response_model=schemas.UserResponse)
async def update_user(
    user_id: int,
    user_update: schemas.UserUpdate,
    db: AsyncSession = Depends(get_async_db),
    current_user: schemas.UserResponse = Depends(get_current_active_user)
):
    # Users can only update their own profile unless they're admin
    if user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    updated_user = await crud.update_user(db, user_id=user_id, user_update=user_update)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: schemas.UserResponse = Depends(get_current_admin_user)
):
    success = await crud.delete_user(db, user_id=user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return None

@router.get("/{user_id}/profile", response_model=schemas.ProfileResponse)
async def read_user_profile(
    user_id: int,
    db: AsyncSession = Depends(get_async_db)
):
    profile = await crud.get_user_profile(db, user_id=user_id)
    if profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

@router.put("/{user_id}/profile", response_model=schemas.ProfileResponse)
async def update_user_profile(
    user_id: int,
    profile_update: schemas.ProfileUpdate,
    db: AsyncSession = Depends(get_async_db),
    current_user: schemas.UserResponse = Depends(get_current_active_user)
):
    # Users can only update their own profile
    if user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    updated_profile = await crud.update_user_profile(db, user_id=user_id, profile_update=profile_update)
    if updated_profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    return updated_profile