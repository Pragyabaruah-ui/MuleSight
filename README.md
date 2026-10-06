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
