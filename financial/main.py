""" Contains API Logic"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from fastapi import BackgroundTasks, FastAPI, Query

from financial.database import query_db
from financial.helpers import get_curr_time
from financial.statistics.model import calculate_statistics
from financial.sync import sync

app = FastAPI()


@app.get("/")
async def financial():
    return {"data": "Welcome!"}


@app.get("/api/financial_data")
async def get_financial_data(
    start_date: Optional[str] = Query(None, description="start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="end date (YYYY-MM-DD)"),
    symbol: Optional[str] = Query("IBM", description="symbol"),
    limit: Optional[int] = Query(5, description="limit of records per page"),
    page: Optional[int] = Query(1, description="page index"),
) -> Dict[str, Any]:
    """
    Endpoint to fetch financial data for symbol based on below parameter
    Args:
        start_date (Optional[str], optional): Start time. Defaults to Query(None, description="start date (YYYY-MM-DD)").
        end_date (Optional[str], optional): End Time. Defaults to Query(None, description="end date (YYYY-MM-DD)").
        symbol (Optional[str], optional): Symbol. Defaults to Query("IBM", description="symbol").
        limit (Optional[int], optional): Limit. Defaults to Query(5, description="limit of records per page").
        page (Optional[int], optional): Page. Defaults to Query(1, description="page index").

    Returns:
        Dict[str, Any]: Response containing financial data
    """
    error: str = ""
    data = None
    try:
        data = await query_db(
            start_date=start_date,
            end_date=end_date,
            symbol=symbol,
            page=page,
            limit=limit,
        )
    except Exception as err:
        error = str(err)
    total_count: int = len(data)
    num_pages: int = (total_count + limit - 1) // limit
    pagination: Dict[str, Any] = {
        "count": total_count,
        "page": page,
        "limit": limit,
        "pages": num_pages,
    }
    result = {"data": data, "pagination": pagination, "info": {"error": error}}
    return result


@app.get("/api/sync")
async def sync_finacial_data(background_tasks: BackgroundTasks) -> Dict[str, str]:
    """
    Triggers sync servoic to fetch financial data and load into database
    Returns:
        Dict[str, str]: Sync Trigger logs
    """
    background_tasks.add_task(sync)
    return {"data": f"Sync Triggered at {get_curr_time()}"}


@app.get("/api/statistics")
async def get_statistics(
    start_date: Optional[str] = Query(None, description="start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="end date (YYYY-MM-DD)"),
    symbol: Optional[str] = Query("IBM", description="symbol"),
) -> Dict[str, Any]:
    """
    API to get statistics of financial data
    Args:
        start_date (str, optional): Start Date. Defaults to Query(None, description="start date (YYYY-MM-DD)").
        end_date (str, optional): End Date. Defaults to Query(None, description="end date (YYYY-MM-DD)").
        symbol (str, optional): Symbol. Defaults to Query(None, description="symbol").

    Returns:
        Dict[str, Any]: Response containing financial data
    """
    error = ""
    output = {}
    try:
        request_data = dict(start_date=start_date, end_date=end_date, symbol=symbol)
        query_res = await query_db(**request_data)
        request_data["results"] = query_res
        output = await calculate_statistics(**request_data)
    except Exception as err:
        error = str(err)
    return {
        "data": output.dict() if type(output) != dict else output,
        "info": {"error": error},
    }
