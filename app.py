from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
import os
import json
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

# Robust secret key handling for Vercel
secret_key = os.environ.get('SECRET_KEY', 'msukwini-portfolio-secret-2024-student-project')
app.secret_key = secret_key

# ===== PORTFOLIO DATA - UPDATE THIS WITH YOUR INFO! =====
portfolio_data = {
    "name": "Msukwini",
    "title": "Student Developer",
    "about": "I'm a passionate student developer learning web development and building cool projects. Currently exploring Python, Flask, and web technologies!",
    "skills": ["Python", "Flask", "HTML/CSS", "JavaScript", "Git", "SQL"],
    "projects": [
        {
            "name": "Personal Portfolio",
            "description": "A responsive portfolio website built with Flask and deployed on Vercel",
            "tech": ["Python", "Flask", "HTML", "CSS", "Vercel"]
        },
        {
            "name": "Task Manager App",
            "description": "A simple web application for managing daily tasks and to-do lists",
            "tech": ["Python", "Flask", "SQLite", "Bootstrap"]
        }
    ],
    "contact": {
        "email": "your-email@student.com",  # Update with your email
        "github": "https://github.com/Msukwini",
        "linkedin": "https://linkedin.com/in/your-profile"  # Update if available
    }
}

# ===== MESSAGE STORAGE SOLUTION FOR VERCEL =====
# In Vercel, we can't write to files, so we'll use a simple in-memory store
# Note: This resets when the serverless function restarts (normal for Vercel)

# Simple in-memory message store
messages_store = []

def save_message(name, email, message):
    """Save message to in-memory store (works on Vercel)"""
    try:
        new_message = {
            'id': len(messages_store) + 1,
            'name': name.strip(),
            'email': email.strip().lower(),
            'message': message.strip(),
            'timestamp': datetime.now().isoformat(),
            'read': False
        }
        
        messages_store.append(new_message)
        
        # Log the message (visible in Vercel logs)
        print(f"📧 NEW MESSAGE: From {name} ({email})")
        print(f"💬 Message: {message[:100]}...")  # First 100 chars
        
        return True
        
    except Exception as e:
        print(f"❌ Error saving message: {e}")
        return False

def get_messages_count():
    """Get total number of messages received"""
    return len(messages_store)

def send_email_notification(name, email, message):
    """Send email notification when someone submits the contact form"""
    try:
        # This is optional - you can set up email later
        # For now, we'll just log it
        print(f"📧 EMAIL NOTIFICATION WOULD BE SENT:")
        print(f"   From: {name} <{email}>")
        print(f"   Message: {message}")
        return True
    except Exception as e:
        print(f"Email notification error: {e}")
        return False

# ===== ROUTES =====
@app.route('/')
def index():
    """Home page with portfolio information"""
    message_count = get_messages_count()
    return render_template('index.html', 
                         data=portfolio_data, 
                         message_count=message_count)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact form page"""
    if request.method == 'POST':
        # Get form data
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        message = request.form.get('message', '').strip()
        
        # Validation
        if not name or not email or not message:
            flash('❌ Please fill in all fields', 'error')
        elif len(name) < 2:
            flash('❌ Name should be at least 2 characters long', 'error')
        elif len(message) < 10:
            flash('❌ Message should be at least 10 characters long', 'error')
        elif '@' not in email or '.' not in email:
            flash('❌ Please enter a valid email address', 'error')
        else:
            # Save message
            if save_message(name, email, message):
                # Optional: Send email notification
                send_email_notification(name, email, message)
                flash('✅ Message sent successfully! I\'ll get back to you soon.', 'success')
            else:
                flash('❌ Sorry, there was an error sending your message. Please try again.', 'error')
            
            return redirect(url_for('contact'))
    
    return render_template('contact.html', data=portfolio_data)

@app.route('/about')
def about():
    """About page"""
    return render_template('about.html', data=portfolio_data)

# ===== API ROUTES =====
@app.route('/api/messages/count')
def api_message_count():
    """API endpoint to get message count"""
    count = get_messages_count()
    return jsonify({'count': count})

@app.route('/api/health')
def health_check():
    """Health check endpoint for deployment"""
    return jsonify({
        'status': 'healthy', 
        'service': 'Portfolio API',
        'timestamp': datetime.now().isoformat(),
        'message_count': get_messages_count(),
        'environment': 'Vercel Serverless'
    })

@app.route('/api/portfolio')
def api_portfolio():
    """API endpoint to get portfolio data"""
    return jsonify(portfolio_data)

# ===== ERROR HANDLERS =====
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', data=portfolio_data), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html', data=portfolio_data), 500

# ===== MAIN APPLICATION =====
if __name__ == '__main__':
    # Run the application
    print("🎉 Portfolio application starting...")
    print("💡 Using in-memory message storage (Vercel compatible)")
    print("🌐 Server will run on: http://127.0.0.1:5000")
    print("📧 Messages will be logged to console and stored in memory")
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )