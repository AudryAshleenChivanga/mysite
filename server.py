#!/usr/bin/env python3
"""
Mission Portfolio Server with Admin Interface
Run with: python server.py
"""

from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import json
import os
from datetime import datetime
import secrets
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  # Generate a random secret key

# Configuration
ADMIN_USERNAME = "audry"  # Change this to your preferred username
ADMIN_PASSWORD = "healthcare2025"  # Change this to a secure password
DATA_FILE = "portfolio_data.json"

# Email Configuration
RECIPIENT_EMAIL = "audryashleenchivanga@gmail.com"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USERNAME = "audryashleenchivanga@gmail.com"  # Your Gmail address
SMTP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD", "")  # Use App Password from environment variable

def load_data():
    """Load portfolio data from JSON file"""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            pass
    
    # Default data structure with your actual data
    return {
        "personal": {
            "name": "Audry Ashleen Chivanga",
            "email": "audryashleenchivanga@gmail.com",
            "linkedin": "https://www.linkedin.com/in/audry-ashleen-chivanga-081175231/",
            "github": "https://github.com/AudryAshleenChivanga",
            "program": "BSE (Bachelor of Software Engineering)"
        },
        "mission": {
            "pathways": ["Healthcare", "Women Empowerment"],
            "statement": "My mission is to harness technology to transform traditional healthcare systems across Africa by addressing critical challenges such as diagnostic inefficiencies, delays in service delivery, and gaps in women's health. I aim to build digital platforms that enhance patient outcomes and make healthcare more accessible, efficient, and equitable.",
            "narrative": "In many African healthcare systems, the burden of long wait times and inefficiencies in service delivery is more than just an inconvenience—it is a threat to lives. I remember sitting in a hospital waiting room for over five hours, watching patients, many elderly and some in visible pain, wait endlessly just to be seen by a doctor. That experience led me to build Mediqueueless, a digital solution aimed at eliminating waiting queues by automating patient intake and triage, making healthcare access faster and more dignified."
        },
        "experience": [],
        "projects": [
            {
                "id": 1,
                "name": "Mediqueueless",
                "description": "Digital solution aimed at eliminating waiting queues by automating patient intake and triage, making healthcare access faster and more dignified.",
                "tags": ["Healthcare Tech", "Queue Management", "Patient Care"],
                "featured": True,
                "award": "",
                "url": ""
            },
            {
                "id": 2,
                "name": "AshleTech Connect SRHR",
                "description": "Digital outreach initiative that won the 2024 Project Award for its impact in educating young women on menstrual and sexual health.",
                "tags": ["Women's Health", "SRHR Education", "Digital Platform"],
                "featured": True,
                "award": "2024 Project Award Winner",
                "url": ""
            }
        ]
    }

def save_data(data):
    """Save portfolio data to JSON file"""
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving data: {e}")
        return False

