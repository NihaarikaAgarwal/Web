import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message
from dotenv import load_dotenv # Keep this for local development

# Load environment variables from .env file for local development
load_dotenv()

app = Flask(__name__)

# --- Flask-Mail Configuration (using os.getenv for flexibility) ---
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT')) # Ensure port is an integer
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS').lower() == 'true'
app.config['MAIL_USE_SSL'] = os.getenv('MAIL_USE_SSL').lower() == 'true'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'a_fallback_secret_key_if_not_set')

mail = Mail(app)

# --- Routes ---

@app.route('/')
def index():
    """Renders the contact form page."""
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    """Handles the contact form submission and sends an email."""
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message_content = request.form.get('message')

        # Basic validation
        if not name or not email or not message_content:
            flash('All fields are required!', 'error')
            return redirect(url_for('index'))

        try:
            msg = Message(
                subject=f"Contact Form Submission from {name}",
                sender=app.config['MAIL_DEFAULT_SENDER'],
                recipients=[os.getenv('RECIPIENT_EMAIL')], # The email where you want to receive messages
                html=f"""
                <p><strong>Name:</strong> {name}</p>
                <p><strong>Email:</strong> {email}</p>
                <p><strong>Message:</strong></p>
                <p style="white-space: pre-wrap;">{message_content}</p>
                """
            )
            mail.send(msg)
            flash('Your message has been sent successfully!', 'success')
        except Exception as e:
            flash(f'Failed to send message. Please try again later. Error: {str(e)}', 'error')
            print(f"Error sending email: {e}") # Log the error for debugging

        return redirect(url_for('index'))

if __name__ == '__main__':
    # This block only runs when you execute app.py directly (locally)
    # It's ignored by Vercel's deployment process
    app.run(debug=True)