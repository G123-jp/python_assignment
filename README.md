# Getting Started

1. Get APIKEY from  https://www.alphavantage.co/support/#api-key
2. Rename env_template to .env, and set the value of ALPHAVANTAGE_API_KEY which got from step  1
3. After setting .env, please go to the root directory
4. using command line to build
```angular2html
docker-compose build
```
5. after building
```angular2html
docker-compose run
```
6. Let's get financial data via this url
```angular2html
127.0.0.1:8000/api/financial_data?symbol=AAPL
```
7. Let's get statistics info via this url
```angular2html
127.0.0.1:8000/api/statistics?start_date=2022-01-01&end_date=2023-12-01&symbol=AAPL
```

## Note
if you want to reset database,
you can use this command as below:
```angular2html
docker-compose down --volumes
```
