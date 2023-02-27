from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from typing import Optional, Union
from .database import SessionLocal, engine
from .schemas import GetFinancialDataResponse, GetStatisticsDataResponse, InfoResponse
from . import models, crud

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/api/financial_data", response_model=Union[GetFinancialDataResponse, InfoResponse])
async def get_financial_data(start_date: Optional[str] = None, end_date: Optional[str] = None,
                             symbol: Optional[str] = None, limit: Optional[int] = 5, page: Optional[int] = 1,
                             db: Session = Depends(get_db)):
    try:
        query_info = {"start_date": start_date, "end_date": end_date, "symbol": symbol}
        page_info = {"limit": limit, "page": page}
        items, pagination = crud.get_financial_data(db, query_info=query_info,
                                                    page_info=page_info)

        return GetFinancialDataResponse(data=items, pagination=pagination, info=InfoResponse(error=""))
    except Exception as e:
        return InfoResponse(error=str(e))


@app.get("/api/statistics", response_model=Union[GetStatisticsDataResponse, InfoResponse])
async def get_statistics(start_date: str, end_date: str, symbol: str, db: Session = Depends(get_db)):
    try:
        query_info = {"start_date": start_date, "end_date": end_date, "symbol": symbol}
        statistics = crud.get_statistics(db, query_info)
        return GetStatisticsDataResponse(data=statistics, info=InfoResponse(error=""))
    except Exception as e:
        return InfoResponse(error=str(e))
