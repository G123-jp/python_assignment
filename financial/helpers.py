"""
Useful Miscellaneous Utilities which can be reused at multiple places in a Python Code
"""

from __future__ import annotations

import datetime
from typing import Any, Callable, Dict, List

from dateutil import parser


def _map(func: Callable, data: List[Any]) -> List[Any]:
    """Wrapper over python's map fucntion"""
    return [*map(func, data)]


def is_valid_datetime(string):
    try:
        if parser.parse(string):
            return True
    except:
        return False


def sanetize_dict(data):
    symbols = [".", " "]
    output = {}
    for key, val in data.items():
        if isinstance(val, dict):
            val = sanetize_dict(val)
        if is_valid_datetime(key):
            output[key] = val
            continue
        for char in [*range(0, 9)] + symbols:
            key = key.replace(str(char), "")
        output[key] = val
    return output


def get_curr_time():
    now = datetime.datetime.now()
    current_date_time = now.strftime("%Y-%m-%d %H:%M:%S")
    return current_date_time


def db_row_to_dict(row):
    d = {}
    for column in row.__table__.columns:
        d[column.name] = str(getattr(row, column.name))
    return d
