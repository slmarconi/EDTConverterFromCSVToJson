"""
errors.py
=========

Definisce eccezioni specifiche per il parser EDT, in modo da poter
mostrare messaggi di errore chiari e comprensibili anche a chi non
conosce i dettagli tecnici o EDT stesso.
"""


class ParserError(Exception):
    """Errore generico del parser EDT."""


class ParserFileNotFoundError(ParserError):
    """
    Uno dei file TSV richiesti non è stato trovato.

    Viene sollevata quando il file non esiste o non è leggibile.
    """


class MissingColumnError(ParserError):
    """
    Una colonna obbligatoria non è stata trovata nel TSV.

    Questo di solito indica che:
    - è stata esportata la tabella sbagliata, oppure
    - EDT è stato aggiornato e ha cambiato i nomi delle colonne.
    """


class InvalidFormatError(ParserError):
    """
    Il formato di un campo non è valido.

    Esempi:
    - 'Giorno e ora' non nel formato 'lunedì 07h55'
    - 'Durata' non nel formato '1h00'
    - 'Settimana d'applicazione' senza numero
    """
