from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Any
from app.services.lru_cache import lru_cache

router = APIRouter()

class CacheItem(BaseModel):
    key: str
    value: Any

@router.put("/cache")
async def put_item(item: CacheItem):
    try:
        lru_cache.put(item.key, item.value)
        return {"message": f"Item with key '{item.key}' added to cache"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding item to cache: {str(e)}")

@router.get("/cache/{key}")
async def get_item(key: str):
    try:
        value = lru_cache.get(key)
        if value is not None:
            return {"key": key, "value": value}
        else:
            raise HTTPException(status_code=404, detail=f"Item with key '{key}' not found in cache")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving item from cache: {str(e)}")