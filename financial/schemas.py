from pydantic import BaseModel
from typing import List, Any


class FinancialData(BaseModel):
    symbol: str
    date: str
    open_price: str
    close_price: str
    volume: str

    class Config:
        orm_mode = True


class Pagination(BaseModel):
    count: int
    page: int
    limit: int
    pages: int

    class Config:
        orm_mode = True


class GetFinancialDataResponse(BaseModel):
    data: List[FinancialData]
    pagination: Pagination
    info: Any

    class Config:
        orm_mode = True


class StatisticsData(BaseModel):
    start_date: str
    end_date: str
    symbol: str
    average_daily_open_price: float
    average_daily_close_price: float
    average_daily_volume: int

    class Config:
        orm_mode = True


class GetStatisticsDataResponse(BaseModel):
    data: StatisticsData
    info: Any

    class Config:
        orm_mode = True
