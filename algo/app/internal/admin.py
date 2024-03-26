'''
Date: 2024-03-21 17:45:33
LastEditors: 牛智超
LastEditTime: 2024-03-21 17:45:38
FilePath: \python\algo\app\internal\admin.py
'''
from fastapi import APIRouter

router = APIRouter()


@router.post("/")
async def update_admin():
    return {"message": "Admin getting schwifty"}