# Routes
@app.route('/')
def home():
    """Serve the main portfolio website"""
    try:
        with open('index.html', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return "<h1>Portfolio website not found</h1><p>Please check if index.html exists.</p>", 404

@app.route('/styles.css')
def styles():
    """Serve CSS file"""
    try:
        with open('styles.css', 'r', encoding='utf-8') as f:
            response = app.response_class(
                response=f.read(),
                status=200,
                mimetype='text/css'
            )
            return response
    except FileNotFoundError:
        return "CSS file not found", 404

@app.route('/script.js')
def scripts():
    """Serve JavaScript file"""
    try:
        with open('script.js', 'r', encoding='utf-8') as f:
            response = app.response_class(
                response=f.read(),
                status=200,
                mimetype='application/javascript'
            )
            return response
    except FileNotFoundError:
        return "JavaScript file not found", 404

@app.route('/images/<path:filename>')
def serve_image(filename):
    """Serve image files"""
    from flask import send_from_directory
    return send_from_directory('images', filename)

@app.route('/admin')
def admin_dashboard():
    """Admin dashboard - requires authentication"""
    if 'authenticated' not in session:
        return redirect(url_for('admin_login'))
    
    data = load_data()
    # Simple HTML dashboard if template not found
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Admin Dashboard - Mission Portfolio</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
        <style>
            body {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }}
            .admin-card {{ background: white; border-radius: 15px; box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1); }}
            .header-gradient {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }}
        </style>
    </head>
    <body>
        <div class="container mt-4">
            <div class="admin-card">
                <div class="header-gradient p-4 rounded-top">
                    <div class="d-flex justify-content-between align-items-center">
                        <div>
                            <h1><i class="fas fa-user-cog"></i> Mission Portfolio Admin</h1>
                            <p class="mb-0">Manage your healthcare innovation portfolio</p>
                        </div>
                        <div>
                            <span class="me-3">Welcome, {session.get('username')}!</span>
                            <a href="/admin/logout" class="btn btn-outline-light">
                                <i class="fas fa-sign-out-alt"></i> Logout
                            </a>
                        </div>
                    </div>
                </div>
                <div class="p-4">
                    <div class="alert alert-success">
                        <i class="fas fa-check-circle"></i>
                        Successfully logged in! Your mission portfolio admin panel is ready.
                    </div>
                    
                    <div class="row mb-4">
                        <div class="col-md-3">
                            <div class="card text-center">
                                <div class="card-body">
                                    <i class="fas fa-rocket fa-2x text-primary mb-2"></i>
                                    <h5>{len(data.get('projects', []))}</h5>
                                    <p class="text-muted">Projects</p>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-3">
                            <div class="card text-center">
                                <div class="card-body">
                                    <i class="fas fa-briefcase fa-2x text-success mb-2"></i>
                                    <h5>{len(data.get('experience', []))}</h5>
                                    <p class="text-muted">Experience</p>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-3">
                            <div class="card text-center">
                                <div class="card-body">
                                    <i class="fas fa-bullseye fa-2x text-warning mb-2"></i>
                                    <h5>{len(data.get('mission', {}).get('pathways', []))}</h5>
                                    <p class="text-muted">Mission Pathways</p>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-3">
                            <div class="card text-center">
                                <div class="card-body">
                                    <i class="fas fa-user fa-2x text-info mb-2"></i>
                                    <h5>Ready</h5>
                                    <p class="text-muted">Personal Info</p>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="row">
                        <div class="col-md-6">
                            <div class="card">
                                <div class="card-header bg-light">
                                    <h5><i class="fas fa-tachometer-alt"></i> Quick Actions</h5>
                                </div>
                                <div class="card-body">
                                    <div class="d-grid gap-2">
                                        <a href="/admin/projects" class="btn btn-primary">
                                            <i class="fas fa-rocket"></i> Manage Projects
                                        </a>
                                        <a href="/admin/experience" class="btn btn-success">
                                            <i class="fas fa-briefcase"></i> Manage Experience
                                        </a>
                                        <a href="/admin/personal" class="btn btn-info">
                                            <i class="fas fa-user"></i> Update Personal Info
                                        </a>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="card">
                                <div class="card-header bg-light">
                                    <h5><i class="fas fa-star"></i> Featured Projects</h5>
                                </div>
                                <div class="card-body">
                                    {"".join([f'<div class="mb-2"><strong>{p["name"]}</strong>' + ('<span class="badge bg-warning ms-2">Featured</span>' if p.get("featured") else '') + f'<br><small class="text-muted">{p["description"][:60]}...</small></div>' for p in data.get('projects', [])[:3]])}
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="row mt-4">
                        <div class="col-12">
                            <div class="card border-success">
                                <div class="card-header bg-success text-white">
                                    <h5 class="mb-0"><i class="fas fa-external-link-alt"></i> Portfolio Actions</h5>
                                </div>
                                <div class="card-body">
                                    <div class="row">
                                        <div class="col-md-6">
                                            <a href="/" target="_blank" class="btn btn-success btn-lg w-100">
                                                <i class="fas fa-eye"></i> View Live Portfolio
                                            </a>
                                        </div>
                                        <div class="col-md-6">
                                            <a href="/admin/backup" class="btn btn-warning btn-lg w-100">
                                                <i class="fas fa-download"></i> Download Backup
                                            </a>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    return html

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Admin login page"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['authenticated'] = True
            session['username'] = username
            return redirect(url_for('admin_dashboard'))
        else:
            error = "Invalid credentials"
    else:
        error = None
    
    # Simple login form
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Admin Login - Mission Portfolio</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
        <style>
            body {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; display: flex; align-items: center; }}
            .login-card {{ background: white; border-radius: 15px; box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1); }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="row justify-content-center">
                <div class="col-md-4">
                    <div class="card login-card">
                        <div class="card-body p-5">
                            <div class="text-center mb-4">
                                <i class="fas fa-shield-alt fa-3x text-primary mb-3"></i>
                                <h3>Welcome Back, Audry!</h3>
                                <p class="text-muted">Enter your credentials to manage your mission portfolio</p>
                            </div>
                            {'<div class="alert alert-danger"><i class="fas fa-exclamation-triangle"></i> ' + error + '</div>' if error else ''}
                            <form method="POST">
                                <div class="mb-3">
                                    <label class="form-label"><i class="fas fa-user"></i> Username</label>
                                    <input type="text" class="form-control form-control-lg" name="username" required>
                                </div>
                                <div class="mb-4">
                                    <label class="form-label"><i class="fas fa-lock"></i> Password</label>
                                    <input type="password" class="form-control form-control-lg" name="password" required>
                                </div>
                                <button type="submit" class="btn btn-primary btn-lg w-100">
                                    <i class="fas fa-sign-in-alt"></i> Login to Admin Panel
                                </button>
                            </form>
                            <hr>
                            <div class="text-center">
                                <small class="text-muted">
                                    <strong>Demo Credentials:</strong><br>
                                    Username: <code>audry</code><br>
                                    Password: <code>healthcare2025</code>
                                </small>
                                <br><br>
                                <a href="/" class="text-decoration-none">
                                    <i class="fas fa-arrow-left"></i> Back to Portfolio
                                </a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    return html

