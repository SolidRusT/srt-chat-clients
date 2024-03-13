# logging_config.py
import logging
import os
from logging.handlers import RotatingFileHandler

def configure_logger(name, debug=False, logs_path='logs', log_file_name='application.log'):
    """
    Configures and returns a logger with the specified settings.

    :param name: Name of the logger.
    :param debug: Flag to set logging level to DEBUG. INFO is default.
    :param logs_path: Path to store log files.
    :param log_file_name: Name of the log file.
    :return: Configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG if debug else logging.INFO)
    
    # Create logs directory if it doesn't exist
    if not os.path.exists(logs_path):
        os.makedirs(logs_path)
    
    # Log file path
    log_file_path = os.path.join(logs_path, log_file_name)
    
    # Create a file handler with rotation
    file_handler = RotatingFileHandler(log_file_path, maxBytes=1024*1024*5, backupCount=5)
    file_handler.setLevel(logging.DEBUG if debug else logging.INFO)
    
    # Console handler with a higher log level
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.ERROR)
    
    # Create formatters and add them to the handlers
    file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    
    file_handler.setFormatter(file_formatter)
    console_handler.setFormatter(console_formatter)
    
    # Add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

## Use logger for debugging and information logging
#logger.debug("Debugging message")
#logger.info("Information message")
#logger.error("Error message")