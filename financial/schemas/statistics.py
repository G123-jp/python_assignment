import json
from pydantic import BaseModel


class StatisticsData(BaseModel):
    start_date: str
    end_date: str
    symbol: str
    average_daily_open_price: float
    average_daily_close_price: float
    average_daily_volume: int

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
