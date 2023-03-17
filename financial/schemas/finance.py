from pydantic import BaseModel, validator
from datetime import date


class FinancialData(BaseModel):
    symbol: str
    date: str
    open_price: str
    close_price: str
    volume: str

    @validator('date', pre=True, always=True)
    def date_to_str(cls, value):
        if isinstance(value, date):
            return value.isoformat()
        return value

    @validator('open_price', 'close_price', 'volume')
    def convert_to_string(cls, v):
        return str(v)
