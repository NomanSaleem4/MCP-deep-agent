import logging
import os
from logging.handlers import TimedRotatingFileHandler
from pythonjsonlogger.json import JsonFormatter


def setup_logging(level=logging.INFO, log_file="logs/app.log"):
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    plain_fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    json_fmt = JsonFormatter("%(asctime)s %(levelname)s %(name)s %(message)s")

    # terminal — plain text (human readable)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(plain_fmt)

    # file — JSON (machine readable), rotates at midnight, keeps 7 days
    file_handler = TimedRotatingFileHandler(log_file, when="midnight", backupCount=7)
    file_handler.setFormatter(json_fmt)

    root = logging.getLogger()
    root.setLevel(level)
    root.addHandler(stream_handler)
    root.addHandler(file_handler)

    # silence noisy libraries
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("mcp").setLevel(logging.WARNING)
    # watchfiles logs every fs event it sees (unfiltered by --reload-exclude);
    # since it writes into log_file, which lives inside the watched tree, it
    # would otherwise re-trigger itself in an infinite loop under --reload
    logging.getLogger("watchfiles").setLevel(logging.WARNING)