@app.route('/admin/logout')
def admin_logout():
    """Admin logout"""
    session.clear()
    return redirect(url_for('home'))

@app.route('/admin/projects')
def admin_projects():
    """Simple projects management"""
    if 'authenticated' not in session:
        return redirect(url_for('admin_login'))
    
    data = load_data()
    projects = data.get('projects', [])
    
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Projects Management</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
        <style>
            body { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }
            .admin-card { background: white; border-radius: 15px; box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1); }
        </style>
    </head>
    <body>
        <div class="container mt-4">
            <div class="admin-card p-4">
                <h2><i class="fas fa-rocket"></i> Projects Management</h2>
                <a href="/admin" class="btn btn-secondary mb-3"><i class="fas fa-arrow-left"></i> Back to Dashboard</a>
                
                <div class="row">
    """
    
    for project in projects:
        featured_badge = '<span class="badge bg-warning text-dark"><i class="fas fa-star"></i> Featured</span>' if project.get('featured') else ''
        award_badge = f'<span class="badge bg-success">{project["award"]}</span>' if project.get('award') else ''
        
        html += f"""
                    <div class="col-md-6 mb-3">
                        <div class="card h-100">
                            <div class="card-body">
                                <h5 class="card-title">{project['name']}</h5>
                                <div class="mb-2">{featured_badge} {award_badge}</div>
                                <p class="card-text">{project['description'][:150]}...</p>
                                <div class="mb-2">
                                    {''.join([f'<span class="badge bg-light text-dark me-1">{tag}</span>' for tag in project.get('tags', [])])}
                                </div>
                                {'<a href="' + project.get('url', '#') + '" target="_blank" class="btn btn-sm btn-outline-primary"><i class="fas fa-external-link-alt"></i> View Project</a>' if project.get('url') else ''}
                            </div>
                        </div>
                    </div>
        """
    
    if not projects:
        html += """
                    <div class="col-12">
                        <div class="alert alert-info text-center">
                            <i class="fas fa-info-circle fa-2x mb-3"></i>
                            <h5>No projects yet!</h5>
                            <p>Projects will appear here when you add them. The full admin interface includes forms to add, edit, and manage all your projects.</p>
                        </div>
                    </div>
        """
    
    html += """
                </div>
                <div class="alert alert-info mt-4">
                    <i class="fas fa-lightbulb"></i>
                    <strong>Enhanced Features:</strong> The complete admin interface includes forms to add new projects, edit existing ones, manage tags, and upload project images.
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    return html

