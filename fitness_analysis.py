"""
Fitness Coach Analytics — Google Sheets Pipeline
=================================================
Schritt 1: pip install gspread google-auth pandas
Schritt 2: Google Service Account erstellen
Schritt 3: Skript ausführen
"""

import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# ─── KONFIGURATION ────────────────────────────────────────────────
CREDENTIALS_FILE = "service_account.json"
SPREADSHEET_ID = "13cyH3MjxqeAn2IV4oEgQjpvzRwdHgNhDb2lwecoZZQQ"
CSV_FILE = "fitness_coach_data.csv"
# ──────────────────────────────────────────────────────────────────


def connect_sheets():
    """Verbindung zu Google Sheets herstellen."""
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]
    creds = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=scopes)
    client = gspread.authorize(creds)
    return client


def upload_raw_data(client, df):
    """Rohdaten in Sheet 'Klienten' hochladen."""
    spreadsheet = client.open_by_key(SPREADSHEET_ID)

    # Sheet "Klienten" anlegen oder leeren
    try:
        ws = spreadsheet.worksheet("Klienten")
        ws.clear()
    except gspread.WorksheetNotFound:
        ws = spreadsheet.add_worksheet("Klienten", rows=100, cols=20)

  # Header + Daten hochladen
    df = df.fillna("")
    data = [df.columns.tolist()] + df.fillna("").astype(str).replace("nan", "").values.tolist()
    ws.update(data, value_input_option="USER_ENTERED")
    print(f"✓ {len(df)} Klienten in Sheet 'Klienten' hochgeladen")
    return spreadsheet


def calculate_kpis(df):
    """Kernkennzahlen berechnen."""
    df["startdatum"] = pd.to_datetime(df["startdatum"])

    total = len(df)
    aktiv = df[df["status"] == "Aktiv"]
    inaktiv = df[df["status"] == "Inaktiv"]

    kpis = {
        "Gesamt Klienten": total,
        "Aktive Klienten": len(aktiv),
        "Inaktive Klienten (Churn)": len(inaktiv),
        "Churn Rate (%)": round(len(inaktiv) / total * 100, 1),
        "Gesamtumsatz (€)": df["gesamtumsatz"].sum(),
        "Ø Umsatz pro Klient (€)": round(df["gesamtumsatz"].mean(), 0),
        "Ø Aktive Monate": round(df["aktive_monate"].mean(), 1),
        "MRR aktiv (€)": aktiv["preis_monat"].sum(),
    }
    return {k: int(v) if hasattr(v, 'item') else v for k, v in kpis.items()}

def calculate_paket_summary(df):
    """Auswertung nach Paket."""
    summary = df.groupby("paket").agg(
        klienten=("klient_id", "count"),
        aktiv=("status", lambda x: (x == "Aktiv").sum()),
        umsatz_gesamt=("gesamtumsatz", "sum"),
        avg_monate=("aktive_monate", "mean"),
    ).round(1).reset_index()
    summary["churn_rate_%"] = round(
        (summary["klienten"] - summary["aktiv"]) / summary["klienten"] * 100, 1
    )
    return summary


def calculate_monthly_revenue(df):
    """Monatlicher Umsatz schätzen (vereinfacht)."""
    df["startdatum"] = pd.to_datetime(df["startdatum"])
    df["monat"] = df["startdatum"].dt.to_period("M")
    monthly = df.groupby("monat").agg(
        neue_klienten=("klient_id", "count"),
        neuer_umsatz=("preis_monat", "sum"),
    ).reset_index()
    monthly["monat"] = monthly["monat"].astype(str)
    return monthly


def upload_analysis(spreadsheet, kpis, paket_df, monthly_df):
    """Analyse-Sheets hochladen."""

    # Sheet: KPIs
    try:
        ws_kpi = spreadsheet.worksheet("KPIs")
        ws_kpi.clear()
    except gspread.WorksheetNotFound:
        ws_kpi = spreadsheet.add_worksheet("KPIs", rows=20, cols=5)

    kpi_data = [["Kennzahl", "Wert"]] + [[k, v] for k, v in kpis.items()]
    ws_kpi.update(kpi_data, value_input_option="USER_ENTERED")
    print("✓ KPIs hochgeladen")

    # Sheet: Paket-Analyse
    try:
        ws_paket = spreadsheet.worksheet("Pakete")
        ws_paket.clear()
    except gspread.WorksheetNotFound:
        ws_paket = spreadsheet.add_worksheet("Pakete", rows=20, cols=10)

    paket_data = [paket_df.columns.tolist()] + paket_df.astype(str).values.tolist()
    ws_paket.update(paket_data, value_input_option="USER_ENTERED")
    print("✓ Paket-Analyse hochgeladen")

    # Sheet: Monatlich
    try:
        ws_monthly = spreadsheet.worksheet("Monatlich")
        ws_monthly.clear()
    except gspread.WorksheetNotFound:
        ws_monthly = spreadsheet.add_worksheet("Monatlich", rows=50, cols=5)

    monthly_data = [monthly_df.columns.tolist()] + monthly_df.astype(str).values.tolist()
    ws_monthly.update(monthly_data, value_input_option="USER_ENTERED")
    print("✓ Monatliche Daten hochgeladen")


def main():
    print("── Fitness Coach Analytics Pipeline ──")

    # 1. Daten laden
    df = pd.read_csv(CSV_FILE)
    print(f"✓ CSV geladen: {len(df)} Klienten")

    # 2. Google Sheets verbinden
    client = connect_sheets()
    print("✓ Google Sheets verbunden")

    # 3. Rohdaten hochladen
    spreadsheet = upload_raw_data(client, df)

    # 4. Analysen berechnen
    kpis = calculate_kpis(df)
    paket_df = calculate_paket_summary(df)
    monthly_df = calculate_monthly_revenue(df)

    print("\n── KPIs ──")
    for k, v in kpis.items():
        print(f"  {k}: {v}")

    # 5. Analyse-Sheets hochladen
    upload_analysis(spreadsheet, kpis, paket_df, monthly_df)

    url = f"https://docs.google.com/spreadsheets/d/{spreadsheet.id}"
    print(f"\n✓ Fertig! Sheet öffnen: {url}")


if __name__ == "__main__":
    main()