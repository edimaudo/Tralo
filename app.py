import random
from datetime import datetime, timedelta
from flask import Flask, render_template, url_for, redirect, request

app = Flask(__name__)

# GLOBAL PORTFOLIO: Restored with all 7 logical data points
portfolio_data = [
    {"id": "LN-101", "borrower": "Precision Mfg Ltd", "loan_type": "Term Loan A", "exposure": 450000000, "jurisdiction": "UK", "track_milestone": "Annual Audited Accounts", "deadline": (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d'), "status": "Overdue", "rm": "Alice Sterling", "cro": "Robert Vance", "margin": "2.25%", "sector": "Manufacturing", "provision_summary": "Net Debt/EBITDA < 3.5x"},
    {"id": "LN-202", "borrower": "Pacific Infra Group", "loan_type": "Project Finance", "exposure": 1100000000, "jurisdiction": "US", "track_milestone": "Quarterly Progress Report", "deadline": (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d'), "status": "Pending", "rm": "Markus Thorne", "cro": "Robert Vance", "margin": "3.10%", "sector": "Infrastructure", "provision_summary": "DSCR > 1.20x"},
    {"id": "LN-303", "borrower": "Global Telecom Corp", "loan_type": "RCF", "exposure": 850000000, "jurisdiction": "Germany", "track_milestone": "Compliance Certificate", "deadline": (datetime.now() + timedelta(days=15)).strftime('%Y-%m-%d'), "status": "Submitted", "rm": "James Chen", "cro": "Sarah Jenkins", "margin": "1.75%", "sector": "Telecommunications", "provision_summary": "Min Net Worth > $2B"},
    {"id": "LN-404", "borrower": "Apex Logistics", "loan_type": "Asset-Based Loan", "exposure": 250000000, "jurisdiction": "UK", "track_milestone": "Borrowing Base Certificate", "deadline": (datetime.now() - timedelta(days=5)).strftime('%Y-%m-%d'), "status": "Overdue", "rm": "Alice Sterling", "cro": "Sarah Jenkins", "margin": "2.50%", "sector": "Transportation", "provision_summary": "Eligible Receivables > 80%"},
    {"id": "LN-505", "borrower": "Solaris Energy", "loan_type": "Green Bond", "exposure": 600000000, "jurisdiction": "France", "track_milestone": "ESG Impact Statement", "deadline": (datetime.now() + timedelta(days=3)).strftime('%Y-%m-%d'), "status": "Pending", "rm": "James Chen", "cro": "Robert Vance", "margin": "1.90%", "sector": "Utilities", "provision_summary": "Renewable Mix > 90%"},
    {"id": "LN-606", "borrower": "Sterling Property REIT", "loan_type": "Development Finance", "exposure": 850000000, "jurisdiction": "UK", "track_milestone": "LTV Certificate", "deadline": (datetime.now() + timedelta(hours=12)).strftime('%Y-%m-%d'), "status": "Pending", "rm": "Alice Sterling", "cro": "Sarah Jenkins", "margin": "3.80%", "sector": "Real Estate", "provision_summary": "LTV < 65%"},
    {"id": "LN-707", "borrower": "CloudScale Systems", "loan_type": "Venture Debt", "exposure": 200000000, "jurisdiction": "US", "track_milestone": "Series D Funding Proof", "deadline": (datetime.now() - timedelta(days=5)).strftime('%Y-%m-%d'), "status": "Overdue", "rm": "Markus Thorne", "cro": "Sarah Jenkins", "margin": "6.50%", "sector": "Technology", "provision_summary": "Runway > 12 Months"}
]

def analyze_track_status(loan):
    try:
        deadline = datetime.strptime(loan['deadline'], '%Y-%m-%d')
        days_left = (deadline - datetime.now()).days
        if loan['status'] == "Overdue":
            return {"level": "OFF-TRACK", "path": f"{loan.get('cro', 'CRO')}", "action": "Remediation Required"}
        elif days_left <= 2:
            return {"level": "AT-RISK", "path": f"{loan.get('rm', 'RM')}", "action": "Urgent Nudge"}
        return {"level": "ON-TRACK", "path": "Monitor", "action": "Log Milestone"}
    except:
        return {"level": "ON-TRACK", "path": "N/A", "action": "Review"}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    total_off_track = 0
    for loan in portfolio_data:
        loan['risk'] = analyze_track_status(loan)
        if loan['risk']['level'] == "OFF-TRACK":
            total_off_track += loan.get('exposure', 0)
    
    formatted_val = "{:,.0f}".format(total_off_track)
    return render_template('app.html', portfolio=portfolio_data, crit_val=formatted_val)

@app.route('/reader')
def reader():
    borrowers = ["Alpha Robotics", "Summit Grid", "Vertex Shipping", "Brio Water"]
    sectors = ["Technology", "Infrastructure", "Transportation", "Utilities"]
    idx = random.randint(0, 3)
    
    extracted_loan = {
        "borrower": borrowers[idx],
        "sector": sectors[idx],
        "jurisdiction": random.choice(["US", "UK", "Germany"]),
        "loan_type": "Bridge Facility",
        "exposure": random.randint(100, 500) * 1000000,
        "margin": "4.25%",
        "track_milestone": "Compliance Certificate",
        "provision_summary": "Leverage < 3.0x",
        "deadline": (datetime.now() + timedelta(days=20)).strftime('%Y-%m-%d')
    }
    return render_template('reader.html', loan=extracted_loan)

@app.route('/add_loan', methods=['POST'])
def add_loan():
    new_loan = {
        "id": f"LN-{random.randint(800, 999)}",
        "borrower": request.form.get('borrower'),
        "loan_type": request.form.get('loan_type'),
        "exposure": int(request.form.get('exposure', 0)),
        "jurisdiction": request.form.get('jurisdiction'),
        "track_milestone": request.form.get('track_milestone'),
        "deadline": request.form.get('deadline'),
        "status": "Submitted",
        "rm": "Auto-RM",
        "cro": "Auto-CRO",
        "margin": request.form.get('margin'),
        "sector": request.form.get('sector'),
        "provision_summary": request.form.get('provision_summary')
    }
    portfolio_data.append(new_loan)
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
