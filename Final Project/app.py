import os
from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user
import sqlite3
import datetime
import random

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Replace with a secure key
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Mock user class
class User(UserMixin):
    def __init__(self, id, role):
        self.id = id
        self.role = role

@login_manager.user_loader
def load_user(user_id):
    return User(user_id, "technician")  # Mock role

# Get absolute path for SQLite database
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'tickets.db')

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tickets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                issue TEXT,
                severity TEXT,
                description TEXT,
                client TEXT,
                timestamp TEXT,
                assigned_to TEXT,
                status TEXT,
                resolved_at TEXT,
                resolution_time TEXT
            )
        ''')
        conn.commit()

# Generate mock incidents (unchanged)
def generate_mock_incident():
    severity_levels = ["Low", "Medium", "High", "Critical"]
    issues = ["Server Down", "Network Latency", "Disk Space Low", "CPU Overload"]
    clients = ["Client A", "Client B", "Client C"]
    return {
        "issue": random.choice(issues),
        "severity": random.choice(severity_levels),
        "description": f"{random.choice(issues)} detected on system.",
        "client": random.choice(clients),
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "assigned_to": "Tech" + str(random.randint(1, 5)),
        "status": "Open",
        "resolved_at": None,
        "resolution_time": None
    }

# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        # Mock login (replace with real auth in production)
        user = User("tech1", "technician")
        login_user(user)
        return redirect(url_for('dashboard'))
    return render_template('login.html')

# Dashboard (protected)
@app.route('/')
@login_required
def dashboard():
    with sqlite3.connect('tickets.db') as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tickets')
        tickets = [dict(row) for row in cursor.fetchall()]
    return render_template('dashboard.html', tickets=tickets)

# API endpoints (unchanged from SQLite version, but protected)
@app.route('/api/tickets', methods=['GET'])
@login_required
def get_tickets():
    with sqlite3.connect('tickets.db') as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tickets')
        tickets = [dict(row) for row in cursor.fetchall()]
    return jsonify(tickets)

@app.route('/api/new_incident', methods=['POST'])
@login_required
def new_incident():
    ticket = generate_mock_incident()
    with sqlite3.connect('tickets.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO tickets (issue, severity, description, client, timestamp, assigned_to, status, resolved_at, resolution_time)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (ticket['issue'], ticket['severity'], ticket['description'], ticket['client'],
              ticket['timestamp'], ticket['assigned_to'], ticket['status'], ticket['resolved_at'], ticket['resolution_time']))
        conn.commit()
        ticket['id'] = cursor.lastrowid
    print(f"ALERT: New {ticket['severity']} incident - {ticket['issue']}")
    return jsonify({"status": "success", "ticket": ticket})

@app.route('/api/update_ticket/<int:ticket_id>', methods=['POST'])
@login_required
def update_ticket(ticket_id):
    with sqlite3.connect('tickets.db') as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tickets WHERE id = ?', (ticket_id,))
        ticket = cursor.fetchone()
        if ticket:
            ticket = dict(ticket)
            new_status = request.json.get('status', 'Resolved')
            resolved_at = ticket['resolved_at']
            resolution_time = ticket['resolution_time']
            if new_status == 'Resolved' and not resolved_at:
                resolved_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                timestamp_dt = datetime.datetime.strptime(ticket['timestamp'], "%Y-%m-%d %H:%M:%S")
                resolved_at_dt = datetime.datetime.now()
                duration = resolved_at_dt - timestamp_dt
                resolution_time = str(duration)
            cursor.execute('''
                UPDATE tickets SET status = ?, resolved_at = ?, resolution_time = ?
                WHERE id = ?
            ''', (new_status, resolved_at, resolution_time, ticket_id))
            conn.commit()
            ticket.update({'status': new_status, 'resolved_at': resolved_at, 'resolution_time': resolution_time})
            return jsonify({"status": "success", "ticket": ticket})
    return jsonify({"status": "error", "message": "Ticket not found"}), 404

if __name__ == '__main__':
    init_db()
    for _ in range(3):
        ticket = generate_mock_incident()
        with sqlite3.connect('tickets.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO tickets (issue, severity, description, client, timestamp, assigned_to, status, resolved_at, resolution_time)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (ticket['issue'], ticket['severity'], ticket['description'], ticket['client'],
                  ticket['timestamp'], ticket['assigned_to'], ticket['status'], ticket['resolved_at'], ticket['resolution_time']))
            conn.commit()
    app.run(debug=True)