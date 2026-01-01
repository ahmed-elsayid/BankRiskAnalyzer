# Bank Transaction Risk & Anomaly Analyzer

## Project Overview
This project is a Python-based console application designed to analyze banking transaction data. Its primary objective is to detect risky customers and flag anomalous transactions using statistical techniques (Z-Score analysis) and rule-based logic. The system follows Object-Oriented Programming (OOP) principles to ensure modularity and maintainability.

The application is optimized for the **PaySim Mobile Money Dataset**, focusing specifically on `TRANSFER` and `CASH_OUT` transaction types, which are most indicative of fraudulent activity.

## Features
*   **Data Ingestion:** Loads large CSV datasets with options to limit rows for testing.
*   **Data Cleaning:** Handles missing values, removes duplicates, converts time steps to days, and filters relevant transaction types.
*   **Feature Engineering:** Aggregates customer behavior, including:
    *   Total, Average, and Maximum transaction amounts.
    *   Daily transaction velocity.
    *   Rolling statistical volatility (Standard Deviation).
*   **Risk Scoring:** Calculates a weighted risk score using Z-Scores on transaction magnitude and frequency.
*   **Anomaly Detection:** Flags specific transactions based on business rules (e.g., spikes in spending vs. average behavior).
*   **Reporting:** Generates CSV exports and a textual summary of high-risk entities.

## Folder Structure
```text
BankRiskAnalyzer/
├── data/
│   └── PS_20174392719_1491204439457_log.csv  (Place dataset here)
├── output/
│   ├── customer_risk_summary.csv             (Generated)
│   ├── flagged_transactions.csv              (Generated)
│   └── report.txt                            (Generated)
├── src/
│   ├── ConsoleApp.py
│   ├── DataManager.py
│   ├── FeatureBuilder.py
│   ├── ReportGenerator.py
│   ├── RiskScorer.py
│   ├── TransactionCleaner.py
│   ├── TransactionFlagger.py
│   └── main.py
└── README.md
