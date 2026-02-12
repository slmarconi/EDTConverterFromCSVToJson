"""
exporter.py
===========

Responsabile dell'esportazione del modello dati in formato JSON.

Il JSON risultante è pensato per essere consumato direttamente
dall'applicazione che visualizza le mappe delle aule.
"""

import json


def export_json(data, path="orario.json"):
    """
    Esporta il dizionario `data` in un file JSON.

    :param data: dizionario Python serializzabile in JSON
    :param path: percorso del file di output
    """
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
