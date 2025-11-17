from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
import os
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-' + str(os.urandom(16)))

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

# ===== CONFIGURATION =====
MESSAGES_FILE = 'messages.json'

def init_messages_file():
    """Initialize messages file if it doesn't exist"""
    if not os.path.exists(MESSAGES_FILE):
        try:
            with open(MESSAGES_FILE, 'w') as f:
                json.dump([], f)
            print("Messages file initialized")
        except Exception as e:
            print(f"Error initializing messages file: {e}")

def save_message(name, email, message):
    """Save message to JSON file with error handling"""
    try:
        # Read existing messages
        if os.path.exists(MESSAGES_FILE):
            with open(MESSAGES_FILE, 'r') as f:
                messages = json.load(f)
        else:
            messages = []
        
        # Create new message object
        new_message = {
            'id': len(messages) + 1,
            'name': name.strip(),
            'email': email.strip().lower(),
            'message': message.strip(),
            'timestamp': datetime.now().isoformat(),
            'read': False
        }
        
        # Add to messages list
        messages.append(new_message)
        
        # Save back to file
        with open(MESSAGES_FILE, 'w') as f:
            json.dump(messages, f, indent=2)
        
        print(f"Message saved from {name} ({email})")
        return True
        
    except Exception as e:
        print(f"Error saving message: {e}")
        return False

def get_messages_count():
    """Get total number of messages received"""
    try:
        if os.path.exists(MESSAGES_FILE):
            with open(MESSAGES_FILE, 'r') as f:
                messages = json.load(f)
            return len(messages)
        return 0
    except:
        return 0

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
                flash('✅ Message sent successfully! I\'ll get back to you soon.', 'success')
                
                # Optional: You can add email notification here later
                # For now, we'll just log it
                print(f"New contact form submission from {name} ({email})")
                
            else:
                flash('❌ Sorry, there was an error sending your message. Please try again.', 'error')
            
            return redirect(url_for('contact'))
    
    return render_template('contact.html', data=portfolio_data)

@app.route('/about')
def about():
    """About page"""
    return render_template('about.html', data=portfolio_data)

# ===== API ROUTES (Optional) =====
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
        'message_count': get_messages_count()
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

# ===== INITIALIZATION =====
# Remove the deprecated before_first_request decorator
# We'll initialize when the app starts instead

# ===== MAIN APPLICATION =====
if __name__ == '__main__':
    # Initialize messages file
    init_messages_file()
    
    # Run the application
    print("🎉 Portfolio application starting...")
    print("📧 Messages will be saved to:", MESSAGES_FILE)
    print("🌐 Server will run on: http://127.0.0.1:5000")
    print("💡 Make sure to update your personal information in the portfolio_data dictionary!")
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )