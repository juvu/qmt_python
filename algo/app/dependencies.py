'''
Date: 2024-03-21 16:10:44
LastEditors: 牛智超
LastEditTime: 2024-03-21 16:10:50
FilePath: \python\algo\app\dependencies.py
'''
from fastapi import Header, HTTPException


async def get_token_header(x_token: str = Header()):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def get_query_token(token: str):
    if token != "jessica":
        raise HTTPException(status_code=400, detail="No Jessica token provided")