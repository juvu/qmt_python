from pydantic import BaseModel


class AccountsItem(BaseModel):
    m_dBalance: float  # 账户余额
    m_dAssureAsset: float  # 总资产
    m_dInstrumentValue: float  # 证券市值
    m_dAvailable: float  # 可用资金
    m_dPositionProfit: float  # 持仓盈亏