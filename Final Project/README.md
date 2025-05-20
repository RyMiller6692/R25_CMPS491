# Final Project

Overview
This is a prototype for a Managed Service Provider (MSP) ticketing system that automates incident detection, ticket creation, and resolution tracking. It was developed as part of CMPS 491: System Architecture.
Features

Web dashboard to view and manage IT incident tickets.
SQLite database for persistent ticket storage.
Mock authentication for technician access.
Bar chart displaying ticket severity distribution.
Real-time updates with ticket resolution tracking.

Prerequisites
To run this application locally, you need:

Python 3.6+: Download from https://python.org/ or use Anaconda.
Git: To clone the repository (download from https://git-scm.com/).
Web Browser: Chrome or Firefox recommended.

Setup and Running Instructions
Follow these steps to run the application from GitHub:

Clone the Repository:
git clone https://github.com/your-username/msp-ticketing-system.git
cd msp-ticketing-system

Note: Replace your-username with your actual GitHub username.

Install Dependencies:

Ensure Python is installed (python --version).
Install required Python packages:pip install -r requirements.txt


This installs Flask, Flask-Login, and other dependencies listed in requirements.txt.


Run the Application:
python app.py


This starts the Flask server locally. You should see output like:* Running on http://127.0.0.1:5000 (Press CTRL+C to quit)




Access the Dashboard:

Open your browser and go to: http://127.0.0.1:5000/.
You’ll see a login page. Click Login as Technician (mock authentication for the prototype).
The dashboard displays tickets with details (ID, issue, severity, description, client, timestamp, status, resolution time).
Use the Simulate New Incident button to create new tickets.
Click Resolve on a ticket to update its status and log resolution time.
View the Ticket Severity Distribution chart to see ticket counts by severity.



Project Structure

app.py: Flask backend with API endpoints, database logic, and authentication.
templates/: HTML templates (dashboard.html for the main UI, login.html for the login page).
tickets.db: SQLite database file (generated on first run, stores ticket data).
requirements.txt: Lists Python dependencies.

Troubleshooting

Python Not Found:
Ensure Python is installed and added to your PATH. Use python3 app.py if python doesn’t work.


Dependencies Fail to Install:
Verify pip is installed (pip --version). Use pip3 if needed.
Run pip install flask flask-login manually if requirements.txt fails.


Port Conflict:
If port 5000 is in use, edit app.py to change the port (e.g., app.run(host='0.0.0.0', port=5001)), then access http://127.0.0.1:5001/.


Database Issues:
If tickets.db is missing or corrupted, delete it and re-run python app.py to recreate it with initial tickets.



Last Updated
These instructions were last updated at 10:15 PM PDT on Monday, May 19, 2025.