@app.route('/admin/personal')
def admin_personal():
    """Simple personal info display"""
    if 'authenticated' not in session:
        return redirect(url_for('admin_login'))
    
    data = load_data()
    personal = data.get('personal', {})
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Personal Information</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
        <style>
            body {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }}
            .admin-card {{ background: white; border-radius: 15px; box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1); }}
        </style>
    </head>
    <body>
        <div class="container mt-4">
            <div class="admin-card p-4">
                <h2><i class="fas fa-user"></i> Personal Information</h2>
                <a href="/admin" class="btn btn-secondary mb-3"><i class="fas fa-arrow-left"></i> Back to Dashboard</a>
                
                <div class="row">
                    <div class="col-md-8">
                        <div class="card">
                            <div class="card-body">
                                <h5>Current Information</h5>
                                <table class="table table-borderless">
                                    <tr>
                                        <td><strong><i class="fas fa-user text-primary"></i> Name:</strong></td>
                                        <td>{personal.get('name', 'Not set')}</td>
                                    </tr>
                                    <tr>
                                        <td><strong><i class="fas fa-envelope text-primary"></i> Email:</strong></td>
                                        <td>{personal.get('email', 'Not set')}</td>
                                    </tr>
                                    <tr>
                                        <td><strong><i class="fas fa-graduation-cap text-primary"></i> Program:</strong></td>
                                        <td>{personal.get('program', 'Not set')}</td>
                                    </tr>
                                    <tr>
                                        <td><strong><i class="fab fa-linkedin text-primary"></i> LinkedIn:</strong></td>
                                        <td><a href="{personal.get('linkedin', '#')}" target="_blank">View Profile</a></td>
                                    </tr>
                                    <tr>
                                        <td><strong><i class="fab fa-github text-primary"></i> GitHub:</strong></td>
                                        <td><a href="{personal.get('github', '#')}" target="_blank">View Profile</a></td>
                                    </tr>
                                </table>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="card">
                            <div class="card-body text-center">
                                <i class="fas fa-user-circle fa-5x text-primary mb-3"></i>
                                <h5>{personal.get('name', 'Your Name')}</h5>
                                <p class="text-muted">{personal.get('program', 'Your Program')}</p>
                                <div class="d-flex justify-content-center gap-3">
                                    <a href="{personal.get('email', '#')}" class="text-primary">
                                        <i class="fas fa-envelope fa-lg"></i>
                                    </a>
                                    <a href="{personal.get('linkedin', '#')}" target="_blank" class="text-primary">
                                        <i class="fab fa-linkedin fa-lg"></i>
                                    </a>
                                    <a href="{personal.get('github', '#')}" target="_blank" class="text-primary">
                                        <i class="fab fa-github fa-lg"></i>
                                    </a>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="alert alert-info mt-3">
                    <i class="fas fa-info-circle"></i>
                    <strong>Enhanced Features:</strong> The complete admin interface includes forms to edit all personal information with live preview and validation.
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    return html

