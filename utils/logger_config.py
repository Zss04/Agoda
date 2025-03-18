import os
import logging
import datetime
from pathlib import Path

def setup_logging(test_name=None):
    """
    Configure logging with proper formatting and file output.
    
    Args:
        test_name: Optional name of the test to include in log file name
    
    Returns:
        Logger: Configured logger instance
    """
    # Create logs directory if it doesn't exist
    log_dir = Path(os.path.expanduser("~/Downloads/agoda/Reports/Logs"))
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate log file name with timestamp and test name if provided
    timestamp = datetime.datetime.now().strftime("%Y%m%d")
    log_file_name = f"{timestamp}.log"
    
    log_file_path = log_dir / log_file_name
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    
    # Remove existing handlers to avoid duplicate logs
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Create file handler
    file_handler = logging.FileHandler(log_file_path, mode='a')
    file_handler.setLevel(logging.INFO)
    
    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # Create formatter with timestamp, level, and message
    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(name)-20s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Set formatter for handlers
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Add handlers to root logger
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
    
    # Create and return logger for the calling module
    if test_name:   
        logger = logging.getLogger(test_name)
    else:
        logger = logging.getLogger("agoda_tests")
    
    logger.info(f"Logging initialized. Log file: {log_file_path}")
    return logger

def get_logger(name=None):
    """
    Get a logger with the specified name.
    If the logger doesn't exist, it will be created.
    
    Args:
        name: Name for the logger
        
    Returns:
        Logger: Logger instance
    """
    if name:
        return logging.getLogger(name)
    else:
        return logging.getLogger("agoda_tests")