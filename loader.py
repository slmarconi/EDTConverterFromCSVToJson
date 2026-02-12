"""
loader.py
=========

Responsabile del caricamento dei file TSV esportati da EDT.

I file sono TSV (tab-separated values), non CSV con virgole o punti e virgola.
Questo perché EDT, nella versione di consultazione, copia le tabelle negli
appunti usando il TAB come separatore.
"""

import csv
from errors import ParserFileNotFoundError, MissingColumnError


def load_tsv(path, required_columns=None):
    """
    Carica un file TSV e restituisce una lista di dict (una per riga).

    :param path: percorso del file TSV
    :param required_columns: lista di nomi di colonne obbligatorie
    :raises ParserFileNotFoundError: se il file non esiste o non è leggibile
    :raises MissingColumnError: se manca una colonna obbligatoria
    """
    try:
        with open(path, encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter="\t")
            rows = list(reader)
    except OSError:
        raise ParserFileNotFoundError(
            f"File non trovato o non leggibile: {path}"
        )

    if required_columns:
        # reader.fieldnames contiene l'elenco delle colonne lette dal file
        for col in required_columns:
            if col not in reader.fieldnames:
                raise MissingColumnError(
                    f"La colonna obbligatoria '{col}' non è presente in '{path}'. "
                    f"Colonne trovate: {reader.fieldnames}"
                )

    return rows
