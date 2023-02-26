from peewee import SqliteDatabase, Model, CharField, DateField, DecimalField, IntegerField, SQL

# Connect to a SQLite database
db = SqliteDatabase('financial_data.db')

# Define a database model
class FinancialData(Model):
    symbol      = CharField()
    date        = DateField()
    open_price  = DecimalField(max_digits=10, decimal_places=2)
    close_price = DecimalField(max_digits=10, decimal_places=2)
    volume      = IntegerField()

    class Meta:
        # Database to be used for the model
        database = db
        # Name of the table to store data. By default, it is name of model class.
        db_table = "financial_data"
        # constraints
        constraints = [SQL('UNIQUE (symbol, date)')]


# Create the table if it doesn't exist
# classmethod of FinancialData Model class that performs equivalent CREATE TABLE query
FinancialData.create_table()