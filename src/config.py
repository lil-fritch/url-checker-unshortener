import sys
from loguru import logger

def setup_logger():
    logger.remove()
    
    logger.add(sys.stderr, level="INFO")
    
    logger.add(
        "logs/app_log_{time}.log",
        rotation="5 minutes",
        retention="20 minutes",
        level="DEBUG",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
    )
    
    return logger