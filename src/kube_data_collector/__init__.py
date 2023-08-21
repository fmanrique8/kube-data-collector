"""kube-data-collector
"""

__version__ = "0.1"

import logging
import coloredlogs

# Create a logger for the forex app
logger = logging.getLogger("forex")

# Basic logging format
fmt = "%(asctime)s - %(levelname)s - %(message)s"

# Set log level
logger.setLevel(logging.DEBUG)

# Set up colored logging
coloredlogs.install(level="DEBUG", logger=logger, fmt=fmt)
