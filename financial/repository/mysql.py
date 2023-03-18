import inflection as inflection

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy import Column, Integer, Date, String, Float, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy_pagination import paginate
from sqlalchemy import func

from common import constants
from common.logging import Logger
from datetime import datetime
from errors import DataBaseError
from repository import BaseFinancialRepository, BaseStatisticsRepository
from typing import List

from schemas import Pagination

Base = declarative_base()


class BaseModel:
    # Make every table name equal to the lower-cased name of the mapped class
    @declared_attr
    def __tablename__(cls) -> str:
        return inflection.underscore(cls.__name__)


class FinancialData(BaseModel, Base):
    symbol = Column(String, nullable=False, primary_key=True, unique=False, index=True)
    date = Column(Date, nullable=False, primary_key=True, unique=False)
    open_price = Column(Float, nullable=True)
    close_price = Column(Float, nullable=True)
    volume = Column(Integer, nullable=True)


class FinancialRepository(BaseFinancialRepository):

    def __init__(self, database_url: str) -> None:
        db_engine = create_engine(database_url)
        if not database_exists(db_engine.url):
            create_database(db_engine.url)
        Base.metadata.create_all(db_engine)
        self.session = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
        self._logger = Logger()

    def add_financial_data(self, entries: List[FinancialData]):
        session = self.session()
        try:
            # Manually convert string of datetime value to pytho datetime to support SQL operation.
            entries = [FinancialData(symbol=entry.symbol, date=datetime.strptime(entry.date, '%Y-%m-%d'),
                                     open_price=entry.open_price, close_price=entry.close_price,
                                     volume=entry.volume) for entry in entries]
            for entry in entries:
                session.merge(entry)
            session.commit()
            return entries
        except SQLAlchemyError as e:
            session.rollback()
            self._logger.error(
                f'Database error in creating Finance Data'
                f'- {str(e)}')
            raise DataBaseError(
                message=f'Database error in creating Finance Data'
                        f'- {str(e)}')
        finally:
            session.close()

    def get_financial_data(self, symbol, start_date, end_date, limit, page):
        session = self.session()
        if limit is None:
            limit = constants.DEFAULT_PAGE_LIMIT
        if page is None:
            page = constants.DEFAULT_PAGE_NUMBER

        try:
            q = session.query(FinancialData)
            if symbol:
                q = q.filter(symbol == symbol)
            if start_date:
                q = q.filter(FinancialData.date >= start_date)
            if end_date:
                q = q.filter(FinancialData.date <= end_date)
            q = paginate(q, page=int(page), page_size=int(limit))
            pagination = Pagination(count=q.total, page=int(page), limit=int(limit), pages=q.pages)
            return q.items, pagination
        except SQLAlchemyError as e:
            self._logger.error(
                f'Database error in getting Finance Data'
                f'- {str(e)}')
            raise DataBaseError(
                message=f'Database error in getting Finance Data'
                        f'- {str(e)}')
        finally:
            session.close()


class StatisticsRepository(BaseStatisticsRepository):

    def __init__(self, database_url: str) -> None:
        db_engine = create_engine(database_url)
        Base.metadata.create_all(db_engine)
        self.session = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
        self._logger = Logger()

    def get_statistics_data(self, symbol, start_date, end_date):
        session = self.session()
        try:
            q = session.query(FinancialData.symbol,
                         func.avg(FinancialData.open_price).label("average_daily_open_price"),
                         func.avg(FinancialData.close_price).label("average_daily_close_price"),
                         func.avg(FinancialData.volume).label("average_daily_volume")) \
                .filter(FinancialData.symbol == symbol,
                        FinancialData.date >= start_date,
                        FinancialData.date <= end_date) \
                .group_by(FinancialData.symbol)
            return q.first()
        except SQLAlchemyError as e:
            self._logger.error(
                f'Database error in getting Finance Data'
                f'- {str(e)}')
            raise DataBaseError(
                message=f'Database error in getting Finance Data'
                        f'- {str(e)}')
        finally:
            session.close()

