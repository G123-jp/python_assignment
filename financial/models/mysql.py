import inflection as inflection

from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy import Column, Integer, Date, Numeric, String, Float, create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy_utils import database_exists, create_database
from models import BaseFinancialDataDB
from typing import List, Union
from datetime import date

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


class FinancialDataDB(BaseFinancialDataDB):

    def __init__(self, database_url: str) -> None:
        db_engine = create_engine(database_url)
        if not database_exists(db_engine.url):
            create_database(db_engine.url)
        Base.metadata.create_all(db_engine)
        session_factory = sessionmaker(bind=db_engine)
        self.session = scoped_session(session_factory)

    def add_financial_data(self, entries: List[FinancialData]):
        """Add financial data to repository"""
        entries = [FinancialData(**entry.dict()) for entry in entries]
        for entry in entries:
            self.session.merge(entry)
        self.session.commit()
        return entries

    def get_financial_data(self, symbol: Union[str, None] = None,
                           start_date: Union[date, None] = None,
                           end_date: Union[date, None] = None):
        pass
