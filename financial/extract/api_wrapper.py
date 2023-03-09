from __future__ import annotations

import asyncio
from typing import Any, Dict, List, Optional

import requests

from financial.constants import API_KEY, TimeFunctions

scheme: str = "https://"
domain: str = "www.alphavantage.co"


async def get_core_stocks(
    symbols: List[str],
    time_function: Optional[TimeFunctions] = TimeFunctions.TIME_SERIES_WEEKLY,
) -> Dict[str, Any]:
    """
    Fetch Cores Stocks data
    Args:
        symbol (str): Symbol
        time_function (Optional[TimeFunctions], optional): Defaults to TimeFunctions.TIME_SERIES_WEEKLY.
    Returns:
        dict: Finanical Data
    """
    sym_url_map: List[str] = {
        symbol: f"{scheme}{domain}/query?function={time_function}&symbol={symbol}&apikey={API_KEY}"
        for symbol in symbols
    }

    tasks = [asyncio.ensure_future(call_get_api(url)) for _, url in sym_url_map.items()]
    results = await asyncio.gather(*tasks)
    return {symbol: data for symbol, data in zip(symbols, results)}


async def call_get_api(url: str) -> Dict[str, Any]:
    """Calls Get API"""
    response = requests.get(url, verify=False)
    response.raise_for_status()
    return response.json()
