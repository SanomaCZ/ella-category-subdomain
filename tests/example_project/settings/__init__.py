# logging init - this options should be overriden somewhere
LOGGING_CONFIG_FILE = None

# load base configuration for whole app
from .base import *

# load some dev env configuration options
from .config import *

# load any settings for local development
try:
    from .local import *
except ImportError:
    pass

if LOGGING_CONFIG_FILE:
    import logging.config
    logging.config.fileConfig(LOGGING_CONFIG_FILE)
