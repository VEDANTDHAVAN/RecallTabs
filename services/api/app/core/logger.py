import logging
from pythonjsonlogger.json import JsonFormatter

def configure_logging() -> None:
    root_logger = logging.getLogger()
    
    if root_logger.handlers:
        return
    
    root_logger.setLevel(logging.INFO)

    handler = logging.StreamHandler()

    formatter = JsonFormatter(
        "%(asctime)s %(levelname)s %(name)s %(message)s"
    )

    handler.setFormatter(formatter)

    root_logger.addHandler(handler)