import logging
import sys
from pythonjsonlogger.json import JsonFormatter

def configure_logging(log_level="INFO"):
    log_handler = logging.StreamHandler(sys.stdout)

    formatter = JsonFormatter()
    log_handler.setFormatter(formatter)

    logging.basicConfig(
        level=log_level,
        handlers=[log_handler]
    )

    logging.getLogger("flask.app").setLevel(log_level)
    logging.getLogger("werkzeug").setLevel(log_level)

    logging.info("Structured logging is now configured.")