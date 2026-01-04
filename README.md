# Tralo | Loan Obligation Monitoring System

## Overview
Tralo is a montioring system for loan obligations. It bridges the gap between static loan agreements and operational compliance.

## App Design
- **Risk Analysis:** Automated prioritization based on "Time-to-Default."
- **Stakeholder Routing:** Direct escalation paths (RM/CRO) based on risk severity.
- **Exposure Valuation:** Real-time calculation of capital at risk.

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
