import random
from datetime import datetime, timedelta
from flask import Flask, render_template, url_for, redirect, request

app = Flask(__name__)

# --- CORRECT MASTER PORTFOLIO DATA ---
portfolio_data = [
    {"id": "LN-101", "borrower": "Precision Mfg Ltd", "loan_type": "Financial Maintenance", "exposure": 450000000, "jurisdiction": "UK", "track_milestone": "Annual Audited Accounts", "deadline": (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d'), "status": "Overdue", "rm": "Alice Sterling", "cro": "Robert Vance", "margin": "2.25%", "sector": "Manufacturing", "provision_summary": "Net Debt/EBITDA < 3.5x"},
    {"id": "LN-202", "borrower": "Pacific Infra Group", "loan_type": "Reporting Obligation", "exposure": 1100000000, "jurisdiction": "US", "track_milestone": "Quarterly Progress Report", "deadline": (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d'), "status": "Pending", "rm": "Markus Thorne", "cro": "Robert Vance", "margin": "3.10%", "sector": "Infrastructure", "provision_summary": "DSCR > 1.20x"},
    {"id": "LN-303", "borrower": "Global Telecom Corp", "loan_type": "Information Delivery", "exposure": 850000000, "jurisdiction": "Germany", "track_milestone": "Compliance Certificate", "deadline": (datetime.now() + timedelta(days=15)).strftime('%Y-%m-%d'), "status": "Submitted", "rm": "James Chen", "cro": "Sarah Jenkins", "margin": "1.75%", "sector": "Telecommunications", "provision_summary": "Min Net Worth > $2B"},
    {"id": "LN-404", "borrower": "Apex Logistics", "loan_type": "Financial Maintenance", "exposure": 250000000, "jurisdiction": "UK", "track_milestone": "Borrowing Base Certificate", "deadline": (datetime.now() - timedelta(days=5)).strftime('%Y-%m-%d'), "status": "Overdue", "rm": "Alice Sterling", "cro": "Sarah Jenkins", "margin": "2.50%", "sector": "Transportation", "provision_summary": "Eligible Receivables > 80%"},
    {"id": "LN-505", "borrower": "Solaris Energy", "loan_type": "Reporting Obligation", "exposure": 600000000, "jurisdiction": "France", "track_milestone": "ESG Impact Statement", "deadline": (datetime.now() + timedelta(days=3)).strftime('%Y-%m-%d'), "status": "Pending", "rm": "James Chen", "cro": "Robert Vance", "margin": "1.90%", "sector": "Utilities", "provision_summary": "Renewable Mix > 90%"},
    {"id": "LN-606", "borrower": "Sterling Property REIT", "loan_type": "Financial Maintenance", "exposure": 850000000, "jurisdiction": "UK", "track_milestone": "LTV Certificate", "deadline": (datetime.now() + timedelta(hours=12)).strftime('%Y-%m-%d'), "status": "Pending", "rm": "Alice Sterling", "cro": "Sarah Jenkins", "margin": "3.80%", "sector": "Real Estate", "provision_summary": "LTV < 65%"},
    {"id": "LN-707", "borrower": "General Undertaking", "loan_type": "General Undertaking", "exposure": 200000000, "jurisdiction": "US", "track_milestone": "Series D Funding Proof", "deadline": (datetime.now() - timedelta(days=5)).strftime('%Y-%m-%d'), "status": "Overdue", "rm": "Markus Thorne", "cro": "Sarah Jenkins", "margin": "6.50%", "sector": "Technology", "provision_summary": "Runway > 12 Months"}
]

# --- SYNCHRONIZED HISTORY ---
history_logs = []
for loan in portfolio_data:
    history_logs.append({
        "loan_id": loan['id'],
        "borrower": loan['borrower'],
        "date": "2025-12-01",
        "event": "Governance Track Initialized",
        "status": "OFF-TRACK" if loan['status'] == "Overdue" else "ON-TRACK"
    })

def analyze_track_status(loan):
    deadline = datetime.strptime(loan['deadline'], '%Y-%m-%d')
    days_left = (deadline - datetime.now()).days
    if loan['status'] == "Overdue":
        return {"level": "OFF-TRACK", "color": "danger", "path": f"{loan['cro']} (CRO)", "action": "Remediate"}
    elif days_left <= 2:
        return {"level": "AT-RISK", "color": "warning", "path": f"{loan['rm']} (RM)", "action": "Nudge"}
    return {"level": "ON-TRACK", "color": "success", "path": "Monitor", "action": "Update"}

# Context processor to make datetime available in all templates
@app.context_processor
def inject_now():
    return {'datetime': datetime, 'timedelta': timedelta}

@app.route('/')
def index(): return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    total_off_track = 0
    for loan in portfolio_data:
        loan['risk'] = analyze_track_status(loan)
        if loan['risk']['level'] == "OFF-TRACK":
            total_off_track += loan['exposure']
    return render_template('app.html', portfolio=portfolio_data, crit_val="{:,.0f}".format(total_off_track))

@app.route('/history')
def history(): return render_template('history.html', history=history_logs)

@app.route('/reader')
def reader():
    return render_template('reader.html', loan={
        "borrower": "Vertex Global", "sector": "Logistics", "jurisdiction": "US",
        "loan_type": "Information Delivery", "exposure": 250000000, "margin": "2.25%",
        "track_milestone": "Compliance Cert", "provision_summary": "LTV < 50%",
        "deadline": (datetime.now() + timedelta(days=20)).strftime('%Y-%m-%d')
    })

@app.route('/add_loan', methods=['POST'])
def add_loan():
    new_loan = {
        "id": f"LN-{random.randint(800, 999)}", "borrower": request.form.get('borrower'),
        "loan_type": request.form.get('loan_type'), "exposure": int(request.form.get('exposure', 0)),
        "jurisdiction": request.form.get('jurisdiction'), "track_milestone": request.form.get('track_milestone'),
        "deadline": request.form.get('deadline'), "status": "Submitted",
        "margin": request.form.get('margin'), "sector": request.form.get('sector'),
        "provision_summary": request.form.get('provision_summary')
    }
    portfolio_data.append(new_loan)
    history_logs.insert(0, {"loan_id": new_loan['id'], "borrower": new_loan['borrower'], "date": datetime.now().strftime('%Y-%m-%d'), "event": "Track Ingested via OCR", "status": "ON-TRACK"})
    return redirect(url_for('dashboard'))

@app.route('/help')
def help(): return render_template('help.html')

if __name__ == '__main__': app.run(debug=True)
