from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
import os
from datetime import datetime

app = Flask(__name__)

# Simple secret key for Vercel
app.secret_key = os.environ.get('SECRET_KEY', 'simple-secret-key-for-vercel')

# Portfolio data
portfolio_data = {
    "name": "Msukwini",
    "title": "Student Developer", 
    "about": "I'm a passionate student developer learning web development and building cool projects.",
    "skills": ["Python", "Flask", "HTML/CSS", "JavaScript", "Git"],
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
        "linkedin": "#"
    }
}

# Simple in-memory storage
messages_store = []

@app.route('/')
def index():
    try:
        return render_template('index.html', data=portfolio_data)
    except Exception as e:
        return f"Error loading page: {str(e)}", 500

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    try:
        if request.method == 'POST':
            name = request.form.get('name', '').strip()
            email = request.form.get('email', '').strip()
            message = request.form.get('message', '').strip()
            
            # Basic validation
            if not name or not email or not message:
                flash('Please fill in all fields', 'error')
            elif len(message) < 5:
                flash('Message should be at least 5 characters long', 'error')
            else:
                # Save message to memory
                new_message = {
                    'name': name,
                    'email': email,
                    'message': message,
                    'timestamp': datetime.now().isoformat()
                }
                messages_store.append(new_message)
                
                # Log to Vercel console
                print(f"NEW MESSAGE - Name: {name}, Email: {email}, Message: {message}")
                
                flash('Message sent successfully! Thank you for reaching out.', 'success')
                return redirect(url_for('contact'))
        
        return render_template('contact.html', data=portfolio_data)
    except Exception as e:
        return f"Error in contact form: {str(e)}", 500

@app.route('/about')
def about():
    try:
        return render_template('about.html', data=portfolio_data)
    except Exception as e:
        return f"Error loading about page: {str(e)}", 500

# Health check endpoint
@app.route('/api/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'service': 'portfolio',
        'timestamp': datetime.now().isoformat()
    })

# Simple error handlers
@app.errorhandler(404)
def not_found(error):
    return "Page not found", 404

@app.errorhandler(500)
def internal_error(error):
    return "Internal server error", 500

# Vercel needs this
if __name__ == '__main__':
    app.run(debug=True)
else:
    # For Vercel serverless
    application = app