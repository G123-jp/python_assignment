from sqlalchemy.orm import Session
from sqlalchemy_pagination import paginate
from . import models, schemas


def create_financial_data(db: Session, financial_data: schemas.CreateFinancialData):
    db.add(models.FinancialData(symbol=financial_data.symbol, date=financial_data.date,
                                open_price=financial_data.open_price, close_price=financial_data.close_price,
                                volume=int(financial_data.volume)))
    db.commit()
    #db.refresh(financial_data)
    return financial_data


def get_financial_data(db: Session, query_info, page_info):
    print(f"{query_info=} {page_info=}")
    q = db.query(models.FinancialData)
    if query_info["symbol"]:
        q = q.filter_by(symbol=query_info["symbol"])
    if query_info["start_date"]:
        q = q.filter(models.FinancialData.date >= query_info["start_date"])
    if query_info["end_date"]:
        q = q.filter(models.FinancialData.date <= query_info["end_date"])
    q = paginate(q, page=page_info["page"], page_size=page_info["limit"])
    return q.items, {"count": q.total, "page": page_info["page"], "limit": page_info["limit"], "pages": q.pages}

