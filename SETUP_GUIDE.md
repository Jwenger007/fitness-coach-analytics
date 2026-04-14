# Fitness Coach Analytics — Setup Guide

## What you'll have at the end

- CSV dataset (50 clients)
- Python script that analyzes data and pushes it to Google Sheets (initial setup)
- Google Apps Script button — refresh the analysis with one click, no Python needed (production variant)
- 4 Sheets: Raw data / KPIs / Package analysis / Monthly
- Looker Studio dashboard connected to these sheets

---

## Option A — Python Pipeline (initial setup)

### Step 1 — Create a Google Service Account

1. Go to https://console.cloud.google.com
2. Create a new project (e.g. "fitness-analytics")
3. Enable APIs:
   - Search "Google Sheets API" → enable
   - Search "Google Drive API" → enable
4. IAM & Admin → Service Accounts → "+ Create Service Account"
   - Name: "fitness-analytics-bot"
   - Role: "Editor"
5. Open the service account → "Keys" tab → "Add Key" → JSON
6. Rename the downloaded file to `service_account.json`
7. Place `service_account.json` in the same folder as the Python script

### Step 2 — Python setup

```bash
pip install gspread google-auth pandas
```

Folder structure:
```
fitness_project/
├── fitness_coach_data.csv
├── fitness_analysis.py
└── service_account.json   ← never push this to GitHub!
```

### Step 3 — Run the script

```bash
python fitness_analysis.py
```

The script will:
- Automatically create a new Google Sheet ("Fitness Coach Dashboard")
- Upload raw data + 3 analysis tabs
- Print the link to the sheet at the end

---

## Option B — Google Apps Script (production variant)

No Python, no terminal, no setup. Runs directly inside Google Sheets.

### Step 1 — Add the script

In your Google Sheet: **Extensions → Apps Script** → paste the contents of `pipeline.gs` → save → run once manually to grant permissions.

### Step 2 — Create a button

Insert → Drawing → draw any shape → add text "Refresh Analysis" → save. Then right-click the button in the sheet → assign script → enter `analyseAktualisieren`.

### Step 3 — Done

The coach presses the button → all three tabs (KPIs, Packages, Monthly) are recalculated automatically.

---

## Step 4 — Looker Studio Dashboard

1. Go to https://lookerstudio.google.com
2. Blank report → "+ Add data" → Google Sheets
3. Select your sheet, tab "KPIs" → connect
4. Repeat for "Pakete" and "Monatlich"

### Recommended visualizations

**Page 1 — Overview**
- Scorecard: Active clients
- Scorecard: MRR (Monthly Recurring Revenue)
- Scorecard: Churn Rate %
- Donut chart: Active vs. Inactive

**Page 2 — Packages**
- Bar chart: Clients per package
- Bar chart: Revenue per package
- Table: Churn rate per package (key insight!)

**Page 3 — Growth**
- Line chart: New clients per month
- Line chart: New revenue per month

---

## Next steps

1. `.gitignore` — never commit `service_account.json`
2. For larger clients: replace manual CSV upload with Shopify API or Airbyte
3. Automate with a time-based trigger in Apps Script (runs weekly, no cron job needed)
