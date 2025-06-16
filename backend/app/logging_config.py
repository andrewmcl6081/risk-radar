import logging.config

LOG_CONFIG = {
  "version": 1,
  "disable_existing_loggers": False,
  "formatters": {
    "default": {
      "format": "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
    },
  },
  "handlers": {
    "console": {
      "class": "logging.StreamHandler",
      "formatter": "default",
      "level": "INFO",
    },
  },
  "root": {
    "level": "INFO",
    "handlers": ["console"],
  },
  "loggers": {
    "transformers": {"level": "WARNING"},
    "urllib3": {"level": "WARNING"},
  },
}

def setup_logging():
  logging.config.dictConfig(LOG_CONFIG)