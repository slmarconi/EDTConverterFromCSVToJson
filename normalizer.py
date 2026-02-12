"""
normalizer.py
=============

Contiene funzioni di normalizzazione e parsing dei campi provenienti
dai TSV di EDT.

Qui avviene la conversione da:
- stringhe EDT (es. "lunedì 07h55", "1h00", "Settimana 49")
a
- valori strutturati (giorno=1, ora="07:55", durata_min=50, settimana=49, ecc.)
"""

import re
from config import DAYS, LESSON_UNIT_MINUTES
from errors import InvalidFormatError


def parse_time(s: str) -> str:
    """
    Converte una stringa oraria EDT nel formato HH:MM.

    Esempio:
    - "07h55" → "07:55"

    :param s: stringa nel formato "HHhMM"
    :raises InvalidFormatError: se il formato non è valido
    """
    match = re.match(r"^(\d{2})h(\d{2})$", s)
    if not match:
        raise InvalidFormatError(f"Formato ora non valido: '{s}'")
    return f"{match.group(1)}:{match.group(2)}"


def parse_duration(s: str) -> int:
    """
    Converte la durata EDT in minuti reali.

    In EDT:
    - "1h00" significa 1 unità didattica
    - "2h00" significa 2 unità didattiche
    ecc.

    Nel contesto della scuola:
    - 1 unità didattica = LESSON_UNIT_MINUTES (es. 50 minuti)

    Esempi:
    - "1h00" → 50
    - "2h00" → 100

    :param s: stringa nel formato "NhMM" (es. "1h00", "4h00")
    :return: durata in minuti reali
    :raises InvalidFormatError: se il formato non è valido
    """
    match = re.match(r"^(\d+)h(\d{2})$", s)
    if not match:
        raise InvalidFormatError(f"Formato durata non valido: '{s}'")

    units = int(match.group(1))
    # Ignoriamo i minuti riportati da EDT (es. "1h00") perché nel contesto
    # della scuola la durata reale è definita a livello di istituto.
    return units * LESSON_UNIT_MINUTES


def parse_day_and_time(s: str):
    """
    Converte il campo "Giorno e ora" in (giorno_numero, "HH:MM").

    Esempi:
    - "lunedì 07h55" → (1, "07:55")
    - "martedì 12h05" → (2, "12:05")
    - "Non piazzata" → None (lezione non piazzata, da ignorare)

    :param s: stringa nel formato "giorno HHhMM" oppure "Non piazzata"
    :return: (giorno_numero, ora_inizio) oppure None
    :raises InvalidFormatError: se il formato non è valido
    """
    if s == "Non piazzata":
        return None

    parts = s.split()
    if len(parts) != 2:
        raise InvalidFormatError(
            f"Formato 'Giorno e ora' non valido: '{s}'"
        )

    day_str, time_str = parts
    if day_str not in DAYS:
        raise InvalidFormatError(f"Giorno non riconosciuto: '{day_str}'")

    return DAYS[day_str], parse_time(time_str)


def parse_week(s: str):
    """
    Estrae il numero di settimana dal campo "Settimana d'applicazione".

    Esempi:
    - "Settimana 49" → 49
    - "Settimana 4" → 4
    - "" → None

    :param s: stringa contenente un numero di settimana
    :return: numero di settimana (int) oppure None
    """
    if not s:
        return None
    match = re.search(r"(\d+)", s)
    return int(match.group(1)) if match else None


def add_minutes(hhmm: str, minutes: int) -> str:
    """
    Aggiunge un certo numero di minuti a un orario HH:MM.

    Esempio:
    - "07:55" + 50 → "08:45"

    :param hhmm: orario di partenza nel formato "HH:MM"
    :param minutes: minuti da aggiungere
    :return: orario risultante nel formato "HH:MM"
    """
    h, m = map(int, hhmm.split(":"))
    total = h * 60 + m + minutes
    return f"{total // 60:02d}:{total % 60:02d}"
