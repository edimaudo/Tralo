from flask import Flask, render_template, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)

# Expanded Portfolio with deep-dive metadata
portfolio_data = [
    {
        "id": "FAC-882", "borrower": "Global Logistics S.A.", "facility": "EUR 500M Revolver",
        "exposure": 500000000, "jurisdiction": "UK", "obligation": "Quarterly Financial Statements",
        "deadline": (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d'),
        "status": "Overdue", "rm": "Alice Sterling", "cro": "Robert Vance",
        "margin": "3.50%", "sector": "Logistics", "covenant_summary": "Net Debt/EBITDA < 3.0x; Interest Cover > 4.0x"
    },
    {
        "id": "FAC-110", "borrower": "Titan Energy Corp", "facility": "USD 1.2B Term Loan B",
        "exposure": 1200000000, "jurisdiction": "US", "obligation": "Asset Disposal Notice",
        "deadline": (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d'),
        "status": "Pending", "rm": "Markus Thorne", "cro": "Robert Vance",
        "margin": "4.25%", "sector": "Energy", "covenant_summary": "Minimum Liquidity $50M; Senior Leverage < 2.5x"
    },
    {
        "id": "FAC-994", "borrower": "Nordic Pharma", "facility": "GBP 150M Capex Facility",
        "exposure": 150000000, "jurisdiction": "UK", "obligation": "Compliance Certificate",
        "deadline": (datetime.now() + timedelta(days=15)).strftime('%Y-%m-%d'),
        "status": "Submitted", "rm": "James Chen", "cro": "Sarah Jenkins",
        "margin": "2.75%", "sector": "Healthcare", "covenant_summary": "Clean Down Period: 15 Days; R&D Spend > 10%"
    }
]

def analyze_risk(loan):
    deadline = datetime.strptime(loan['deadline'], '%Y-%m-%d')
    days_left = (deadline - datetime.now()).days
    if loan['status'] == "Overdue":
        return {"level": "CRITICAL", "path": f"{loan['cro']} (CRO)", "action": "Escalate to Credit Committee"}
    elif days_left <= 2:
        return {"level": "HIGH", "path": f"{loan['rm']} (RM)", "action": "Issue Formal Warning"}
    return {"level": "STABLE", "path": "Internal Review", "action": "Log Compliance"}

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
    
    # Pre-formatting currency to fix the rendering bug
    formatted_crit = "{:,.0f}".format(total_crit)
    return render_template('app.html', portfolio=portfolio_data, crit_val=formatted_crit)

@app.route('/help')
def help():
    return render_template('help.html')

if __name__ == '__main__':
    app.run(debug=True)
