# Fitness Coach Analytics Pipeline

End-to-end analytics pipeline for fitness coaches — from raw data to an interactive dashboard.

> **For coaches:** Instead of spending hours in Excel, you can see at a glance which clients are churning, which package performs best, and how your revenue is growing — no technical knowledge required.

---

## Dashboard

<img width="924" height="606" alt="image" src="https://github.com/user-attachments/assets/71840d0d-4d09-4fd0-9397-dbb69be71ea0" />



🔗 [Open Live Demo](https://lookerstudio.google.com/reporting/dd59615f-0755-4453-9406-625b307797e2)

---

## What this project demonstrates

- Python pipeline that analyzes data and pushes it to Google Sheets
- Google Apps Script button — refresh the analysis with one click, no Python needed
- KPIs: Active clients, MRR, churn rate, revenue per package
- Interactive Looker Studio dashboard with 3 pages

---

## Tech Stack

- Python (pandas, gspread)
- Google Sheets API + Google Apps Script
- Looker Studio

---

## Project Structure

```
fitness-coach-analytics/
├── fitness_analysis.py       — Python pipeline (initial setup)
├── pipeline.gs               — Apps Script (production variant, no Python needed)
├── fitness_coach_data.csv    — Simulated dataset (50 clients)
├── SETUP_GUIDE.md            — Setup instructions
├── TECHNICAL_NOTES.md        — Technical details & decisions
└── assets/
    └── dashboard_screenshot.png
```

---

## Dataset

- 50 simulated fitness coach clients
- AI-generated sample data (no real clients)
- Fields: Client ID, name, package, price, start/end date, status, check-ins, revenue

---

## Author

Johannes — aspiring Data Analyst  
Focus: E-Commerce & small businesses
