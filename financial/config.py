import os
import sys

from loguru import logger
from financial.common import constants
from dotenv import load_dotenv

logger.remove()
load_dotenv('.env')
fmt = "{time:YYYY-MM-DDTHH:mm:ss.SSSZ!UTC} | {level: <8} | {name: <15} | {line: >4} | {message}"
logger.add(sys.stderr, level='INFO', format=fmt)


class Config:
    log_level = 'DEBUG'
    service_name = 'ctw-python'

    # Fianancial API configs
    finance_api_client_api_key = os.getenv('FINANCE_API_CLIENT_API_KEY', None)
    finance_api_client_api_url = os.getenv('FINANCE_API_CLIENT_API_URL', None)
    finance_api_client_data_duration = int(os.getenv('FINANCE_API_CLIENT_DATA_DURATION', constants.API_CLIENT_DATA_DURATION))

    #  Database configs
    finance_database_url = os.getenv('FINANCE_DATABASE_URL', None)


class Development(Config):
    pass


class Production(Config):
    log_level = 'INFO'


# Add other SERVICE ENVIRONMENTS here (e.g., sandbox, production, uat, etc)
configs = {
    'development': Development,
    'production': Production
}

env = os.getenv('SERVICE_ENVIRONMENT', 'development')
config_obj = configs[env]


def print_configs():
    logger.info(f'log_level: {config_obj.log_level}')
    logger.info(f'service_name: {config_obj.service_name}')
    logger.info(f'service_environment: {env}')
    logger.info(f'finance_api_client_api_key: {config_obj.finance_api_client_api_key}')
    logger.info(f'finance_api_client_api_url: {config_obj.finance_api_client_api_url}')
    logger.info(f'finance_api_client_data_duration: {config_obj.finance_api_client_data_duration}')
