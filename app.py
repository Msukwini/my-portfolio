from flask import Flask, render_template, request, flash, redirect, url_for
import os
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-123')

# Portfolio data - Update this with your info!
portfolio_data = {
    "name": "Your Name",
    "title": "Student Developer",
    "about": "I'm a passionate student developer learning web development and building cool projects!",
    "skills": ["Python", "Flask", "HTML/CSS", "JavaScript", "Git"],
    "projects": [
        {
            "name": "Portfolio Website",
            "description": "A personal portfolio built with Flask",
            "tech": ["Python", "Flask", "HTML", "CSS"]
        },
        {
            "name": "Task Manager",
            "description": "A simple task management application",
            "tech": ["Python", "Flask", "SQLite"]
        }
    ],
    "email": "your.email@student.com",  # Update this
    "github": "https://github.com/yourusername",
    "linkedin": "https://linkedin.com/in/yourusername"
}

# Store messages in a simple JSON file (free tier solution)
MESSAGES_FILE = 'messages.json'

def save_message(name, email, message):
    """Save message to JSON file"""
    try:
        # Create messages file if it doesn't exist
        if not os.path.exists(MESSAGES_FILE):
            with open(MESSAGES_FILE, 'w') as f:
                json.dump([], f)
        
        # Read existing messages
        with open(MESSAGES_FILE, 'r') as f:
            messages = json.load(f)
        
        # Add new message
        new_message = {
            'name': name,
            'email': email,
            'message': message,
            'timestamp': datetime.now().isoformat()
        }
        messages.append(new_message)
        
        # Save back to file
        with open(MESSAGES_FILE, 'w') as f:
            json.dump(messages, f, indent=2)
            
        return True
    except Exception as e:
        print(f"Error saving message: {e}")
        return False

@app.route('/')
def index():
    return render_template('index.html', data=portfolio_data)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        
        if not all([name, email, message]):
            flash('Please fill in all fields', 'error')
        else:
            if save_message(name, email, message):
                flash('Message sent successfully! I\'ll get back to you soon.', 'success')
            else:
                flash('Sorry, there was an error sending your message. Please try again.', 'error')
            
            return redirect(url_for('contact'))
    
    return render_template('contact.html', data=portfolio_data)

# For Vercel serverless deployment
@app.route('/api/health')
def health_check():
    return {'status': 'healthy', 'message': 'Portfolio API is running'}

if __name__ == '__main__':
    app.run(debug=True)