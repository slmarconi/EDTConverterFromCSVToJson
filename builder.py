"""
builder.py
==========

Costruisce il modello dati a partire dalle righe TSV caricate e normalizzate.

Qui trasformiamo:
- le righe di Attività.tsv in una lista di "lezioni"
- le righe di Aule.tsv in una lista di "aule"
- le righe di Docenti.tsv in una lista di "docenti"
- le righe di Classi.tsv in una lista di "classi"

Il risultato finale è un dizionario pronto per essere serializzato in JSON.
"""

from normalizer import (
    parse_day_and_time,
    parse_duration,
    parse_week,
    add_minutes,
)


def build_lessons(attivita_rows):
    """
    Costruisce la lista delle lezioni a partire dalle righe di Attività.tsv.

    Ogni lezione è un dict con campi normalizzati, ad esempio:
    {
      "giorno": 1,
      "inizio": "07:55",
      "fine": "08:45",
      "durata_min": 50,
      "docente": "...",
      "materia": "...",
      "classe": "...",
      "aula": "...",
      "settimana": 49,
      "periodicita": "S (33/33)"
    }
    """
    lessons = []

    for row in attivita_rows:
        parsed = parse_day_and_time(row["Giorno e ora"])
        if parsed is None:
            # Lezione non piazzata: non ha senso per la mappa delle aule.
            continue

        day, start = parsed
        duration_min = parse_duration(row["Durata"])
        end = add_minutes(start, duration_min)

        lessons.append(
            {
                "giorno": day,
                "inizio": start,
                "fine": end,
                "durata_min": duration_min,
                "docente": row["Docente"],
                "materia": row["Materia"],
                "classe": row["Classe"],
                "aula": row["Aula"],
                "settimana": parse_week(row["Settimana d'applicazione"]),
                "periodicita": row["Periodicità"],
            }
        )

    return lessons


def build_rooms(aule_rows):
    """
    Costruisce la lista delle aule a partire da Aule.tsv.

    Esempio di output:
    {
      "nome": "_LabCloud_303",
      "capienza": null,
      "occupazione": "22h00",
      "tasso_occupazione_potenziale": "26%"
    }

    Nota: molti campi sono opzionali o solo informativi.
    """
    rooms = []

    for row in aule_rows:
        rooms.append(
            {
                "nome": row.get("Nome"),
                "capienza": row.get("Capienza") or None,
                "quantita": row.get("Quantità") or None,
                "occupazione": row.get("Occupazione") or None,
                "tasso_occupazione_potenziale": row.get(
                    "Tasso d'occup. potenziale"
                )
                or row.get('"Tasso d\'occup. potenziale"')
                or None,
                "picco_occupazione": row.get("Picco d'occupazione")
                or row.get('"Picco d\'occupazione"')
                or None,
            }
        )

    return rooms


def build_teachers(docenti_rows):
    """
    Costruisce la lista dei docenti a partire da Docenti.tsv.

    Esempio di output:
    {
      "titolo": "Prof.",
      "cognome": "Bianchi",
      "nome": "Sonia",
      "email": "Sonia.Bianchi@...",
      "disciplina": "AB24   Inglese"
    }
    """
    teachers = []

    for row in docenti_rows:
        teachers.append(
            {
                "titolo": row.get("Titolo") or None,
                "cognome": row.get("Cognome"),
                "nome": row.get("Nome"),
                "email": row.get("E-mail") or row.get("E-mail ") or None,
                "disciplina": row.get("Disciplina") or None,
                "monte_ore_settimanale": row.get("Monte ore settimanale")
                or row.get('"Monte ore settimanale"')
                or None,
                "monte_ore_annuale": row.get("Monte ore annuale")
                or row.get('"Monte ore annuale"')
                or None,
            }
        )

    return teachers


def build_classes(classi_rows):
    """
    Costruisce la lista delle classi a partire da Classi.tsv.

    Esempio di output:
    {
      "nome": "1D",
      "alunni_inseriti": 25,
      "numero_alunni": 0,
      "livello": "1°",
      "piano_studi": "...",
      "aula_preferenziale": null
    }
    """
    classes = []

    for row in classi_rows:
        classes.append(
            {
                "nome": row.get("Nome"),
                "alunni_inseriti": row.get("Alunni inseriti")
                or row.get('"Alunni inseriti"')
                or None,
                "numero_alunni": row.get("Numero di alunni")
                or row.get('"Numero di alunni"')
                or None,
                "livello": row.get("Livelli") or None,
                "piano_studi": row.get("Piano di studi")
                or row.get('"Piano di studi"')
                or None,
                "aula_preferenziale": row.get("Aula preferenziale")
                or row.get('"Aula preferenziale"')
                or None,
            }
        )

    return classes


def build_model(attivita_rows, aule_rows, docenti_rows, classi_rows):
    """
    Costruisce il modello dati completo da esportare in JSON.

    Struttura:
    {
      "lezioni": [...],
      "aule": [...],
      "docenti": [...],
      "classi": [...]
    }
    """
    return {
        "lezioni": build_lessons(attivita_rows),
        "aule": build_rooms(aule_rows),
        "docenti": build_teachers(docenti_rows),
        "classi": build_classes(classi_rows),
    }
