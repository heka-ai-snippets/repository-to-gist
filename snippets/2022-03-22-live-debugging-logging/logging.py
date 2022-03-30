import logging

logging.Formatter(
    "[%(asctime)s] %(funcName)s() line %(lineno)s - %(module)s - %(message)s",
    datefmt="%H:%M:%S:%ms",
)
