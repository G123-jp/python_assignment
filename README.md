# Financial Data API

This is a Flask-based API that provides financial data for various publicly-traded companies. The API retrieves data from a SQLite database that stores stock market data retrieved from Alpha Vantage API. The API also includes endpoints that provide statistical data based on the financial data.

## Tech Stack

The following technologies are used in this project:

- Python 3.11.2 (latest version)
- SQLite
- Peewee
- Flask
- Docker

## Maintaining the API Key

To retrieve financial data from Alpha Vantage, you need to have an API key. The API key should be kept **private** and should not be included in the codebase.

To maintain the API key:
1. Create a `.env` file in the root directory of the project.
2. Add `API_KEY=<your_api_key>` to the `.env` file, replacing `<your_api_key>` with your Alpha Vantage API key.
3. Add `.env` to your `.gitignore` file to prevent it from being committed to the repository.
4. In production, you can add the API key to the environment variables of the server running the API.

## Obtaining Financial Data

The `get_raw_data.py` script retrieves financial data from the Alpha Vantage API and stores it in the local SQLite database using the Peewee ORM. This script is not directly used by the Flask API, but can be executed locally to populate the database with fresh data.

To run the script:
1. Install the required packages using `pip install -r requirements.txt`.
2. Simply execute the following command:

```
python get_raw_data.py
```
3. Files `financial_data.db` and `cached_data.json` should now be generated in the root project directory.

## Running the API

To run this project in a local environment, you will need to have Python 3.11.2 and Docker installed on your machine.

1. Make sure `financial_data.db` is existing in the root project directory before proceeding.
2. Run the following command to start the API in Docker:

    ```
    docker-compose up --build
    ```

3. Once the API is up and running, you can access the following endpoints:

    ```
    http://localhost:5000/api/financial_data
    http://localhost:5000/api/statistics
    ```

## Why We Used SQLite, Peewee, and Flask?

- **SQLite** is a lightweight relational database management system that is easy to set up and use. It is perfect for small to medium-sized applications, and it requires no separate server process.

- **Peewee** is a simple and lightweight ORM (Object Relational Mapping) library for Python. It provides a simple and expressive API for interacting with databases, and it supports SQLite out of the box.

- **Flask** is a lightweight web application framework that is easy to learn and use. It provides a simple API for building web applications, and it integrates well with other Python libraries and Database such as Peewee and SQLite. It is a perfect choice for building small to medium-sized APIs.