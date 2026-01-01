from flask import Flask, render_template, url_for
from datetime import datetime, timedelta

app = Flask(__name__)

portfolio_data = [
    {
        "id": "FAC-882", "borrower": "Global Logistics S.A.", "facility": "EUR 500M Revolver",
        "exposure": 500000000, "jurisdiction": "UK", "obligation": "Quarterly Financial Statements",
        "deadline": (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d'),
        "status": "Overdue", "rm": "Alice Sterling", "cro": "Robert Vance",
        "margin": "3.50%", "sector": "Logistics", "provision_summary": "Net Debt/EBITDA < 3.0x; Interest Cover > 4.0x"
    },
    {
        "id": "FAC-110", "borrower": "Titan Energy Corp", "facility": "USD 1.2B Term Loan B",
        "exposure": 1200000000, "jurisdiction": "US", "obligation": "Asset Disposal Notice",
        "deadline": (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d'),
        "status": "Pending", "rm": "Markus Thorne", "cro": "Robert Vance",
        "margin": "4.25%", "sector": "Energy", "provision_summary": "Min Liquidity $50M; Senior Leverage < 2.5x"
    },
    {
        "id": "FAC-994", "borrower": "Nordic Pharma", "facility": "GBP 150M Capex Facility",
        "exposure": 150000000, "jurisdiction": "UK", "obligation": "Compliance Certificate",
        "deadline": (datetime.now() + timedelta(days=15)).strftime('%Y-%m-%d'),
        "status": "Submitted", "rm": "James Chen", "cro": "Sarah Jenkins",
        "margin": "2.75%", "sector": "Healthcare", "provision_summary": "Clean Down Period: 15 Days; R&D Spend > 10%"
    },
    {
        "id": "FAC-442", "borrower": "CloudScale Systems", "facility": "USD 200M Venture Debt",
        "exposure": 200000000, "jurisdiction": "US", "obligation": "Series D Funding Proof",
        "deadline": (datetime.now() - timedelta(days=5)).strftime('%Y-%m-%d'),
        "status": "Overdue", "rm": "Markus Thorne", "cro": "Sarah Jenkins",
        "margin": "6.50%", "sector": "Technology", "provision_summary": "Runway > 12 Months; Minimum ARR $100M"
    },
    {
        "id": "FAC-205", "borrower": "EuroRetail Holdings", "facility": "EUR 300M Inventory Line",
        "exposure": 300000000, "jurisdiction": "Germany", "obligation": "Inventory Valuation Report",
        "deadline": (datetime.now() + timedelta(days=20)).strftime('%Y-%m-%d'),
        "status": "Submitted", "rm": "James Chen", "cro": "Robert Vance",
        "margin": "2.10%", "sector": "Retail", "provision_summary": "Max Leverage 3.5x; No Change of Control"
    },
    {
        "id": "FAC-771", "borrower": "Sterling Property REIT", "facility": "GBP 850M Dev Finance",
        "exposure": 850000000, "jurisdiction": "UK", "obligation": "LTV Certificate",
        "deadline": (datetime.now() + timedelta(hours=12)).strftime('%Y-%m-%d'),
        "status": "Pending", "rm": "Alice Sterling", "cro": "Sarah Jenkins",
        "margin": "3.80%", "sector": "Real Estate", "provision_summary": "LTV < 65%; Interest Reserve 12 Months"
    },
    {
        "id": "FAC-339", "borrower": "Apex Mining Group", "facility": "AUD 750M Bridge Loan",
        "exposure": 750000000, "jurisdiction": "Australia", "obligation": "Environmental Impact Audit",
        "deadline": (datetime.now() + timedelta(days=3)).strftime('%Y-%m-%d'),
        "status": "Pending", "rm": "Markus Thorne", "cro": "Robert Vance",
        "margin": "5.25%", "sector": "Mining", "provision_summary": "Capex Sweep 50%; Min Ore Reserve 2M Tons"
    }
]

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
