import logging
from logging.handlers import TimedRotatingFileHandler
import os

def configurar_logger():
    if not os.path.exists('logs'):
        os.makedirs('logs')

    logger = logging.getLogger("bot_frango")
    logger.setLevel(logging.INFO)

    
    if not logger.handlers:
        
        formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s', 
                                    datefmt='%d/%m/%Y %H:%M:%S')
        
        handler = TimedRotatingFileHandler(
            "logs/bot_frango.log", 
            when="d", 
            interval=1, 
            backupCount=7, 
            encoding='utf-8'
        )
        handler.setFormatter(formatter)

      
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        logger.addHandler(handler)
        logger.addHandler(console_handler)

    return logger