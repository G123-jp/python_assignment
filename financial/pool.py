from psycopg_pool import ConnectionPool

# Improve performance by caching database connections instead of creating new connections for every database operation
# Note that we can use AsyncConnectionPool if (and only if) the webserver's performance can be improved by concurrent async operations
connectionPool = ConnectionPool('host=postgres port=5432 user=shaysrebellion password=webserverdb dbname=stocks') 
