from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from backend.app.data_base.database import get_async_db
from app import schemas, crud
from app.dependencies import get_current_active_user

router = APIRouter(prefix="/posts", tags=["posts"])

@router.get("/", response_model=List[schemas.PostResponse])
async def read_posts(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    published_only: bool = Query(True),
    db: AsyncSession = Depends(get_async_db)
):
    posts = await crud.get_posts(db, skip=skip, limit=limit, published_only=published_only)
    return posts

@router.post("/", response_model=schemas.PostDetailResponse)
async def create_post(
    post: schemas.PostCreate,
    db: AsyncSession = Depends(get_async_db),
    current_user: schemas.UserResponse = Depends(get_current_active_user)
):
    return await crud.create_post(db=db, post=post, user_id=current_user.id)

@router.get("/{post_id}", response_model=schemas.PostDetailResponse)
async def read_post(
    post_id: int,
    db: AsyncSession = Depends(get_async_db)
):
    db_post = await crud.get_post(db, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post

@router.put("/{post_id}", response_model=schemas.PostDetailResponse)
async def update_post(
    post_id: int,
    post_update: schemas.PostUpdate,
    db: AsyncSession = Depends(get_async_db),
    current_user: schemas.UserResponse = Depends(get_current_active_user)
):
    # Check if post exists and user owns it
    db_post = await crud.get_post(db, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    
    if db_post.owner_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    updated_post = await crud.update_post(db, post_id=post_id, post_update=post_update)
    return updated_post

@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: schemas.UserResponse = Depends(get_current_active_user)
):
    # Check if post exists and user owns it
    db_post = await crud.get_post(db, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    
    if db_post.owner_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    await crud.delete_post(db, post_id=post_id)
    return None

@router.get("/user/{user_id}", response_model=List[schemas.PostResponse])
async def read_user_posts(
    user_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    published_only: bool = Query(True),
    db: AsyncSession = Depends(get_async_db)
):
    posts = await crud.get_user_posts(db, user_id=user_id, skip=skip, limit=limit, published_only=published_only)
    return posts

@router.post("/{post_id}/publish", response_model=schemas.PostResponse)
async def publish_post(
    post_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: schemas.UserResponse = Depends(get_current_active_user)
):
    db_post = await crud.get_post(db, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    
    if db_post.owner_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    updated_post = await crud.publish_post(db, post_id=post_id)
    return updated_post