""" Contains Database Logic"""
from __future__ import annotations

import asyncio
from typing import Any, Dict, List, Optional

from requests import Session
from sqlalchemy import (
    Column,
    DateTime,
    Float,
    Integer,
    String,
    UniqueConstraint,
    create_engine,
)
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound

from financial.constants import DB
from financial.helpers import _map, db_row_to_dict

Base = declarative_base()
engine = create_engine(DB)
SessionLocal = sessionmaker(bind=engine)


def init_db():
    """
    Initializes database objects
    """
    Session = sessionmaker(bind=engine)
    session = Session()
    Base.metadata.create_all(bind=engine)
    return session


class FinancialDataTable(Base):
    """Model class for Financial Data"""

    __tablename__ = "financial_data"

    id = Column(Integer, primary_key=True)
    symbol = Column(String(50))
    date = Column(DateTime)
    open_price = Column(Float)
    close_price = Column(Float)
    volume = Column(Integer)
    __table_args__ = (UniqueConstraint("symbol", "date"),)


async def data_present(financial_data: Dict[str, str]):
    """Verify if Data is already is present in DB"""
    try:
        query = session.query(FinancialDataTable).filter_by(
            symbol=financial_data.symbol,
            date=financial_data.date,
        )
        query.one()
        return True
    except NoResultFound:
        return False


async def upsert(financial_data: Dict[str, str]):
    """Insert financial data into database"""
    if not await data_present(financial_data):
        financial_data_table = FinancialDataTable(
            symbol=financial_data.symbol,
            date=financial_data.date,
            open_price=financial_data.open_price,
            close_price=financial_data.close_price,
            volume=financial_data.volume,
        )
        session.add(financial_data_table)
        session.commit()


async def upsert_all(
    financial_data_list: List[Dict[str, Any]],
    all_at_once: Optional[bool] = False,
):
    """
    This will add all the instances in the financial_data_table_list to the session
    and commit the changes to the database at once. If the table doesn't exist,
    it will be created automatically based on the
    definition of the FinancialDataTable model.
    Args:
        financial_data (_type_): _description_
    """
    if all_at_once:
        try:
            session.add_all(
                [FinancialDataTable(**data.dict()) for data in financial_data_list],
            )
            session.commit()
        except IntegrityError as err:
            print(f"Failed to insert data: {err}")
        return

    tasks = [asyncio.ensure_future(upsert(data)) for data in financial_data_list]
    await asyncio.gather(*tasks)


async def query_db(
    start_date: Optional[str],
    end_date: Optional[str],
    symbol: Optional[str],
    limit: Optional[int] = None,
    page: Optional[int] = None,
) -> List[Dict[str, str]]:
    """
    Query Database based on filter
    Returns:
        List[Dict[str, str]]: Data fetched from Database
    """
    query = session.query(FinancialDataTable)
    if start_date:
        query = query.filter(FinancialDataTable.date >= start_date)
    if end_date:
        query = query.filter(FinancialDataTable.date <= end_date)
    if symbol:
        query = query.filter(FinancialDataTable.symbol == symbol)
    if limit and page:
        offset = (page - 1) * limit
        query = query.limit(limit).offset(offset)
    return [db_row_to_dict(row) for row in query.all()]


session: Session = init_db()
