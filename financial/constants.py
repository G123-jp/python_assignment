""" Projects constants """
from __future__ import annotations

import os
from enum import Enum

SYMBOLS = ["IBM", "AAPL"]
API_KEY = os.environ.get("FINANCIAL_KEY", "demo")
DB = "sqlite:///financial_data.db"


class TimeFunctions(str, Enum):
    TIME_SERIES_WEEKLY = "TIME_SERIES_WEEKLY"


TimeFunctionsMap = {TimeFunctions.TIME_SERIES_WEEKLY: "WeeklyTimeSeries"}
