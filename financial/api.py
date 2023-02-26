from flask import Flask, jsonify, request
from model import FinancialData
from utilities import Helpers,StockSymbol
from datetime import datetime

app = Flask(__name__)

def validate_params(start_date, end_date, symbol):
    """
    API Request Parameters Validation
    """

    # Validate start_date and end_date format
    date_format = '%Y-%m-%d'
    try:
        if start_date:
            datetime.strptime(start_date, date_format)
        if end_date:
            datetime.strptime(start_date, date_format)
    except ValueError:
        raise ValueError('Invalid date format')

    # Validate symbol
    if symbol:
        if symbol not in [s.value for s in StockSymbol]:
            raise ValueError('Invalid symbol')


def get_data_from_db(start_date, end_date, symbol):
    """
    Code to retrieve data from database
    """

    # Build the base query
    query = FinancialData.select()
    # Apply filters to query
    if symbol:
        query = query.where(FinancialData.symbol == symbol)
    if start_date:
        query = query.where(FinancialData.date >= start_date)
    if end_date:
        query = query.where(FinancialData.date <= end_date)

    return query

def calculate_statistics(filtered_data):
    """
    Statistics Calculation for get_statistics()
    """
    total_open_price    = sum(d.open_price   for d in filtered_data)
    total_close_price   = sum(d.close_price  for d in filtered_data)
    total_volume        = sum(d.volume       for d in filtered_data)

    total_count             = filtered_data.count()
    ave_daily_open_price    = round(total_open_price / total_count,2)
    ave_daily_close_price   = round(total_close_price / total_count,2)
    ave_daily_volume        = round(total_volume / total_count,2)

    return (ave_daily_open_price, ave_daily_close_price, ave_daily_volume)

# Get financial data
@app.route('/api/financial_data', methods=['GET'])
def get_financial_data():
    """
    Retrieve financial data records from the database with optional filtering and pagination.

    Args:
        start_date (optional): A string representing the start date of the query in the format "YYYY-MM-DD".
        end_date   (optional): A string representing the end date of the query in the format "YYYY-MM-DD".
        symbol     (optional): An optional symbol from the Symbol enum to filter the results by.
        page       (optional): The page number to retrieve, defaults to 1 if not provided.
        limit      (optional): The maximum number of records to retrieve per page, defaults to 5 if not provided.

    Returns:
        dict: A dictionary containing three properties:
            - "data": An array of dictionaries representing the retrieved financial data records, with each dictionary containing the following keys:
                - "symbol"      : The stock symbol.
                - "date"        : The date of the record in the format "YYYY-MM-DD".
                - "open_price"  : The opening price for the stock on the given date.
                - "close_price" : The closing price for the stock on the given date.
                - "volume"      : The trading volume for the stock on the given date.
            - "pagination": A dictionary containing the following keys:
                - "count" : The total number of records that match the given filter criteria.
                - "page"  : The current page number.
                - "limit" : The maximum number of records returned per page.
                - "pages" : The total number of pages.
            - "info": A dictionary containing any error information if applicable
    """
    total_count = 0
    total_pages = 0

    try:
        # 1. Parse the query parameters
        start_date_str  = request.args.get('start_date', '')
        end_date_str    = request.args.get('end_date', '')
        symbol          = request.args.get('symbol', '')
        limit           = request.args.get('limit', 5, type=int)
        page            = request.args.get('page', 1, type=int)

        # 2. Validate the parameters
        validate_params(start_date_str,end_date_str,symbol)

        # Convert start_date and end_date to date objects
        start_date = Helpers.get_date(start_date_str) if start_date_str else None
        end_date = Helpers.get_date(end_date_str) if end_date_str else None

        # If start_date and end_date is not null, check if start_date > end_date
        if start_date and end_date:
            if start_date > end_date:
                raise ValueError("start_date should be an earlier date than the end_date.")

        # 3. Retrieve the relevant data
        query_result = get_data_from_db(start_date,end_date,symbol)
        if not query_result:
            raise ValueError("No data available")

        # 4. Calculate the required data

        # Get total count of records without pagination
        total_count = query_result.count()

        # Calculate total number of pages
        total_pages = total_count // limit + (total_count % limit > 0)

        if page > total_pages or page < 1:
            raise ValueError("Invalid page requested")

        # Apply pagination to query
        query_result = query_result.paginate(page, limit)

        data = []
        for row in query_result:
            data.append({
                "symbol"        : row.symbol,
                "date"          : str(row.date),
                "open_price"    : str(row.open_price),
                "close_price"   : str(row.close_price),
                "volume"        : str(row.volume)
            })

        pagination = {
            "count" : total_count,
            "page"  : page,
            "limit" : limit,
            "pages" : total_pages
        }

        # 5. Construct response object
        response = {
            'data'      : data,
            'pagination': pagination,
            'info'      : {'error': ''}
        }

        return response

    except Exception as ex:
        response = {
            "data": [],
            "pagination": {
                "count" : total_count,
                "page"  : page,
                "limit" : limit,
                "pages" : total_pages
            },
            "info": {
                "error": Helpers.get_root_cause(ex)
            }
        }
        return jsonify(response)

@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """
    Returns the calculated statistics for the specified symbol and time period.

    Args:
        start_date (Required): The start date of the time period in the format 'Y-m-d'.
        end_date   (Required): The end date of the time period in the format 'Y-m-d'.
        symbol     (Required): The symbol of the financial data to be analyzed.

    Returns:
        dict: A dictionary containing two properties:
            - "data": A dictionary with the calculated statistic results for the given period.
                - "average_daily_open_price" : The average daily open price for the period.
                - "average_daily_close_price": The average daily close price for the period.
                - "average_daily_volume"     : The average daily volume for the period.
            - "info": A dictionary that includes any error information if applies.
    """

    try:
        # 1. Parse the query parameters
        start_date_str  = request.args.get('start_date')
        end_date_str    = request.args.get('end_date')
        symbol          = request.args.get('symbol')

        # 2. Validate the parameters
        if not start_date_str or not end_date_str or not symbol:
            raise ValueError("Missing required parameter(s)")

        validate_params(start_date_str,end_date_str,symbol)

        # Convert start_date and end_date to date objects
        start_date = Helpers.get_date(start_date_str) if start_date_str else None
        end_date = Helpers.get_date(end_date_str) if end_date_str else None
        if start_date > end_date:
            raise ValueError("start_date should be an earlier date than the end_date.")

        # 3. Retrieve the relevant data
        query_result = get_data_from_db(start_date,end_date,symbol)

        # 4. Calculate the required statistics
        if query_result:
            (ave_daily_open_price, ave_daily_close_price, ave_daily_volume) = calculate_statistics(query_result)
        else:
            raise ValueError("No data available")

        # 5. Construct the response object
        data = {
            'start_date'                : start_date_str,
            'end_date'                  : end_date_str,
            'symbol'                    : symbol,
            'average_daily_open_price'  : ave_daily_open_price,
            'average_daily_close_price' : ave_daily_close_price,
            'average_daily_volume'      : ave_daily_volume
        }
        response = {'data': data, 'info': {'error': ''}}

        return jsonify(response)

    except Exception as ex:
        response = {
            "data": {},
            "info": {
                "error": Helpers.get_root_cause(ex)
            }
        }

        return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)