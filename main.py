"""
main.py
=======

Entrypoint del parser EDT → JSON.

Questo script:
1. legge i file TSV esportati da EDT Monoposto 2025.2.5 (versione di consultazione)
2. normalizza e valida i dati
3. costruisce un modello dati unico
4. lo esporta in JSON (es. orario.json)

Note operative:
- I file TSV devono essere ottenuti da EDT tramite:
  - apertura della tabella (Attività, Aule, Docenti, Classi)
  - clic sull'icona "Copia" (due quadrati sovrapposti)
  - scelta del formato CSV/TSV
  - incolla in un editor di testo
  - salvataggio come .tsv con codifica UTF-8

- Questo script è pensato per girare su Debian standard, senza EDT, senza Wine.
"""

from config import (
    ATTIVITA_FILE,
    AULE_FILE,
    DOCENTI_FILE,
    CLASSI_FILE,
    REQUIRED_COLUMNS_ATTIVITA,
    REQUIRED_COLUMNS_AULE,
    REQUIRED_COLUMNS_DOCENTI,
    REQUIRED_COLUMNS_CLASSI,
    EDT_VERSION,
)
from loader import load_tsv
from builder import build_model
from exporter import export_json
from logger import get_logger
from errors import ParserError


logger = get_logger()


def main():
    logger.info(f"Parser EDT avviato (versione EDT attesa: {EDT_VERSION})")

    try:
        logger.info(f"Caricamento '{ATTIVITA_FILE}'…")
        attivita_rows = load_tsv(
            ATTIVITA_FILE, required_columns=REQUIRED_COLUMNS_ATTIVITA
        )

        logger.info(f"Caricamento '{AULE_FILE}'…")
        aule_rows = load_tsv(
            AULE_FILE, required_columns=REQUIRED_COLUMNS_AULE
        )

        logger.info(f"Caricamento '{DOCENTI_FILE}'…")
        docenti_rows = load_tsv(
            DOCENTI_FILE, required_columns=REQUIRED_COLUMNS_DOCENTI
        )

        logger.info(f"Caricamento '{CLASSI_FILE}'…")
        classi_rows = load_tsv(
            CLASSI_FILE, required_columns=REQUIRED_COLUMNS_CLASSI
        )

        logger.info("Costruzione del modello dati…")
        model = build_model(attivita_rows, aule_rows, docenti_rows, classi_rows)

        logger.info("Esportazione JSON in 'orario.json'…")
        export_json(model, path="orario.json")

        logger.info("Operazione completata con successo.")

    except ParserError as e:
        # Errori previsti e spiegabili (file mancanti, colonne mancanti, formati errati)
        logger.error(str(e))
        logger.error(
            "Parsing interrotto per errore. Verificare i file TSV esportati da EDT."
        )
    except Exception as e:
        # Qualsiasi altro errore imprevisto
        logger.error(f"Errore imprevisto: {e}")
        logger.error(
            "Parsing interrotto per errore non previsto. Potrebbe essere necessario "
            "controllare il codice del parser."
        )


if __name__ == "__main__":
    main()
