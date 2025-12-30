from flask import Flask, render_template, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)

# The Portfolio: Diverse facilities and multi-jurisdictional stakeholders
portfolio_data = [
    {
        "id": "FAC-LMA-882", "borrower": "Global Logistics S.A.", "facility": "EUR 500M Revolver",
        "exposure": 500000000, "jurisdiction": "UK (LMA)", "obligation": "Quarterly Financial Covenant",
        "deadline": (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d'),
        "status": "Overdue", "rm": "Alice Sterling", "cro": "Robert Vance"
    },
    {
        "id": "FAC-LSTA-110", "borrower": "Titan Energy Corp", "facility": "USD 1.2B Term Loan B",
        "exposure": 1200000000, "jurisdiction": "US (LSTA)", "obligation": "Asset Disposal Notice",
        "deadline": (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d'),
        "status": "Pending", "rm": "Markus Thorne", "cro": "Robert Vance"
    },
    {
        "id": "FAC-LMA-994", "borrower": "Nordic Pharma", "facility": "GBP 150M Capex Facility",
        "exposure": 150000000, "jurisdiction": "UK (LMA)", "obligation": "Compliance Certificate",
        "deadline": (datetime.now() + timedelta(days=15)).strftime('%Y-%m-%d'),
        "status": "Submitted", "rm": "James Chen", "cro": "Sarah Jenkins"
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
    return {"level": "MONITOR", "path": "Agency Ops", "action": "Routine Tracking"}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    # Logic Check: Aggregating Exposure for Commercial Viability
    crit_val = sum(l['exposure'] for l in portfolio_data if analyze_risk(l)['level'] == "CRITICAL")
    for loan in portfolio_data:
        loan['risk'] = analyze_risk(loan)
    return render_template('app.html', portfolio=portfolio_data, crit_val=crit_val)

@app.route('/help')
def help():
    return render_template('help.html')

if __name__ == '__main__':
    app.run(debug=True)
