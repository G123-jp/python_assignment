CREATE TABLE financial_data (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(255) NOT NULL,
    date DATE NOT NULL,
    open_price NUMERIC(10, 2) NOT NULL,
    close_price NUMERIC(10, 2) NOT NULL,
    volume BIGINT NOT NULL
);
