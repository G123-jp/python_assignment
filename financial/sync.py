""" Contains logic to Sync Finanical data into Database"""
from __future__ import annotations

from typing import Dict, List

from financial.database import upsert_all
from financial.extract.extract import RawStock, extract_stock
from financial.transform.transform_financial_data import (
    FinancialData,
    transform,
)


async def sync() -> List[FinancialData]:
    """Extract/Transforms/Load the finaical data into DB"""
    extracted_data: Dict[str, RawStock] = await extract_stock()
    transformed_data: List[FinancialData] = transform(extracted_data)
    await upsert_all(transformed_data, all_at_once=False)
    return transformed_data
