import random
from datetime import datetime, timedelta
from flask import Flask, render_template, url_for, redirect, request

app = Flask(__name__)

# GLOBAL PORTFOLIO: Restored with 5 logical data points across diverse sectors
portfolio_data = [
    {
        "id": "LN-101", "borrower": "Precision Mfg Ltd", "loan_type": "Term Loan A", 
        "exposure": 450000000, "jurisdiction": "UK", "track_milestone": "Annual Audited Accounts",
        "deadline": (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d'),
        "status": "Overdue", "rm": "Alice Sterling", "cro": "Robert Vance",
        "margin": "2.25%", "sector": "Manufacturing", "provision_summary": "Net Debt/EBITDA < 3.5x"
    },
    {
        "id": "LN-202", "borrower": "Pacific Infra Group", "loan_type": "Project Finance", 
        "exposure": 1100000000, "jurisdiction": "US", "track_milestone": "Quarterly Progress Report",
        "deadline": (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d'),
        "status": "Pending", "rm": "Markus Thorne", "cro": "Robert Vance",
        "margin": "3.10%", "sector": "Infrastructure", "provision_summary": "DSCR > 1.20x"
    },
    {
        "id": "LN-303", "borrower": "Global Telecom Corp", "loan_type": "RCF", 
        "exposure": 850000000, "jurisdiction": "Germany", "track_milestone": "Compliance Certificate",
        "deadline": (datetime.now() + timedelta(days=15)).strftime('%Y-%m-%d'),
        "status": "Submitted", "rm": "James Chen", "cro": "Sarah Jenkins",
        "margin": "1.75%", "sector": "Telecommunications", "provision_summary": "Min Net Worth > $2B"
    },
    {
        "id": "LN-404", "borrower": "Apex Logistics", "loan_type": "Asset-Based Loan", 
        "exposure": 250000000, "jurisdiction": "UK", "track_milestone": "Borrowing Base Certificate",
        "deadline": (datetime.now() - timedelta(days=5)).strftime('%Y-%m-%d'),
        "status": "Overdue", "rm": "Alice Sterling", "cro": "Sarah Jenkins",
        "margin": "2.50%", "sector": "Transportation", "provision_summary": "Eligible Receivables > 80%"
    },
    {
        "id": "LN-505", "borrower": "Solaris Energy", "loan_type": "Green Bond", 
        "exposure": 600000000, "jurisdiction": "France", "track_milestone": "ESG Impact Statement",
        "deadline": (datetime.now() + timedelta(days=3)).strftime('%Y-%m-%d'),
        "status": "Pending", "rm": "James Chen", "cro": "Robert Vance",
        "margin": "1.90%", "sector": "Utilities", "provision_summary": "Renewable Mix > 90%"
    }
]

def analyze_track_status(loan):
    deadline = datetime.strptime(loan['deadline'], '%Y-%m-%d')
    days_left = (deadline - datetime.now()).days
    if loan['status'] == "Overdue":
        return {"level": "OFF-TRACK", "path": f"{loan['cro']} (CRO)", "action": "Remediation Plan Required"}
    elif days_left <= 2:
        return {"level": "AT-RISK", "path": f"{loan['rm']} (RM)", "action": "Urgent Compliance Nudge"}
    return {"level": "ON-TRACK", "path": "Internal Monitor", "action": "Log Milestone"}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    total_off_track = 0
    for loan in portfolio_data:
        loan['risk'] = analyze_track_status(loan)
        if loan['risk']['level'] == "OFF-TRACK":
            total_off_track += loan['exposure']
    
    formatted_val = "{:,.0f}".format(total_off_track)
    return render_template('app.html', portfolio=portfolio_data, crit_val=formatted_val)

@app.route('/reader')
def reader():
    # Dynamic Simulation: Generates a different loan context on every refresh
    borrowers = ["Alpha Robotics", "Summit Grid", "Vertex Shipping", "Skyline Telecom", "Brio Water"]
    sectors = ["Manufacturing", "Infrastructure", "Transportation", "Telecommunications", "Utilities"]
    idx = random.randint(0, 4)
    
    extracted_loan = {
        "borrower": borrowers[idx],
        "sector": sectors[idx],
        "jurisdiction": random.choice(["US", "UK", "Germany", "France"]),
        "loan_type": random.choice(["Term Loan", "RCF", "Bridge Loan"]),
        "exposure": random.randint(100, 900) * 1000000,
        "margin": f"{random.uniform(1.5, 4.0):.2f}%",
        "track_milestone": "Quarterly Financial Certificate",
        "provision_summary": "Net Debt/EBITDA < 3.25x; Interest Cover > 4.0x",
        "deadline": (datetime.now() + timedelta(days=25)).strftime('%Y-%m-%d')
    }
    return render_template('reader.html', loan=extracted_loan)

@app.route('/add_loan', methods=['POST'])
def add_loan():
    # Capture form data from reader.html and persist it in the global portfolio_data list
    new_loan = {
        "id": f"LN-{random.randint(600, 999)}",
        "borrower": request.form.get('borrower'),
        "loan_type": request.form.get('loan_type'),
        "exposure": int(request.form.get('exposure')),
        "jurisdiction": request.form.get('jurisdiction'),
        "track_milestone": request.form.get('track_milestone'),
        "deadline": request.form.get('deadline'),
        "status": "Submitted",
        "rm": "System Assigned",
        "cro": "Unassigned",
        "margin": request.form.get('margin'),
        "sector": request.form.get('sector'),
        "provision_summary": request.form.get('provision_summary')
    }
    portfolio_data.append(new_loan)
    return redirect(url_for('dashboard'))

@app.route('/help')
def help():
    return render_template('help.html')

if __name__ == '__main__':
    app.run(debug=True)
