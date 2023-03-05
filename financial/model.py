import datetime
import decimal

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class FinancialData(db.Model):
    # The unique constraint, which speeds up queries, works as an index in PostgreSQL.
    # It is also used when upserting.
    __table_args__ = (db.UniqueConstraint("symbol", "date", name="unique_symbol_date"),)
    id: db.Mapped[int] = db.mapped_column(primary_key=True)
    symbol: db.Mapped[str] = db.mapped_column(db.String(15))
    date: db.Mapped[datetime.date]
    open_price: db.Mapped[decimal.Decimal]
    close_price: db.Mapped[decimal.Decimal]
    volume: db.Mapped[int]
    created_at: db.Mapped[datetime.datetime] = db.mapped_column(
        default=datetime.datetime.now()
    )
