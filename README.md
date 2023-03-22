# Polyglot Webserver

This repo is a fork of https://github.com/G123-jp/python_assignment with the initial implementation in Python.
However, this repo also serves as a testing ground to try out new ideas/technologies.

Currently planned additions:
- [ ] Webserver implemented in Golang
- [ ] Webserver implemented in Java 19+
- [ ] Webserver implemented in NodeJS
- [ ] Webserver implemented in Elixir
- [ ] Load balancer for webservers
- [ ] Distributed postgres database (for experimenting with distributed databases)
- [ ] Redis for caching SQL queries (for testing N-tier architectures)
- [ ] Use https protocol instead of http
- [ ] Integration tests with GitHub and Jenkins

## Notes
### Python
**grequests**. This HTTP client request library is much like the popular, ease-to-use **requests** library with the primary difference in that this allows concurrent async fetches.

**psycopg**. psycopg3. This is a popular driver for connecting with the postgres database. psycopg3 offers substantial performance improvement over psycopg2, e.g. multiple row insertion.

**psycopg_pool**. This is an add-on library to be used in conjunction with psycopg. The connection pool provides cached database connections so less time spent on connection acquisition, improving overall response time.

**fastapi**. A popular, minimalist webserver library that is similar to **flask** but with some additional features. Due to its minimalist nature, improving readability (no magic functionality) and performance.

**uvicorn**. A popular asgi library to run **fastapi**.

### Golang

### Java

### NodeJS

### Elixir

### PostgresSQL
PostgresSQL is a popular, production grade database that offers both performance and functionality.

## Store/handle AlphaVantage API key
The api key is **OTRF8D4LW9QFUFLS**.

Production. Perhaps the safer way to store/handle the key in production is to request the key from a secure, remote server and then pass the key into the script. While that means the key would be in transit over the network, at least the key would be encrypted during transit. Furthermore, the key would be stored in a centralized, hardened location (what would happen if a less secure machine containing the key were compromised?). The alternative is potentially storing the key in a environmental variable but this seems problematic since the key would not be encrypted; furthermore, it is a variable that can be accessed by other programs as well.

Development. Manually run the script providing the key: **python get_raw_data.py --symbols IBM AAPL --apikey OTRF8D4LW9QFUFLS**.

## Setup
1. Clone repo: **git clone https://github.com/ShaysRebellion/polyglot_webserver.git**
2. Install pyenv-virtualenv: https://github.com/pyenv/pyenv-virtualenv
3. Install python 3.10.0 distribution: **pyenv install 3.10.0**
4. Create python virtual environment: **pyenv virtualenv 3.10.0 your_custom_virtualenv_name_here**
5. Activate the virtual environment (there are multiple ways, see documentation: https://github.com/pyenv/pyenv-virtualenv)
6. Navigate to repo root and install package dependencies in requirements.txt file: **pip -r requirements.txt**
7. Navigate to repo root and use docker-compose to start up services: **docker-compose up**
8. Setup complete!

## Running
Sample get_raw_data.py: **python get_raw_data.py --symbols IBM AAPL --apikey OTRF8D4LW9QFUFLS**
Sample financial_data GET query: **http://localhost/api/v1/financial_data&symbol=IBM**
Sample statistics GET query: **http://localhost/api/v1/statistics?start_date=2023-03-21&end_date=2023-03-14&symbol=AAPL**
