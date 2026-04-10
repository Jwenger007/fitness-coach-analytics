# Fitness Coach Analytics — Setup Guide

## Was du am Ende hast
- CSV-Datensatz (50 Klienten)
- Python-Skript das die Daten analysiert und in Google Sheets lädt
- 3 Sheets: Rohdaten / KPIs / Paket-Analyse / Monatlich
- Looker Studio Dashboard das sich auf diese Sheets connected

---

## Schritt 1 — Google Service Account erstellen

1. Geh auf https://console.cloud.google.com
2. Neues Projekt erstellen (z.B. "fitness-analytics")
3. APIs aktivieren:
   - "Google Sheets API" suchen → aktivieren
   - "Google Drive API" suchen → aktivieren
4. IAM & Admin → Service Accounts → "+ Service Account erstellen"
   - Name: "fitness-analytics-bot"
   - Rolle: "Editor"
5. Service Account öffnen → Reiter "Schlüssel" → "Schlüssel hinzufügen" → JSON
6. Die heruntergeladene JSON-Datei umbenennen zu: `service_account.json`
7. `service_account.json` in denselben Ordner wie die Python-Datei legen

---

## Schritt 2 — Python Setup

```bash
pip install gspread google-auth pandas
```

Ordnerstruktur:
```
fitness_project/
├── fitness_coach_data.csv
├── fitness_analysis.py
├── service_account.json   ← niemals auf GitHub pushen!
```

---

## Schritt 3 — Skript ausführen

```bash
python fitness_analysis.py
```

Das Skript:
- Erstellt automatisch ein neues Google Sheet ("Fitness Coach Dashboard")
- Lädt Rohdaten + 3 Analyse-Tabs hoch
- Gibt dir am Ende den Link zum Sheet

---

## Schritt 4 — Looker Studio Dashboard

1. Geh auf https://lookerstudio.google.com
2. "Leere Seite" → "+ Daten hinzufügen" → Google Sheets
3. Dein Sheet auswählen, Tab "KPIs" → verbinden
4. Repeat für "Pakete" und "Monatlich"

### Empfohlene Visualisierungen:

**Seite 1 — Übersicht**
- Scorecard: Aktive Klienten
- Scorecard: MRR (Monthly Recurring Revenue)
- Scorecard: Churn Rate %
- Donut Chart: Aktiv vs. Inaktiv

**Seite 2 — Pakete**
- Balkendiagramm: Klienten pro Paket
- Balkendiagramm: Umsatz pro Paket
- Tabelle: Churn Rate pro Paket (wichtigste Insight!)

**Seite 3 — Wachstum**
- Liniendiagramm: Neue Klienten pro Monat
- Liniendiagramm: Neuer Umsatz pro Monat

---

## Was du dem Fitness-Coach zeigen kannst

Die eine Frage die ihn interessiert:
> "Welches Paket bringt mir die loyalsten Kunden?"

Die Antwort liegt in der Churn Rate pro Paket — Premium-Klienten bleiben länger,
auch wenn es weniger sind. Das ist eine Entscheidung ob er Rabatte auf Basis
oder Fokus auf Premium geben soll.

---

## Nächste Schritte nach dem Projekt

1. `.gitignore` anlegen — `service_account.json` niemals committen
2. Skript mit einem Cron-Job automatisieren (einmal pro Woche laufen lassen)
3. Für echte Kunden: Airbyte statt manuellem CSV-Upload
