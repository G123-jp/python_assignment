from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy_pagination import paginate
from .models import FinancialData


def get_financial_data(db: Session, query_info, page_info):
    q = db.query(FinancialData)
    if query_info["symbol"]:
        q = q.filter_by(symbol=query_info["symbol"])
    if query_info["start_date"]:
        q = q.filter(FinancialData.date >= query_info["start_date"])
    if query_info["end_date"]:
        q = q.filter(FinancialData.date <= query_info["end_date"])
    q = paginate(q, page=page_info["page"], page_size=page_info["limit"])
    return q.items, {"count": q.total, "page": page_info["page"], "limit": page_info["limit"], "pages": q.pages}


def get_statistics(db: Session, query_info):
    q = db.query(FinancialData.symbol,
                 func.avg(FinancialData.open_price).label("average_daily_open_price"),
                 func.avg(FinancialData.close_price).label("average_daily_close_price"),
                 func.avg(FinancialData.volume).label("average_daily_volume")) \
        .filter(FinancialData.symbol == query_info["symbol"],
                FinancialData.date >= query_info["start_date"],
                FinancialData.date <= query_info["end_date"]) \
        .group_by(FinancialData.symbol)
    result = q.first()
    if result:
        return {
            "start_date": query_info["start_date"],
            "end_date": query_info["end_date"],
            "symbol": result.symbol,
            "average_daily_open_price": round(float(result.average_daily_open_price), 2),
            "average_daily_close_price": round(float(result.average_daily_close_price), 2),
            "average_daily_volume": int(result.average_daily_volume)
        }
    else:
        raise f"No result of statistics"
