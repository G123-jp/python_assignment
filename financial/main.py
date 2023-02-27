from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from typing import Optional
from .database import Session, engine
from .schemas import GetFinancialDataResponse, FinancialData, Pagination, GetStatisticsDataResponse, \
    StatisticsData, CreateFinancialData
from . import models, crud

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return {"message": "Hello"}


@app.post("/financial_data", response_model=CreateFinancialData)
def create_financial_data(financial_data: CreateFinancialData, db: Session = Depends(get_db)):
    return crud.create_financial_data(db, financial_data)


@app.get("/api/financial_data", response_model=GetFinancialDataResponse)
async def get_financial_data(start_date: Optional[str] = None, end_date: Optional[str] = None,
                             symbol: Optional[str] = None, limit: Optional[int] = 5, page: Optional[int] = 1,
                             db: Session = Depends(get_db)):
    query_info = {"start_date": start_date, "end_date": end_date, "symbol": symbol}
    page_info = {"limit": limit, "page": page}
    items, pagination = crud.get_financial_data(db, query_info=query_info,
                                                page_info=page_info)

    return GetFinancialDataResponse(data=items, pagination=pagination, info={})


@app.get("/api/statistics")
async def get_statistics(start_date: str, end_date: str, symbol: str):
    return {
        "start_date": start_date,
        "end_date": end_date,
        "symbol": symbol
    }


@app.get("/template_financial_data")
async def get_template_financial_data() -> GetFinancialDataResponse:
    return GetFinancialDataResponse(data=[FinancialData(symbol="AAA", date="bbb", open_price="123",
                                                        close_price="222", volume="123445")],
                                    pagination=Pagination(count=1, page=1, limit=1, pages=1), info={})


@app.get("/template_statistics_data")
async def get_template_statistics_data() -> GetStatisticsDataResponse:
    return GetStatisticsDataResponse(data=StatisticsData(start_date="2023-01-01", end_date="", symbol="",
                                                         average_daily_volume=100, average_daily_close_price=1.2,
                                                         average_daily_open_price=1.1), info={})

# @app.on_event("startup")
# async def startup():
#     ...
#
# @app.on_event("shutdown")
# async def shutdown():
#     ...
#
#
# @app.post("/financial_data", response_model=schemas.FinancialData)
# def create_financial_data(financial_data: schemas.FinancialData, db: Session = Depends(get_db)):
#     return crud.create_financial_data(db=db, financial_data=financial_data)
