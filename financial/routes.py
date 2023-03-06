from flask import jsonify, request

from financial import app
from financial.services import (
    CalculateFinancialStatisticsService,
    FinancialDataInputValidationService,
    FinancialStatisticsInputValidationService,
    GetFinancialDataService,
)


@app.route("/api/financial_data")
def get_financial_data():
    input_validation = FinancialDataInputValidationService(request.args)
    if input_validation.validation_errors:
        return jsonify(
            {
                "data": [],
                "pagination": {},
                "info": {
                    "error": input_validation.validation_errors[0],
                },
            }
        )
    get_data_service = GetFinancialDataService(input_validation.financial_data)
    get_data_service.get_financial_data()
    return jsonify(
        {
            "data": [d for d in get_data_service.financial_data_output],
            "pagination": get_data_service.pagination,
            "info": {
                "error": "",
            },
        }
    )


@app.route("/api/financial_statistics")
def calculate_financial_statistics():
    input_validation = FinancialStatisticsInputValidationService(request.args)
    if input_validation.validation_errors:
        return jsonify(
            {
                "data": [],
                "pagination": {},
                "info": {
                    "error": input_validation.validation_errors[0],
                },
            }
        )

    get_statistics_service = CalculateFinancialStatisticsService(
        input_validation.financial_statistics
    )
    get_statistics_service.calculate_financial_statistics()
    return jsonify(
        {
            "data": get_statistics_service.financial_statistics_output,
            "info": {
                "error": "",
            },
        }
    )
