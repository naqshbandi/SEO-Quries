import os
import sqlite3
from datetime import datetime
from flask import Flask, render_template_string, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'super_secure_commercial_key_786')

# Database Initialization for 1-Year & Full Query Tracking
def init_db():
    conn = sqlite3.connect('advanced_query_journey.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_query_journeys (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            search_date TEXT,
            region TEXT,
            niche TEXT,
            user_session_id TEXT,
            initial_master_query TEXT,
            refined_full_query TEXT,
            time_gap_seconds INTEGER,
            timestamp DATETIME
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Simple Authentication Credentials (Can be moved to Environment Variables)
ACCESS_PASSWORD = os.environ.get('TOOL_PASSWORD', 'admin123')

# HTML & Frontend Design with Smart Niche Input and Login Wall
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SEO Query Journey SaaS - Intelligence Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f4f7f6; margin: 0; padding: 20px; color: #333; }
        .container { max-width: 900px; margin: 0 auto; background: #fff; padding: 30px; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
        h1 { color: #2c3e50; text-align: center; }
        .login-box, .dashboard { margin-top: 20px; }
        input, select, button { width: 100%; padding: 12px; margin: 10px 0; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box; }
        button { background-color: #27ae60; color: white; font-weight: bold; border: none; cursor: pointer; }
        button:hover { background-color: #219653; }
        .logout { background-color: #c0392b; width: auto; padding: 8px 15px; float: right; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { border: 1px solid #ddd; padding: 10px; text-align: left; }
        th { background-color: #2c3e50; color: white; }
    </style>
</head>
<body>
<div class="container">
    {% if not session.get('logged_in') %}
        <h1>SaaS Restricted Access</h1>
        <p style="text-align: center;">Please enter your commercial license password to access the SEO intelligence dashboard.</p>
        <form method="POST" action="/login" class="login-box">
            <input type="password" name="password" placeholder="Enter Access Password" required>
            <button type="submit">Unlock Dashboard</button>
        </form>
    {% else %}
        <form action="/logout" method="POST" style="margin:0;"><button type="submit" class="logout">Logout</button></form>
        <h1>SEO Query Journey Intelligence</h1>
        <p>Explore high-value genuine user search refinements across any custom region and niche.</p>
        
        <div class="dashboard">
            <form method="POST" action="/search">
                <label>Select Region:</label>
                <select name="region">
                    <option value="Europe / UK">Europe / UK</option>
                    <option value="North America">North America</option>
                    <option value="Global / International">Global / International</option>
                </select>

                <label>Target Niche (Select or type your custom niche):</label>
                <input type="text" name="niche" list="niche_suggestions" placeholder="e.g., European Finance, Crypto Trading, Lawn Apparel, etc." required>
                <datalist id="niche_suggestions">
                    <option value="European Finance">
                    <option value="Crypto Trading">
                    <option value="Forex Commodities">
                    <option value="Digital Marketing SaaS">
                    <option value="Ladies Fashion Apparel">
                </datalist>

                <button type="submit">Fetch Genuine Search Intelligence</button>
            </form>

            {% if results is not none %}
                <h3>Intelligence Results for Niche: {{ selected_niche }} (Region: {{ selected_region }})</h3>
                <table>
                    <tr>
                        <th>Initial Master Query</th>
                        <th>Refined Full Query</th>
                        <th>Time Gap (Sec)</th>
                        <th>Date</th>
                    </tr>
                    {% for row in results %}
                    <tr>
                        <td>{{ row[1] }}</td>
                        <td><b>{{ row[2] }}</b></td>
                        <td>{{ row[3] }}s</td>
                        <td>{{ row[4] }}</td>
                    </tr>
                    {% else %}
                    <tr>
                        <td colspan="4" style="text-align:center;">No recent data found for this custom niche. Try adding search tracking logs.</td>
                    </tr>
                    {% endfor %}
                </table>
            {% endif %}
        </div>
    {% endif %}
</div>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, results=None)

@app.route('/login', methods=['POST'])
def login():
    if request.form.get('password') == ACCESS_PASSWORD:
        session['logged_in'] = True
    return redirect(url_for('index'))

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))

@app.route('/search', methods=['POST'])
def search():
    if not session.get('logged_in'):
        return redirect(url_for('index'))
    
    region = request.form.get('region')
    niche = request.form.get('niche')
    
    conn = sqlite3.connect('advanced_query_journey.db')
    cursor = conn.cursor()
    # Fetching data matching user custom niche & region
    cursor.execute('''
        SELECT initial_master_query, refined_full_query, time_gap_seconds, search_date 
        FROM user_query_journeys 
        WHERE region = ? AND niche LIKE ? 
        ORDER BY timestamp DESC LIMIT 20
    ''', (region, f"%{niche}%"))
    results = cursor.fetchall()
    conn.close()
    
    return render_template_string(HTML_TEMPLATE, results=results, selected_niche=niche, selected_region=region)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