@app.route('/admin/experience')
def admin_experience():
    """Simple experience display"""
    if 'authenticated' not in session:
        return redirect(url_for('admin_login'))
    
    data = load_data()
    experiences = data.get('experience', [])
    
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Experience Management</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
        <style>
            body { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }
            .admin-card { background: white; border-radius: 15px; box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1); }
        </style>
    </head>
    <body>
        <div class="container mt-4">
            <div class="admin-card p-4">
                <h2><i class="fas fa-briefcase"></i> Experience Management</h2>
                <a href="/admin" class="btn btn-secondary mb-3"><i class="fas fa-arrow-left"></i> Back to Dashboard</a>
                
    """
    
    if experiences:
        for exp in experiences:
            html += f"""
                <div class="card mb-3">
                    <div class="card-body">
                        <h5>{exp.get('title', 'Position')}</h5>
                        <h6 class="text-muted">{exp.get('organization', 'Organization')}</h6>
                        <p><small><i class="fas fa-calendar"></i> {exp.get('date', 'Date')} | <i class="fas fa-map-marker-alt"></i> {exp.get('location', 'Location')}</small></p>
                        <p>{exp.get('description', 'No description')}</p>
                        <span class="badge bg-primary">{exp.get('type', 'experience').title()}</span>
                    </div>
                </div>
            """
    else:
        html += """
                <div class="alert alert-info text-center">
                    <i class="fas fa-briefcase fa-2x mb-3"></i>
                    <h5>No experience entries yet!</h5>
                    <p>Your conferences, work experience, and volunteer activities will appear here when you add them through the complete admin interface.</p>
                </div>
        """
    
    html += """
                <div class="alert alert-info">
                    <i class="fas fa-plus-circle"></i>
                    <strong>Enhanced Features:</strong> The complete admin interface includes forms to add conferences, work experience, internships, and volunteer activities with detailed categorization.
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    return html

@app.route('/admin/backup')
def admin_backup():
    """Download backup of all data"""
    if 'authenticated' not in session:
        return redirect(url_for('admin_login'))
    
    data = load_data()
    
    from flask import Response
    return Response(
        json.dumps(data, indent=2),
        mimetype='application/json',
        headers={'Content-Disposition': f'attachment; filename=portfolio_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'}
    )

@app.route('/api/data')
def api_data():
    """API endpoint to get all data"""
    return jsonify(load_data())

@app.route('/api/test-email', methods=['GET'])
def test_email_config():
    """Test endpoint to check email configuration"""
    config_status = {
        'smtp_server': SMTP_SERVER,
        'smtp_port': SMTP_PORT,
        'smtp_username': SMTP_USERNAME,
        'recipient_email': RECIPIENT_EMAIL,
        'password_configured': bool(SMTP_PASSWORD),
        'password_length': len(SMTP_PASSWORD) if SMTP_PASSWORD else 0
    }
    
    if SMTP_PASSWORD:
        # Try to connect and authenticate
        try:
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.quit()
            config_status['connection_test'] = 'SUCCESS - Email configuration is working!'
        except Exception as e:
            config_status['connection_test'] = f'FAILED - {str(e)}'
    else:
        config_status['connection_test'] = 'NOT CONFIGURED - Set GMAIL_APP_PASSWORD environment variable'
    
    return jsonify(config_status)

@app.route('/api/contact', methods=['POST'])
def send_contact_email():
    """Handle contact form submissions and send email"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'email', 'subject', 'message']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400
        
        name = data.get('name')
        email = data.get('email')
        subject = data.get('subject')
        message = data.get('message')
        
        # Log the submission
        print("\n" + "="*70)
        print("CONTACT FORM SUBMISSION RECEIVED")
        print("="*70)
        print(f"Name: {name}")
        print(f"Email: {email}")
        print(f"Subject: {subject}")
        print(f"Message: {message[:100]}..." if len(message) > 100 else f"Message: {message}")
        print("="*70 + "\n")
        
        # Create email message
        msg = MIMEMultipart()
        msg['From'] = SMTP_USERNAME
        msg['To'] = RECIPIENT_EMAIL
        msg['Subject'] = f"Portfolio Contact: {subject}"
        msg['Reply-To'] = email
        
        # Email body with HTML formatting
        html_body = f"""
