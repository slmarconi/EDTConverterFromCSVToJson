"""
logger.py
=========

Configura un logger semplice e leggibile, pensato per essere usato
da script eseguiti da persone non tecniche.

I messaggi sono del tipo:
[INFO] ...
[ERROR] ...
"""

import logging


def get_logger():
    logger = logging.getLogger("edt_parser")
    logger.setLevel(logging.INFO)

    # Evita di aggiungere più handler se get_logger() viene chiamato più volte
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter("[%(levelname)s] %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger
