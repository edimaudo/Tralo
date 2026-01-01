from flask import Flask, render_template, url_for
from datetime import datetime, timedelta

app = Flask(__name__)

portfolio_data = [
    {
        "id": "LN-101", "borrower": "Precision Mfg Ltd", "loan_type": "Term Loan A",
        "exposure": 450000000, "jurisdiction": "UK", "track_milestone": "Annual Audited Accounts",
        "deadline": (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d'),
        "status": "Overdue", "rm": "Alice Sterling", "cro": "Robert Vance",
        "margin": "2.25%", "sector": "Manufacturing", "provision_summary": "Net Debt/EBITDA < 3.5x"
    },
    {
        "id": "LN-202", "borrower": "Pacific Infra Group", "loan_type": "Project Finance Facility",
        "exposure": 1100000000, "jurisdiction": "US", "track_milestone": "Quarterly Progress Report",
        "deadline": (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d'),
        "status": "Pending", "rm": "Markus Thorne", "cro": "Robert Vance",
        "margin": "3.10%", "sector": "Infrastructure", "provision_summary": "DSCR > 1.20x"
    },
    {
        "id": "LN-303", "borrower": "Global Telecom Corp", "loan_type": "Revolving Credit Facility",
        "exposure": 850000000, "jurisdiction": "Germany", "track_milestone": "Compliance Certificate",
        "deadline": (datetime.now() + timedelta(days=15)).strftime('%Y-%m-%d'),
        "status": "Submitted", "rm": "James Chen", "cro": "Sarah Jenkins",
        "margin": "1.75%", "sector": "Telecommunications", "provision_summary": "Minimum Net Worth > $2B"
    },
    {
        "id": "LN-404", "borrower": "Apex Logistics", "loan_type": "Asset-Based Loan",
        "exposure": 250000000, "jurisdiction": "UK", "track_milestone": "Borrowing Base Certificate",
        "deadline": (datetime.now() - timedelta(days=5)).strftime('%Y-%m-%d'),
        "status": "Overdue", "rm": "Alice Sterling", "cro": "Sarah Jenkins",
        "margin": "2.50%", "sector": "Transportation", "provision_summary": "Eligible Receivables > 80%"
    },
    {
        "id": "LN-505", "borrower": "Solaris Energy", "loan_type": "Green Bond Facility",
        "exposure": 600000000, "jurisdiction": "France", "track_milestone": "ESG Impact Statement",
        "deadline": (datetime.now() + timedelta(days=3)).strftime('%Y-%m-%d'),
        "status": "Pending", "rm": "James Chen", "cro": "Robert Vance",
        "margin": "1.90%", "sector": "Utilities", "provision_summary": "Renewable Mix > 90%"
    }
]

# Milestone History Data
history_logs = [
    {"loan_id": "LN-101", "date": "2023-10-25", "event": "Deadline Missed", "status": "OFF-TRACK", "user": "System Auto-Flag"},
    {"loan_id": "LN-101", "date": "2023-10-20", "event": "Nudge Sent", "status": "AT-RISK", "user": "Alice Sterling (RM)"},
    {"loan_id": "LN-202", "date": "2023-10-28", "event": "Quarterly Report Uploaded", "status": "ON-TRACK", "user": "Borrower Portal"},
    {"loan_id": "LN-202", "date": "2023-10-15", "event": "Track Initialized", "status": "ON-TRACK", "user": "Sarah Jenkins (CRO)"}
]

@app.route('/history/<loan_id>')
def history(loan_id):
    # Filter history for specific loan
    loan_history = [h for h in history_logs if h['loan_id'] == loan_id]
    loan = next((item for item in portfolio_data if item["id"] == loan_id), None)
    return render_template('history.html', history=loan_history, loan=loan)

@app.route('/reader')
def reader():
    # Simulated OCR extraction data
    extracted_clauses = [
        {"clause": "5.1(a)", "title": "Financial Indebtedness", "requirement": "Net Debt/EBITDA < 3.00:1", "frequency": "Quarterly"},
        {"clause": "7.2", "title": "Insurance Certificate", "requirement": "Maintain $50M liability cover", "frequency": "Annual"},
        {"clause": "12.4", "title": "Asset Sales", "requirement": "Notice required for sales > $10M", "frequency": "Ad-hoc"}
    ]
    return render_template('reader.html', clauses=extracted_clauses)

def analyze_risk(loan):
    deadline = datetime.strptime(loan['deadline'], '%Y-%m-%d')
    days_left = (deadline - datetime.now()).days
    if loan['status'] == "Overdue":
        return {"level": "CRITICAL", "path": f"{loan['cro']} (CRO)", "action": "Escalate to Credit Committee"}
    elif days_left <= 2:
        return {"level": "HIGH", "path": f"{loan['rm']} (RM)", "action": "Issue Warning Notice"}
    return {"level": "STABLE", "path": "Internal Monitor", "action": "Log Compliance"}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    total_crit = 0
    for loan in portfolio_data:
        loan['risk'] = analyze_risk(loan)
        if loan['risk']['level'] == "CRITICAL":
            total_crit += loan['exposure']
    
    formatted_crit = "{:,.0f}".format(total_crit)
    return render_template('app.html', portfolio=portfolio_data, crit_val=formatted_crit)

@app.route('/help')
def help():
    return render_template('help.html')

if __name__ == '__main__':
    app.run(debug=True)
