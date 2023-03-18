import json
from pydantic import BaseModel
from typing import List

from financial.schemas.finance import FinancialData
from financial.schemas.statistics import StatisticsData


class Pagination(BaseModel):
    count: int
    page: int
    limit: int
    pages: int

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


class InfoResponse(BaseModel):
    error: str = ""

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


class GetFinancialDataResponse(BaseModel):
    data: List[FinancialData]
    pagination: Pagination
    info: InfoResponse

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


class GetStatisticsDataResponse(BaseModel):
    data: StatisticsData
    info: InfoResponse

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
