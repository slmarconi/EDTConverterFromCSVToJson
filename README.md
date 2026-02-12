# Parser EDT → JSON (Debian‑ready)

Questo progetto contiene un parser robusto, documentato e production‑ready per convertire i dati esportati da **EDT Monoposto 2025.2.5 (64bit), versione di consultazione** in un unico file JSON utilizzabile da applicazioni Linux‑native (ad esempio per visualizzare l’occupazione delle aule su una mappa interattiva).

Il parser è progettato per funzionare su **Debian standard**, senza EDT, senza Wine e senza dipendenze esterne oltre a Python 3.

---

## Funzionalità principali

- Converte i file TSV esportati da EDT in un JSON strutturato.
- Normalizza:
  - giorno della settimana
  - orario di inizio
  - durata reale (basata sulle ore didattiche da 50 minuti)
  - ora di fine
  - settimana di applicazione
- Gestisce errori con messaggi chiari e comprensibili.
- Produce un JSON pronto per essere consumato da applicazioni web o desktop.
- Architettura modulare, facile da mantenere e estendere.

---

## Contesto: EDT Monoposto

Questo parser è stato scritto per la versione:

EDT Monoposto 2025.2.5 (64bit), versione di consultazione


Note importanti:

- La versione di consultazione **non permette l’esportazione diretta su file**.
- L’unico metodo disponibile è:
  1. aprire una tabella in EDT  
  2. cliccare sull’icona **Copia** (due quadrati sovrapposti)  
  3. scegliere il formato CSV 
  4. incollare in un editor di testo  
  5. salvare come `.csv` (UTF‑8)

EDT usa **TAB** come separatore, non virgole o punti e virgola.
---

## File richiesti

Il parser si aspetta questi file nella stessa cartella:

- `Attività.csv`
- `Aule.csv`
- `Docenti.csv`
- `Classi.csv`

Questi file devono essere esportati da EDT come descritto sopra.

---

## Output

Il parser genera:

```
orario.json
```

con struttura semplificata:

```json
{
  "lezioni": [...],
  "aule": [...],
  "docenti": [...],
  "classi": [...]
}
```

In appendice si trova la struttura completa.

## Durata delle lezioni: 50 minuti
EDT rappresenta le durate come:

1h00

2h00

4h00

Questi valori non rappresentano minuti reali, ma unità didattiche.

Nel contesto della scuola:
1 unità didattica = 50 minuti reali

Il parser converte automaticamente:

1h00 → 50 minuti

2h00 → 100 minuti

4h00 → 200 minuti

E calcola anche l’ora di fine della lezione.


---

# **Esecuzione + Struttura progetto + Dettagli tecnici**

---

## Come eseguire il parser

Assicurati di avere Python 3 installato.

Poi:

```bash
cd parser
python3 main.py
```

Se tutto è corretto, vedrai:

```
[INFO] Parser EDT avviato...
[INFO] Caricamento 'Attività.tsv'…
[INFO] Costruzione del modello dati…
[INFO] Esportazione JSON in 'orario.json'…
[INFO] Operazione completata con successo.
```

# Struttura del progetto

```
parser/
├── main.py                # entrypoint
├── config.py              # costanti, mapping giorni, versione EDT
├── logger.py              # logging leggibile
├── errors.py              # eccezioni personalizzate
├── loader.py              # caricamento TSV con validazioni
├── normalizer.py          # parsing e normalizzazione campi EDT
├── builder.py             # costruzione del modello dati
└── exporter.py            # scrittura JSON finale
```

# Dettagli tecnici

## Normalizzazione dei campi

- Giorno e ora

    - "lunedì 07h55" → giorno=1, ora="07:55"

    - "Non piazzata" → ignorata

- Durata

    - "1h00" → 50 minuti

    - "2h00" → 100 minuti

- Ora di fine

    - calcolata automaticamente

- Settimana d'applicazione

    - "Settimana 49" → 49


---

# **Troubleshooting**


## ❌ Errore: “File non trovato”
Probabilmente i file TSV non sono nella stessa cartella di `main.py`.

## ❌ Errore: “Colonna obbligatoria non presente”
Possibili cause:

- esportata la tabella sbagliata da EDT  
- EDT aggiornato → nomi colonne cambiati  
- TSV salvato male (es. separatore non TAB)  

## ❌ Errore: “Formato ora non valido”
Il campo “Giorno e ora” potrebbe essere stato modificato manualmente.

---

# **Licenza**

Puoi usare, modificare e distribuire questo parser liberamente all’interno della scuola.

---

# **Manutenzione futura**

Il parser è stato scritto per essere leggibile anche da chi:

- non conosce EDT  
- non conosce Python  
- non conosce il contesto originario  

Ogni modulo contiene commenti dettagliati che spiegano:

- perché esiste  
- cosa fa  
- come funziona  
- cosa aspettarsi dai dati di EDT  

Se EDT dovesse cambiare formato, sarà sufficiente aggiornare:

- `config.py` (nomi colonne)  
- `normalizer.py` (formati dei campi)  

---

# Contatti

Per domande o manutenzione futura, consultare il responsabile tecnico del progetto.

# Appendici
## Esempio di struttura completa di output.json
```
{
  "lezioni": [
    {
      "giorno": 1,
      "inizio": "07:55",
      "fine": "08:45",
      "durata_min": 50,
      "docente": "Montalbano Stefano",
      "materia": "AUTOMAZIONE - Sistemi Automazione",
      "classe": "5m_Fen",
      "aula": "_LabCloud_303",
      "settimana": 49,
      "periodicita": "S (33/33)"
    }
  ],

  "aule": [
    {
      "nome": "_LabCloud_303",
      "capienza": null,
      "quantita": "1",
      "occupazione": "22h00",
      "tasso_occupazione_potenziale": "26%",
      "picco_occupazione": null
    }
  ],

  "docenti": [
    {
      "titolo": "Prof.",
      "cognome": "Bianchi",
      "nome": "Sonia",
      "email": "Sonia.Bianchi@marconirovereto.it",
      "disciplina": "AB24   Inglese",
      "monte_ore_settimanale": "12h00",
      "monte_ore_annuale": "0h00"
    }
  ],

  "classi": [
    {
      "nome": "1D",
      "alunni_inseriti": "25",
      "numero_alunni": "0",
      "livello": "1°",
      "piano_studi": null,
      "aula_preferenziale": "*-*"
    }
  ]
}
```