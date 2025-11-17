from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
import os
import requests
from datetime import datetime

app = Flask(__name__)
secret_key = os.environ.get('SECRET_KEY', 'msukwini-portfolio-secret-2024-student-project')
app.secret_key = secret_key

# ===== PORTFOLIO DATA =====
portfolio_data = {
    "name": "Msukwini",
    "title": "Student Developer", 
    "about": "I'm a passionate student developer learning web development and building cool projects.",
    "skills": ["Python", "Flask", "HTML/CSS", "JavaScript", "Git", "SQL"],
    "projects": [
        {
            "name": "Personal Portfolio",
            "description": "A responsive portfolio website built with Flask and deployed on Vercel",
            "tech": ["Python", "Flask", "HTML", "CSS", "Vercel"]
        }
    ],
    "contact": {
        "email": "lwzimsukwini@gmail.com",
        "github": "https://github.com/Msukwini",
        "linkedin": "https://linkedin.com/in/your-profile"
    }
}

# ===== MESSAGE STORAGE =====
messages_store = []

def log_message_to_console(name, email, message):
    """Log message clearly to Vercel console"""
    try:
        print("🚨" * 20)
        print("🚨 IMPORTANT: NEW PORTFOLIO MESSAGE")
        print("🚨" * 20)
        print(f"👤 NAME: {name}")
        print(f"📧 EMAIL: {email}")
        print(f"💬 MESSAGE: {message}")
        print(f"⏰ TIME: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("🚨" * 20)
        print("💡 Check Vercel logs to see this message!")
        print("🚨" * 20)
        return True
    except Exception as e:
        print(f"❌ Error logging message: {e}")
        return False

def save_message(name, email, message):
    """Save message and log it clearly"""
    try:
        new_message = {
            'id': len(messages_store) + 1,
            'name': name.strip(),
            'email': email.strip().lower(),
            'message': message.strip(),
            'timestamp': datetime.now().isoformat(),
        }
        
        messages_store.append(new_message)
        
        # Log message clearly to console
        log_message_to_console(name, email, message)
        
        return True
        
    except Exception as e:
        print(f"❌ Error saving message: {e}")
        return False

def get_messages_count():
    return len(messages_store)

# ===== ROUTES =====
@app.route('/')
def index():
    message_count = get_messages_count()
    return render_template('index.html', data=portfolio_data, message_count=message_count)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        message = request.form.get('message', '').strip()
        
        if not name or not email or not message:
            flash('❌ Please fill in all fields', 'error')
        elif len(name) < 2:
            flash('❌ Name should be at least 2 characters long', 'error')
        elif len(message) < 10:
            flash('❌ Message should be at least 10 characters long', 'error')
        elif '@' not in email or '.' not in email:
            flash('❌ Please enter a valid email address', 'error')
        else:
            if save_message(name, email, message):
                flash('✅ Message sent successfully! I\'ll check my logs and get back to you soon.', 'success')
            else:
                flash('❌ Sorry, there was an error. Please try again.', 'error')
            return redirect(url_for('contact'))
    
    return render_template('contact.html', data=portfolio_data)

@app.route('/about')
def about():
    return render_template('about.html', data=portfolio_data)

@app.route('/api/messages')
def api_messages():
    """API to see recent messages (for debugging)"""
    return jsonify({
        'count': len(messages_store),
        'messages': messages_store[-5:]  # Last 5 messages
    })

@app.route('/api/health')
def health_check():
    return jsonify({
        'status': 'healthy', 
        'message_count': get_messages_count(),
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    print("🎉 Portfolio starting...")
    print("📧 Messages will be logged to console")
    print("🔍 Check Vercel logs to see messages!")
    app.run(host='0.0.0.0', port=5000, debug=True)