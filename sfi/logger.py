import logging
from sfi.config import ConfigBase


def logger():
    logging.basicConfig(level=ConfigBase.log_level, format='%(asctime)s %(name)s %(levelname)s:%(message)s')
    return logging.getLogger("## sfi ##")
