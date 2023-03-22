from datetime import datetime
from enum import Enum
import math
from fastapi import FastAPI
from psycopg.rows import dict_row
from pool import connectionPool

appv1 = FastAPI()

DEFAULT_LIMIT = 5
DEFAULT_PAGE = 1

# Warning and error codes are more concise way than strings, reduces response data size (similar to 3XX, 4XX, 5XX responses),
# and enables debugging without logging (reduced disk writes), all of which should help improve performance should the
# size of the application scale

class WarningCode(Enum):
    SWAP_START_END_DATE = 0
    TRUNCATE_LIMIT = 1
    TRUNCATE_PAGE = 2

class ErrorCode(Enum):
    START_DATE_BAD_FORMAT = 0
    END_DATE_BAD_FORMAT = 1


def process_start_end_date(startDate, endDate, info):
    errorMessages = info.get('error', [])
    warningMessages = info.get('warning', [])

    try:
        if startDate: datetime.strptime(startDate, '%Y-%m-%d')
    except:
        errorMessages.append(ErrorCode.START_DATE_BAD_FORMAT)

    try:
        if endDate: datetime.strptime(endDate, '%Y-%m-%d')
    except:
        errorMessages.append(ErrorCode.END_DATE_BAD_FORMAT)
    
    info.setdefault('error', errorMessages)

    if len(info.get('error')) > 0:
        raise Exception()

    if startDate and endDate and endDate < startDate:
        temp = startDate
        startDate = endDate
        endDate = temp        
        
        warningMessages.append(WarningCode.SWAP_START_END_DATE)

    info.setdefault('warning', warningMessages)

    return startDate, endDate, info

def process_limit_and_page(count, limit, page, info):
    errorMessages = info.get('error', [])
    warningMessages = info.get('warning', [])

    count = max(0, count)
    if limit < 1 or limit > count:
        limit = DEFAULT_LIMIT
        warningMessages.append(WarningCode.TRUNCATE_LIMIT)

    numPages = max(1, math.ceil(count / limit))
    if page < 1 or page > numPages:
        page = DEFAULT_PAGE
        warningMessages.append(WarningCode.TRUNCATE_PAGE)

    info.setdefault('error', errorMessages)
    info.setdefault('warning', warningMessages)

    return count, limit, page, numPages, info


@appv1.get('/financial_data')
def financial_data(start_date: str = '', end_date: str = '', symbol: str = '', limit: int = DEFAULT_LIMIT, page: int = DEFAULT_PAGE):
    data = []
    pagination = {}
    info = {}

    try:
        startDate, endDate, info = process_start_end_date(start_date, end_date, info)
    except:
        return {
            'data': data,
            'pagination': pagination,
            'info': info,
        }

    # Unfortunately, we need to fetch all rows that fit the start date, end date, and symbol instead of a subset of
    # said data based on limit and page (i.e. LIMIT and OFFSET) since we need to count all rows for the metadata.
    # However, because we can use indexing (using WHERE clause) and because the size of the data is expected to be
    # small (< 1000 rows), there should not be any noticeable performance issues at this scale.
    
    # However, should the application scale, then some solution are:
    # 1) configure more parallel workers for postgres (essentially vertical scaling)
    # 2) caching (but then we have to solve the stale cache issue)
    queryTemplate = ' \
        SELECT * FROM financial_data \
        WHERE {endDateCondition} {startDateCondition} {symbolCondition} \
        ORDER BY date ASC \
    '.format(
        endDateCondition = "date <= '{endDate}'".format(endDate = endDate or datetime.now().strftime('%Y-%m-%d')),
        startDateCondition = "AND date >= '{startDate}'".format(startDate = startDate) if startDate else "",
        symbolCondition = "AND symbol = '{symbol}'".format(symbol = symbol) if symbol else "",
    )

    with connectionPool.connection() as conn:
        with conn.cursor(row_factory = dict_row) as cur:
            cur.execute(queryTemplate)
            data = cur.fetchall()

    count, limit, page, numPages, info = process_limit_and_page(len(data), limit, page, info)
    pagination.setdefault('count', count)
    pagination.setdefault('limit', limit)
    pagination.setdefault('page', page)
    pagination.setdefault('pages', numPages)

    return {
        'data': data[((page - 1) * limit): ((page - 1) * limit + limit)],
        'pagination': pagination,
        'info': info,
    }

@appv1.get('/statistics')
def statistics(start_date: str, end_date: str, symbol: str):
    data = {}
    info = {}

    try:
        startDate, endDate, info = process_start_end_date(start_date, end_date, info)
    except:
        return {
            'data': data,
            'info': info,
        }

    queryTemplate = " \
        SELECT AVG(open_price), AVG(close_price), AVG(volume) FROM financial_data \
        WHERE date >= '{startDate}' AND date <= '{endDate}' AND symbol = '{symbol}' \
    ".format(startDate = startDate, endDate = endDate, symbol = symbol)

    with connectionPool.connection() as conn:
        result = conn.execute(queryTemplate).fetchone()
    
    data.setdefault('start_date', startDate)
    data.setdefault('end_date', endDate)
    data.setdefault('symbol', symbol)
    data.setdefault('average_daily_open_price', round(result[0], 2))
    data.setdefault('average_daily_close_price', round(result[1], 2))
    data.setdefault('average_daily_volume', round(result[2]))

    return {
        'data': data,
        'info': info,
    }
