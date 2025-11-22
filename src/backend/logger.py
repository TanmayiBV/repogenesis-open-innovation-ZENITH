import logging
from datetime import datetime
from pathlib import Path

# Create logs directory
LOG_DIR = Path('logs')
LOG_DIR.mkdir(exist_ok=True)

def setup_logger(name):
    '''Setup logger with file and console handlers'''
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # File handler
    log_file = LOG_DIR / f\"{name}_{datetime.now().strftime('%Y%m%d')}.log\"
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

# Create module loggers
weather_logger = setup_logger('weather_service')
crop_logger = setup_logger('crop_recommender')
market_logger = setup_logger('market_intelligence')
