""" Contains logic to trigger Sync"""
from __future__ import annotations

import asyncio
from typing import List

from financial.sync import sync
from financial.transform.transform_financial_data import FinancialData

if __name__ == "__main__":
    financial_data: List[FinancialData] = asyncio.run(sync())
    print(financial_data)
