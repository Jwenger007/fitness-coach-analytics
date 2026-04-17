# Technical Notes

## Architecture

Two pipeline variants were built for this project, each suited to a different client type.

**Python Pipeline** — designed for the initial setup and data ingestion. Uses pandas for data transformation, gspread for Google Sheets authentication via a Service Account, and pushes raw data plus calculated summaries into separate tabs. Best suited for developers or cases where data comes from external sources (APIs, databases).

**Google Apps Script** — the production variant. Runs entirely inside Google Sheets, reads from the "Klienten" tab, recalculates all KPIs and summaries, and writes the results back — triggered by a button. No Python installation, no credentials file, no terminal. Best suited for small clients who just need a refresh button.

Looker Studio connects directly to the Google Sheet and reads the processed tabs. No direct connection to raw data — all logic lives in the pipeline.

---

## Key decisions

**Why Google Sheets as the data layer instead of a database?**
For small clients like a fitness coach with 50 clients, a database adds unnecessary complexity. Google Sheets is accessible, shareable, and Looker Studio connects to it natively. The tradeoff is scalability — for larger datasets or multiple data sources, a proper database would be the right move.

**Why two pipelines?**
The Python pipeline was built first as a learning project and demonstrates the full data engineering flow. The Apps Script variant was added as the more practical solution for the client — they don't need Python installed to refresh their data. Having both in the repo shows the reasoning behind each approach.

**Why simulated data?**
No real client data was available at this stage. The dataset was generated to reflect realistic fitness coach metrics — churn patterns, package distribution, revenue ranges — so the analysis and dashboard are meaningful despite being synthetic.

---

## Bugs & learnings

**FileNotFoundError** — the script couldn't find `service_account.json` because it was being run from a different working directory. Fixed by ensuring the terminal was always opened in the project folder.

**Google API 403 error** — the Service Account had the correct role but the Sheet hadn't been shared with the service account email. Fixed by sharing the Sheet directly with the service account address.

**JSON serialization error (int64 / float NaN)** — pandas uses NumPy data types internally which aren't JSON-serializable by default. Fixed by converting the dataframe to string before uploading, and handling NaN values explicitly.

**Apps Script cold start** — the first execution after opening the script editor takes noticeably longer due to Google's cold start. Normal behavior, not a bug.

**Looker Studio field mismatch** — after switching from the Python pipeline to Apps Script, some column names in the Packages tab changed slightly. Looker Studio lost the field mapping and showed a dataset configuration error. Fixed by re-mapping the fields in the affected charts.

---

## What would change for a real client

- Replace the CSV with a live data source (Shopify API, booking system export, or a simple form)
- Add input validation in Apps Script to handle missing or malformed rows gracefully
- Set up a time-based trigger in Apps Script so the analysis refreshes automatically once a week without any manual action
- For larger clients: move to a proper ETL tool (Airbyte) and a database instead of Google Sheets
