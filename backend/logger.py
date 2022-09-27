import logging

debug_logger = logging.getLogger('root')
error_logger = logging.getLogger('error_logger')


def debug(msg):
    debug_logger.debug(msg)


def error(msg):
    error_logger.error(msg)