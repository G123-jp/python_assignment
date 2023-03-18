import os
from time import time
from wsgiref import simple_server

import falcon
from falcon_cors import CORS

from financial.api.financial_api import FinancialApi
from financial.api.statistics_api import StatisticsApi
from api.health import Liveness, Readiness
from api.version import Version
from common.utility import falcon_error_serializer
from common.logging import Logger
from config import configs
from config import config_obj
from config import print_configs
from common.middleware import Telemetry, RequestValidation

from financial.repository.mysql import FinancialRepository, StatisticsRepository
# DO NOT CHANGE THE FOLLOWING. It affects responder methods in API classes
# INDIVIDUAL_SUFFIX = 'one'
from financial.services.financial_service import FinancialService
from financial.services.statistics_service import StatisticsService

logger = Logger()


def initialize(env) -> falcon.API:
    """
    Initialize the falcon api
    """
    # global INDIVIDUAL_SUFFIX

    config_obj = configs[env]
    print_configs()
    
    tick = time()
    cors = CORS(allow_all_origins=True, allow_all_headers=True, allow_all_methods=True)
    api = falcon.API(middleware=[cors.middleware, RequestValidation(), Telemetry()])
    api.set_error_serializer(falcon_error_serializer)

    # Repositories
    financial_repository = FinancialRepository(config_obj.finance_database_url)
    statistics_repository = StatisticsRepository(config_obj.finance_database_url)

    # Services
    financial_service = FinancialService(financial_repository=financial_repository)
    statistics_service = StatisticsService(statistics_repository=statistics_repository)

    # Apis
    financial_api = FinancialApi(financial_service)
    statistics_api = StatisticsApi(statistics_service)

    # Routes
    api.add_route('/liveness', Liveness())
    api.add_route('/readiness', Readiness())
    api.add_route('/version', Version())

    api.add_route('/api/financial_data', financial_api)
    api.add_route('/api/statistics', statistics_api)

    logger.info(f'Finished initialization in {time() - tick:.3f} seconds')
    return api


def run() -> falcon.API:
    """
    :return: an initialized falcon.API
    """
    logger.info(f'Starting {config_obj.service_name} ...')
    try:
        env = os.getenv('SERVICE_ENVIRONMENT', 'development')
        return initialize(env)
    except Exception as e:
        logger.error(str(e))
        raise e


if __name__ == '__main__':
    httpd = simple_server.make_server('127.0.0.1', 5000, run())
    httpd.serve_forever()
