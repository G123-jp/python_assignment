import json
from pydantic import BaseModel


class FinancialData(BaseModel):
    symbol: str
    date: str
    open_price: float
    close_price: float
    volume: int

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


