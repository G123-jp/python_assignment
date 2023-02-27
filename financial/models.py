from sqlalchemy import Column, Integer, Date, Numeric, String
from .database import Base

"""
    Define Database
"""


class FinancialData(Base):
    __tablename__ = 'financial_data'

    id = Column(Integer, primary_key=True, autoincrement=True)
    symbol = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    open_price = Column(Numeric(10, 2), nullable=True)
    close_price = Column(Numeric(10, 2), nullable=True)
    volume = Column(Integer, nullable=True)

    def date_str(self):
        return str(self.date)
