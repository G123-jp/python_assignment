import math
import pytest
from api import DEFAULT_LIMIT, DEFAULT_PAGE, WarningCode, ErrorCode, process_start_end_date, process_limit_and_page

@pytest.mark.parametrize("input,expected", [
    (("2023-05-14", "2023-05-04", {}), ("2023-05-04", "2023-05-14", { "warning": [WarningCode.SWAP_START_END_DATE], "error": [] })),
    (("2023-05-04", "2023-05-14", {}), ("2023-05-04", "2023-05-14", { "warning": [], "error": [] })),
])
def test_process_date(input, expected):
    assert process_start_end_date(input[0], input[1], input[2]) == expected

@pytest.mark.parametrize("input,expected", [
    ((-1, -1, -1, {}), (0, DEFAULT_LIMIT, DEFAULT_PAGE, 1, { "warning": [WarningCode.TRUNCATE_LIMIT, WarningCode.TRUNCATE_PAGE], "error": [] })),
    ((10, 20, 20, {}), (10, DEFAULT_LIMIT, DEFAULT_PAGE, math.ceil(10 / DEFAULT_LIMIT), { "warning": [WarningCode.TRUNCATE_LIMIT, WarningCode.TRUNCATE_PAGE], "error": [] })),
    ((10, 3, 10, {}), (10, 3, DEFAULT_PAGE, 4, { "warning": [WarningCode.TRUNCATE_PAGE], "error": [] })),
    ((10, 2, 5, {}), (10, 2, 5, 5, { "warning": [], "error": [] }))
])
def test_process_limit_page(input, expected):
    assert process_limit_and_page(input[0], input[1], input[2], input[3]) == expected
