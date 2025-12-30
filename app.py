from flask import Flask, render_template, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)

# Institutional Portfolio Data: Diverse facilities and multi-jurisdictional stakeholders
portfolio_data = [
    {
        "id": "FAC-TRK-882", "borrower": "Global Logistics S.A.", "facility": "EUR 500M Revolver",
        "exposure": 500000000, "jurisdiction": "UK (Standard)", "obligation": "Quarterly Financial Statements",
        "deadline": (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d'),
        "status": "Overdue", "rm": "Alice Sterling", "cro": "Robert Vance"
    },
    {
        "id": "FAC-TRK-110", "borrower": "Titan Energy Corp", "facility": "USD 1.2B Bridge Facility",
        "exposure": 1200000000, "jurisdiction": "US (Standard)", "obligation": "Asset Disposal Notice",
        "deadline": (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d'),
        "status": "Pending", "rm": "Markus Thorne", "cro": "Robert Vance"
    },
    {
        "id": "FAC-TRK-994", "borrower": "Nordic Pharma", "facility": "GBP 150M Capex Facility",
        "exposure": 150000000, "jurisdiction": "UK (Standard)", "obligation": "Compliance Certificate",
        "deadline": (datetime.now() + timedelta(days=15)).strftime('%Y-%m-%d'),
        "status": "Submitted", "rm": "James Chen", "cro": "Sarah Jenkins"
    },
    {
        "id": "FAC-TRK-402", "borrower": "Solaris Infra", "facility": "USD 300M Term Loan",
        "exposure": 300000000, "jurisdiction": "US (Standard)", "obligation": "Insurance Renewal",
        "deadline": (datetime.now() + timedelta(days=5)).strftime('%Y-%m-%d'),
        "status": "Pending", "rm": "David Chen", "cro": "Robert Vance"
    }
]

def analyze_risk(loan):
    deadline = datetime.strptime(loan['deadline'], '%Y-%m-%d')
    days_left = (deadline - datetime.now()).days
    
    if loan['status'] == "Overdue":
        return {"level": "CRITICAL", "path": f"{loan['cro']} (CRO)", "action": "Breach Escalation"}
    elif days_left <= 2:
        return {"level": "HIGH", "path": f"{loan['rm']} (RM)", "action": "Urgent Follow-up"}
    elif loan['status'] == "Submitted":
        return {"level": "STABLE", "path": "N/A", "action": "Review Document"}
    else:
        return {"level": "MONITOR", "path": "Agency Ops", "action": "Routine Tracking"}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    # Summarize Critical Exposure for the Dashboard KPIs
    crit_val = 0
    for loan in portfolio_data:
        loan['risk'] = analyze_risk(loan)
        if loan['risk']['level'] == "CRITICAL":
            crit_val += loan['exposure']
    
    return render_template('app.html', portfolio=portfolio_data, crit_val=crit_val)

@app.route('/help')
def help():
    glossary = [
        {"term": "Facility Agent", "def": "The administrative body managing communications between the Borrower and Lenders."},
        {"term": "Information Obligation", "def": "A contractual requirement for the borrower to provide updates by a set date."},
        {"term": "Notice of Default", "def": "A formal notification issued when a contractual breach remains unremedied."},
        {"term": "Utilisation Request", "def": "The mechanism for a borrower to draw funds from an active facility."}
    ]
    workflow = [
        {"step": "1. Data Intake", "desc": "Facility terms and deadlines are mapped into the tracking environment."},
        {"step": "2. Tracking", "desc": "The engine monitors 'Reporting Windows' against real-time calendars."},
        {"step": "3. Risk Profiling", "desc": "Logic assigns risk levels based on deadline proximity and status."},
        {"step": "4. Escalation", "desc": "Alerts are routed to specific officers responsible for remediation."}
    ]
    return render_template('help.html', glossary=glossary, workflow=workflow)

@app.route('/api/template/<level>')
def get_template(level):
    templates = {
        "CRITICAL": "URGENT: Formal Notice of Technical Breach regarding subject facility reporting requirements.",
        "HIGH": "NOTICE: Impending reporting deadline. Please confirm status with borrower to avoid escalation."
    }
    return jsonify({"body": templates.get(level, "Standard follow-up regarding loan tracking.")})

if __name__ == '__main__':
    app.run(debug=True)
