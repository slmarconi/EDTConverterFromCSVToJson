"""
config.py
=========

Contiene costanti e configurazioni usate dal parser.

Qui documentiamo anche la versione di EDT per cui il parser è stato
progettato, in modo che in futuro sia chiaro il contesto.
"""

# Versione di EDT Monoposto per cui questo parser è stato scritto.
EDT_VERSION = "EDT Monoposto 2025.2.5 (64bit), versione di consultazione"

# Mappatura dei giorni in italiano → numero (1=lunedì, 7=domenica)
DAYS = {
    "lunedì": 1,
    "martedì": 2,
    "mercoledì": 3,
    "giovedì": 4,
    "venerdì": 5,
    "sabato": 6,
    "domenica": 7,
}

# Durata di una "ora" didattica nel contesto della scuola (in minuti reali).
# ATTENZIONE: in EDT la durata è espressa come "1h00", "2h00", ecc.
# ma nel tuo istituto una "ora" di lezione dura 50 minuti reali.
LESSON_UNIT_MINUTES = 50

# Nomi dei file CSV attesi (esportati da EDT tramite copia negli appunti).
ATTIVITA_FILE = "CSVFiles/Attività.csv"
AULE_FILE = "CSVFiles/Aule.csv"
DOCENTI_FILE = "CSVFiles/Docenti.csv"
CLASSI_FILE = "CSVFiles/Classi.csv"

# Colonne obbligatorie per la tabella Attività.
REQUIRED_COLUMNS_ATTIVITA = [
    "Durata",
    "Giorno e ora",
    "Docente",
    "Materia",
    "Classe",
    "Aula",
    "Settimana d'applicazione",
    "Periodicità",
]

# Colonne obbligatorie per le altre tabelle (più leggere).
REQUIRED_COLUMNS_AULE = [
    "Nome",
]

REQUIRED_COLUMNS_DOCENTI = [
    "Cognome",
    "Nome",
]

REQUIRED_COLUMNS_CLASSI = [
    "Nome",
]
