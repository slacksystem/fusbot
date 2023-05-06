import logging
import logging.config

# Define the configuration dictionary
LOGGING_CONF = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "rich.logging.RichHandler",
            "level": "DEBUG",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "DEBUG",
            "filename": "bot.log"
        },
    },
    "loggers": {
        "": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
        },
    },
}


def configure_logging():
    # load the configuration
    logging.config.dictConfig(LOGGING_CONF)
