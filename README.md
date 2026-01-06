# Tralo | Loan Obligation Monitoring System

## Overview
Tralo is a montioring system for loan obligations. It bridges the gap between static loan agreements and operational compliance.

## App Design

- **Risk Analysis**: Automated prioritization based on "Time-to-Default," ensuring that the most urgent obligations are surfaced to the top of the workflow.

- **Stakeholder Routing**: Direct escalation paths based on risk severity, automating the internal remediation chain.

- **Exposure Valuation**: Real-time calculation of capital at risk, providing an immediate financial view of portfolio vulnerability.

## Core Features

**1. Unified Obligation Ingestion (Document Intelligence)**

Tralo utilizes OCR and document analysis to map "Provision Language" directly to structured milestones. This replaces manual data entry with a verified digital twin of the loan agreement.

**2. Active Health Monitoring**

The central dashboard calculates "Requirement Health" as a percentage of portfolio stability. Loans are dynamically categorized (STABLE, AT-RISK, OFF-TRACK) based on real-time deadline proximity and submission status.

**3. Closed-Loop Communication**
The system removes communication bottlenecks by automating notice distribution and evidence collection.

Requirement Validation: Instant cross-referencing of borrower-reported data against original agreement parameters to satisfy obligations.

Multi-Channel Distribution: Instant notifications via Email, SMS, and Client Portal (Future update)

## Project structure
```
tralo/
├── app.py
├── requirements.txt
├── README.md
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
└── templates/
    ├── index.html
    ├── app.html
    └── help.html
```

## Setup
1. `pip install -r requirements.txt`
2. `python app.py`