<html>
<head></head>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
        <h2 style="color: #d4a853;">New Message from Portfolio Contact Form</h2>
        <div style="background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0;">
            <p><strong>Name:</strong> {name}</p>
            <p><strong>Email:</strong> <a href="mailto:{email}">{email}</a></p>
            <p><strong>Subject:</strong> {subject}</p>
        </div>
        <div style="margin: 20px 0;">
            <h3>Message:</h3>
            <p style="white-space: pre-wrap;">{message}</p>
        </div>
        <hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;">
        <p style="color: #666; font-size: 12px;">
            This message was sent from your portfolio website.<br>
            Reply directly to this email to respond to {name}.
        </p>
    </div>
</body>
</html>
"""
        
        plain_body = f"""
New message from your portfolio contact form:

Name: {name}
Email: {email}
Subject: {subject}

Message:
{message}

---
This message was sent from your portfolio website.
Reply directly to this email to respond to {name} ({email}).
"""
        
        # Attach both plain text and HTML versions
        msg.attach(MIMEText(plain_body, 'plain'))
        msg.attach(MIMEText(html_body, 'html'))
        
        # Send email
        if SMTP_PASSWORD:
            try:
                print(f"Attempting to send email to {RECIPIENT_EMAIL}...")
                print(f"SMTP Server: {SMTP_SERVER}:{SMTP_PORT}")
                print(f"SMTP Username: {SMTP_USERNAME}")
                
                server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
                server.set_debuglevel(1)  # Enable debug output
                server.starttls()
                
                print("Logging in to SMTP server...")
                server.login(SMTP_USERNAME, SMTP_PASSWORD)
                print("Login successful!")
                
                text = msg.as_string()
                print(f"Sending email to {RECIPIENT_EMAIL}...")
                server.sendmail(SMTP_USERNAME, RECIPIENT_EMAIL, text)
                server.quit()
                
                print("Email sent successfully!")
                
                return jsonify({
                    'success': True,
                    'message': 'Thank you! Your message has been sent successfully. I will get back to you soon!'
                }), 200
                
            except smtplib.SMTPAuthenticationError as e:
                error_msg = f"SMTP Authentication failed. Please check your Gmail App Password."
                print(f"ERROR: {error_msg}")
                print(f"Details: {str(e)}")
                return jsonify({
                    'success': False,
                    'error': error_msg + ' Make sure you\'re using an App Password, not your regular Gmail password.'
                }), 500
                
            except smtplib.SMTPException as e:
                error_msg = f"SMTP error occurred: {str(e)}"
                print(f"ERROR: {error_msg}")
                return jsonify({
                    'success': False,
                    'error': f'Failed to send email. Please try again later. Error: {str(e)}'
                }), 500
                
            except Exception as e:
                error_msg = f"Unexpected error: {str(e)}"
                print(f"ERROR: {error_msg}")
                import traceback
                traceback.print_exc()
                return jsonify({
                    'success': False,
                    'error': f'Failed to send email: {str(e)}'
                }), 500
        else:
            # If no SMTP password configured, log the message (for development)
            print("\n" + "="*70)
            print("⚠️  EMAIL NOT CONFIGURED - Message logged to console only")
            print("="*70)
            print(f"To enable email sending, set GMAIL_APP_PASSWORD environment variable")
            print(f"See EMAIL_SETUP.md for instructions")
            print("="*70 + "\n")
            
            return jsonify({
                'success': True,
                'message': 'Thank you! Your message has been received. (Email sending not configured - check server logs)'
            }), 200
            
    except Exception as e:
        import traceback
        print(f"ERROR in send_contact_email: {str(e)}")
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500

if __name__ == '__main__':
    # Initialize data file if it doesn't exist
    if not os.path.exists(DATA_FILE):
        save_data(load_data())
    
    print("Mission Portfolio Server Starting...")
    print("Website: http://localhost:5000")
    print("Admin Panel: http://localhost:5000/admin")
    print(f"Admin Login: {ADMIN_USERNAME} / {ADMIN_PASSWORD}")
    print("Press Ctrl+C to stop the server")
    print()
    
    app.run(debug=True, host='0.0.0.0', port=5000)
