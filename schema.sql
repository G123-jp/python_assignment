CREATE TABLE IF NOT EXISTS financial_data (
    symbol VARCHAR(5), /* Quick Google search suggests that the longest stock symbol is 5 characters long */
    date VARCHAR(10),  /* Since format is YYYY-MM-DD is 10 characters long */
    open_price DECIMAL,
    close_price DECIMAL,
    volume INT,
    PRIMARY KEY(symbol, date) /* Ensures row uniqueness and creates indices for optimal query performance */
)
