# CTW Assignment

## Tech Stack

The tech stack used in this project includes:

- Python 3.7
- SQLAlchemy
- Falcon
- Docker
- SQLite
- Greenlet

Here are the steps to set up the CTW Assignment service locally:

### Step 1: Clone the Repository
Clone the CTW Assignment repository to your local machine.
```shell
git clone https://github.com/tiroshanm/ctw-python.git
```
### Step 2: Get API Key
Go to https://www.alphavantage.co/support/#api-key and get an API key.

### Step 3: Set API Key
Set the value of `FINANCE_API_CLIENT_API_KEY` in the ".env" file with the API key you obtained in Step 2.

### Step 4: Setup financial_data locally
Run the `get_raw_data.py` to download the financial data and populate data in SQLite database.
```shell
python get_raw_data.py
```

### Step 5: Build the Docker Image
Build the Docker image by running the following command in the project directory:
```shell
docker-compose build
```

### Step 6: Start the Server
Start the server by running the following command:
```shell
docker-compose up
```

### Step 7: Retrieve Stock Data
To get financial data or statistics data, use the following requests respectively:

#### Financial Data Request:
```http request
127.0.0.1:8000/api/financial_data?start_date=2023-01-01&end_date=2023-01-14&symbol=IBM&limit=3&page=2
```

#### Statistics Data Request:
```http request
127.0.0.1:8000/api/statistics?start_date=2023-01-01&end_date=2023-01-31&symbol=IBM
```

### API Key Management
To retrieve financial data from AlphaVantage, an API key is required. Do not store the API key in your code or version control, as it can be a security risk.

In both local development and production environments, set the API key as an environment variable. This can be done in a .env file in your environment.

To retrieve the API key in your code, use the os.getenv() method to read the value of the environment variable.
