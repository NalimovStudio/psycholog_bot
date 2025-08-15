
import logging
import coloredlogs
from pythonjsonlogger import jsonlogger 
from logging.config import dictConfig

def configure_logging():
    dictConfig({
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "json": {
                "()": jsonlogger.JsonFormatter,
                "format": "%(asctime)s %(levelname)s %(name)s %(message)s",
            },
            "default": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "json", 
            },
            "file": {
                "class": "logging.FileHandler",
                "formatter": "json",
                "filename": "app.json.log",  
            },
        },
        "root": {
            "level": "DEBUG",
            "handlers": ["console", "file"],
        },
    })

    coloredlogs.install(level="DEBUG", logger=logging.getLogger())  # Colored logs