# MuleSight

### AML Transaction-Network Analysis and Mule Account Intelligence Platform

MuleSight is a transaction analytics platform designed to identify potentially suspicious mule accounts by analyzing transaction patterns and account relationships.

## Problem Statement

Banks process thousands of transactions every day, making it difficult to manually identify mule accounts that receive and move suspicious funds. Mule activity is often visible through patterns of money movement between multiple accounts rather than through a single transaction.

MuleSight analyzes transaction behavior to identify suspicious patterns such as fan-in, fan-out, rapid pass-through, and circular flows. It assigns risk scores to accounts and provides reasons for each alert to support analyst investigation.

## Key Features

- Transaction data generation and preprocessing
- Account-level feature engineering
- Fan-in detection
- Fan-out detection
- Rapid pass-through detection
- Circular transaction flow detection
- Rule-based mule account risk scoring
- Detection performance evaluation
- Interactive Streamlit dashboard
- Risk-level and typology-based filtering

## Project Workflow

```text
Transaction Data
       ↓
Data Cleaning
       ↓
Feature Engineering
       ↓
Suspicious Pattern Detection
       ↓
Risk Scoring
       ↓
Mule Account Evaluation
       ↓
Interactive Dashboard
```

## Suspicious Patterns

| Pattern | Description |
|---|---|
| Fan-in | Multiple accounts sending money into a single account |
| Fan-out | A single account distributing money to multiple accounts |
| Rapid Pass-through | Money received and transferred out within a short period |
| Circular Flow | Money moving through a cycle of connected accounts |

## Dataset

The project uses a **synthetically generated transaction dataset** containing:

- 50,000 normal transactions
- 2,000 accounts
- 104 injected suspicious transactions
- Transaction timestamp, sender, receiver, amount and channel information

The suspicious transactions were intentionally injected to evaluate whether the detection system could identify known mule-account patterns.

## Results

The prototype successfully detected:

**6 out of 7 known injected mule accounts**

**Detection Rate: 85.71%**

The system categorizes accounts into:

- High Risk
- Medium Risk
- Low Risk

## Dashboard

The Streamlit dashboard provides:

- Overall transaction statistics
- Suspicious transaction counts
- Risk-level distribution
- Suspicious typology analysis
- Top suspicious accounts
- Risk score distribution
- Transaction-level investigation
- Interactive risk and typology filters

## Tech Stack

- Python
- Pandas
- NumPy
- Plotly
- Streamlit
- Git & GitHub

## Project Structure

```text
MuleSight/
│
├── data/
│   ├── transactions.csv
│   ├── transactions_with_fraud.csv
│   ├── account_features.csv
│   └── mule_risk_scores.csv
│
├── src/
│   ├── data_generator.py
│   ├── fraud_injector.py
│   ├── feature_engineering.py
│   ├── mule_detector.py
│   ├── evaluation.py
│   └── dashboard.py
│
├── .gitignore
└── README.md
```

## How to Run

Install the required libraries:

```bash
pip install pandas numpy streamlit plotly
```

Run the dashboard:

```bash
cd src
streamlit run dashboard.py
```

## Project Objective

The objective of MuleSight is to demonstrate how transaction-level data can be transformed into account-level intelligence using behavioral patterns, rule-based risk scoring, and interactive analytics.

> **Note:** This is a portfolio/research prototype using synthetic transaction data and is not intended to represent a production AML detection system.
