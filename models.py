from pydantic import BaseModel


class NicehashReport(BaseModel):
    datetime: str
    local_datetime: str
    purpose: str
    amount_btc: float
    exchange_rate: float
    amount_jpy: float


class FreeeReport(BaseModel):
    収支区分: str
    発生日: str
    勘定科目: str
    税区分: str
    金額: int
    備考: str
    品名: str
