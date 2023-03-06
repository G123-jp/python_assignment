# Python Assignment

A simple API server to get financial data. Built with Flask, PostgreSQL, and Docker.


## Installation and Setup
1. Clone the project.
```bash
git clone git@github.com:pevenc12/python_assignment.git
```
2. Enter the directory.
```bash
cd python_assignment
```
3. Copy `.env` file from `.env.sample` file. Update `ALPHA_VANTAGE_API_KEY` key with your own [Alpha Vantage](https://www.alphavantage.co/) key.
```bash
cp .env.example .env
```
3. build image and run container
```bash
docker-compose up
```
4. migrate database, you need to run the following commands in order. You can find the name of api container by running `docker ps`. It should be something like `python_assignment_api_1`.
```bash
docker exec {name_of_api_container} flask db init
docker exec {name_of_api_container} flask db migrate
docker exec {name_of_api_container} flask db upgrade
```
5. Run `get_raw_data.py` to get initial data.
```bash
docker exec {name_of_api_container} python get_raw_data.py
```

## API

### 1. Get Financial Data

Example Request:
```bash
curl -X GET "http://localhost:5000/api/financial_data?start_date=2023-03-01&end_date=2023-03-04&symbol=IBM&limit=2&page=2"
```

Example Response:
```json
{
  "data": [
    {
      "symbol": "IBM",
      "open_price": "129.35",
      "close_price": "129.64",
      "date": "2023-03-03",
      "volume": 2860286
    }
  ],
  "info": {
    "error": ""
  },
  "pagination": {
    "limit": 2,
    "page": 2,
    "pages": 2,
    "total": 3
  }
}
```
Query parameters:
- `start_date`: [Optional] start date of the data, format: `YYYY-MM-DD`, default: today - 2 weeks
- `end_date`: [Optional] end date of the data, format: `YYYY-MM-DD`, default: today
- `symbol`: [Optional] symbol of the stock. Only `IBM` and `AAPL` are supported, default: `IBM`
- `limit`: [Optional] number of records per page, default: `5`
- `page`: [Optional] page number, default: `1`.

Note that page number is 1-indexed.

Possible errors:
- `start_date is not a valid date`: `start_date` is not in the format `YYYY-MM-DD`
- `end_date is not a valid date`: `end_date` is not in the format `YYYY-MM-DD`
- `start_date is after end_date`: `start_date` is after `end_date`
- `symbol is not supported`: `symbol` is not `IBM` or `AAPL`
- `limit is not a valid integer`: `limit` is not an integer
- `page is not a valid integer`: `page` is not an integer

### 2. Get Financial Statistics
Example Request:
```bash
curl -X GET "http://localhost:5000/api/financial_statistics?start_date=2023-03-01&end_date=2023-03-04&symbol=IBM"
```

Example Response:
```json
{
  "data": {
    "average_daily_close_price": "128.92",
    "average_daily_open_price": "128.88",
    "average_daily_volume": "3320406",
    "end_date": "2023-03-04",
    "start_date": "2023-03-01",
    "symbol": "IBM"
  },
  "info": {
    "error": ""
  }
}
```
Query parameters:
- `start_date`: [Required] start date of the data, format: `YYYY-MM-DD`
- `end_date`: [Required] end date of the data, format: `YYYY-MM-DD`
- `symbol`: [Required] symbol of the stock. Only `IBM` and `AAPL` are supported.

Possible errors:
- `start_date is not a valid date`: `start_date` is not in the format `YYYY-MM-DD`
- `end_date is not a valid date`: `end_date` is not in the format `YYYY-MM-DD`
- `start_date is after end_date`: `start_date` is after `end_date`
- `symbol is not supported`: `symbol` is not `IBM` or `AAPL`
- `{field} is required`: `{field}` is not provided

## Packages
- Flask: a micro web framework, used to build the API server
- Flask-SQLAlchemy: an ORM for Flask, used to interact with the database
- Flask-Migrate: a database migration tool for Flask, used to manage database migrations
- requests: a HTTP library, used to make requests to Alpha Vantage API
- psycopg2-binary: a PostgreSQL adapter for Python, used to interact with the database
- python-dotenv: a tool to load environment variables from `.env` file, used to load environment variables

## Database Migration
1. Make changes to the models in `financial/models.py`
2. Run `flask db migrate` to generate a migration file
3. Run `flask db upgrade` to apply the migration

Note that you need to run `flask db init` only oncem and we did it during installation and setup.

## To-do List before Production
1. Install a WSGI server like [Gunicorn](https://gunicorn.org/) to serve the API.
2. Install a reverse proxy like [Nginx](https://www.nginx.com/) to handle HTTPS and load balancing.
3. Use a secret management tool like [Secrets Manager](https://aws.amazon.com/secrets-manager/) and Parameter Store to manage the secret and key.
4. Set `FLASK_ENV` to production, `FLASK_DEBUG` to false.


## Future Improvements
- Add more tests, for services and apis.
- Add more logging, for debugging and monitoring.







<!-- `flask db init` only needs to be run once. `flask db migrate` and `flask db upgrade` -->