import sys
from loguru import logger
from financial.config import config_obj


class LoggerMixin:
    @property
    def _logger(self):
        self.__logger__ = logger
        # Remove all default handlers, including stdout
        self.__logger__.remove()
        log_level = config_obj.log_level
        fmt = "{time:YYYY-MM-DDTHH:mm:ss.SSSZ!UTC} | {level: <8} | {name: <15} | {line: >4} | {message}"
        self.__logger__.add(sys.stderr, level=log_level, format=fmt)
        return self.__logger__


class Logger(LoggerMixin):
    """
    An instantiable class allowing non-protected access to the LoggerMixin methods.
    Intended for use with functions (things without classes).
    When using this class, you must supply a logger name; by convention, the dotted
    package path.
    """

    def trace(self, msg, *args, **kwargs) -> None:
        self._logger.trace(msg, *args, **kwargs)

    def debug(self, msg, *args, **kwargs) -> None:
        self._logger.debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs) -> None:
        self._logger.info(msg, *args, **kwargs)

    def success(self, msg, *args, **kwargs) -> None:
        self._logger.success(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs) -> None:
        self._logger.warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs) -> None:
        self._logger.error(msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs) -> None:
        self._logger.critical(msg, *args, **kwargs)
