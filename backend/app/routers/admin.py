from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.data_base.database import get_async_db
from app import schemas, crud
from app.dependencies import get_current_admin_user

router = APIRouter(prefix="/admin", tags=["admin"])

@router.post("/users/{user_id}/activate")
async def activate_user(
    user_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: schemas.UserResponse = Depends(get_current_admin_user)
):
    success = await crud.activate_user(db, user_id=user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User activated successfully"}

@router.post("/users/{user_id}/deactivate")
async def deactivate_user(
    user_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: schemas.UserResponse = Depends(get_current_admin_user)
):
    success = await crud.deactivate_user(db, user_id=user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deactivated successfully"}

@router.post("/users/{user_id}/make-admin")
async def make_user_admin(
    user_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: schemas.UserResponse = Depends(get_current_admin_user)
):
    success = await crud.make_user_admin(db, user_id=user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User promoted to admin successfully"}

@router.get("/stats")
async def get_admin_stats(
    db: AsyncSession = Depends(get_async_db),
    current_user: schemas.UserResponse = Depends(get_current_admin_user)
):
    stats = await crud.get_admin_stats(db)
    return stats