'''
Date: 2024-03-21 16:11:02
LastEditors: 牛智超
LastEditTime: 2024-03-28 18:11:55
FilePath: \python\algo\app\routers\items.py
'''
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from typing import Union, List
from fastapi.responses import FileResponse
from dependencies import get_token_header
import qstock as qs
import os

router = APIRouter(
    prefix="",
    tags=["items"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


fake_items_db = {"plumbus": {"name": "Plumbus"}, "gun": {"name": "Portal Gun"}}


class OrdersItem(BaseModel):
    m_strInstrumentID: str  # 证券代码
    m_strInstrumentName: str  # 证券名称
    m_nOffsetFlag: int  # 买卖方向
    m_nVolumeTotalOriginal: int  # 委托数量
    m_dTradedPrice: float  # 成交价格
    m_nVolumeTraded: int  # 成交数量
    m_dTradeAmount: float  # 成交金额


class DealsItem(BaseModel):
    m_strInstrumentID: str  # 证券代码
    m_strInstrumentName: str  # 证券名称
    m_nOffsetFlag: int  # 买卖方向
    m_dPrice: float  # 成交价格
    m_nVolume: int  # 成交数量
    m_dTradeAmount: float  # 成交金额


class PositionsItem(BaseModel):
    m_strInstrumentID: str  # 证券代码
    m_strInstrumentName: str  # 证券名称
    m_nVolume: int  # 持仓数量
    m_nCanUseVolume: int  # 可用数量
    m_dOpenPrice: float  # 开仓价格
    m_dInstrumentValue: float  # 证券市值
    m_dPositionCost: float  # 持仓成本
    m_dPositionProfit: float  # 盈亏


class AccountsItem(BaseModel):
    m_dBalance: float  # 账户余额
    m_dAssureAsset: float  # 总资产
    m_dInstrumentValue: float  # 证券市值
    m_dAvailable: float  # 可用资金
    m_dPositionProfit: float  # 持仓盈亏


class SellItem(BaseModel):
    orders: List[OrdersItem]
    deals: List[DealsItem]
    positions: List[PositionsItem]
    accounts: List[AccountsItem]


@router.get("/")
def read_root():
    print('read_root')
    return {"Hello": "World"}


@router.post("/init")
async def init(request: Request):
    print('init-----------------------------------------')
    return {"data": "今日无推荐", "code": 1,
            }


@router.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@router.post("/login")
def login(request: Request):
    item_json = request.json()
    return {"Hello": "World"}


@router.post("/sell")
async def sell(request: SellItem):
    """
    分阶段卖出
    可以借鉴AI分时高低策略，
    不能猛砸，有大单就出给大单，有小单就出给小单
    """
    account = {
        "now_hold_stock_code": '',
        "now_hold_stock_name": '',
        "now_hold_stock_num": '',
    }

    orders, deals, positions, accounts = request.orders, request.deals, request.positions, request.accounts
    # 订单
    for o in orders:
        m_strInstrumentID = o.m_strInstrumentID
        m_strInstrumentName = o.m_strInstrumentName
        m_nOffsetFlag = o.m_nOffsetFlag
        m_nVolumeTotalOriginal = o.m_nVolumeTotalOriginal
        m_dTradedPrice = o.m_dTradedPrice
        m_nVolumeTraded = o.m_nVolumeTraded
        m_dTradeAmount = o.m_dTradeAmount
    for d in deals:
        m_strInstrumentID = d.m_strInstrumentID
        m_strInstrumentName = d.m_strInstrumentName
        m_nOffsetFlag = d.m_nOffsetFlag
        m_dPrice = d.m_dPrice
        m_nVolume = d.m_nVolume
        m_dTradeAmount = d.m_dTradeAmount
    for p in positions:
        m_strInstrumentID = p.m_strInstrumentID
        m_strInstrumentName = p.m_strInstrumentName
        m_nVolume = p.m_nVolume
        if m_nVolume > 0:
            account['now_hold_stock_code'] = m_strInstrumentID
            account['now_hold_stock_name'] = m_strInstrumentName
            account['now_hold_stock_num'] = m_nVolume
        m_nCanUseVolume = p.m_nCanUseVolume
        m_dOpenPrice = p.m_dOpenPrice
        m_dInstrumentValue = p.m_dInstrumentValue
        m_dPositionCost = p.m_dPositionCost
        m_dPositionProfit = p.m_dPositionProfit

    for a in accounts:
        account['m_dBalance'] = a.m_dBalance
        account['m_dAssureAsset'] = a.m_dAssureAsset
        account['m_dInstrumentValue'] = a.m_dInstrumentValue
        account['m_dAvailable'] = a.m_dAvailable
        account['m_dPositionProfit'] = a.m_dPositionProfit
    return True


@router.get("/buy")
async def buy():
    code_list = ['000001.SH', '399001.SZ']
    return code_list


@router.get("/{item_id}")
async def read_item(item_id: str):
    if item_id not in fake_items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"name": fake_items_db[item_id]["name"], "item_id": item_id}


@router.put(
    "/{item_id}",
    tags=["custom"],
    responses={403: {"description": "Operation forbidden"}},
)
async def update_item(item_id: str):
    if item_id != "plumbus":
        raise HTTPException(
            status_code=403, detail="You can only update the item: plumbus"
        )
    return {"item_id": item_id, "name": "The great Plumbus"}


def list_log_files(directory: str = os.getcwd()):
    files = []
    directory = os.path.join(directory,'algo','app','logs')
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            files.append(filename)
    return files

@router.get("/files/")
async def get_files():
    files = list_log_files()
    return {"files": files}

@router.get("/download/{filename}")
async def download_file(filename: str):
    filepath = os.path.join(os.getcwd(),"algo","app","logs", filename)
    if os.path.isfile(filepath):
        return FileResponse(filepath, media_type='application/octet-stream', filename=filename)
    else:
        raise HTTPException(status_code=404, detail="File not found")
    
@router.get("/excel/")
async def get_data_excel():
    #获取沪深A股最新行情指标
    df=qs.realtime_data()
    #查看前几行
    df.head()
    print(df.head())