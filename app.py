from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import secrets
import openai
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'tu_clave_secreta')  # Cambiar en producción
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sas.db'
app.config['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
app.config['ASSISTANT_ID'] = os.getenv('CREADOR_DE_SAS')

db = SQLAlchemy(app)
openai.api_key = app.config['OPENAI_API_KEY']

# Modelo de Base de Datos
class UserSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    token = db.Column(db.String(64), unique=True, nullable=False)
    expiration = db.Column(db.DateTime, nullable=False)

# Ruta Principal
@app.route('/')
def index():
    return redirect(url_for('login'))

# Sistema de Validación por Email
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        token = secrets.token_urlsafe(32)
        expiration = datetime.now() + timedelta(days=30)
        
        existing_user = UserSession.query.filter_by(email=email).first()
        if existing_user:
            existing_user.token = token
            existing_user.expiration = expiration
        else:
            new_user = UserSession(
                email=email,
                token=token,
                expiration=expiration
            )
            db.session.add(new_user)
        
        db.session.commit()
        
        # Enviar email con enlace de validación (Implementar servicio de email)
        validation_link = url_for('validate', token=token, _external=True)
        return f'Se ha enviado un enlace de validación a {email}'
    
    return render_template('login.html')

# Validación de Token
@app.route('/validate/<token>')
def validate(token):
    session = UserSession.query.filter_by(token=token).first()
    
    if session and session.expiration > datetime.now():
        return redirect(url_for('chat_interface'))
    return 'Enlace inválido o expirado'

# Interfaz de Chat
@app.route('/chat')
def chat_interface():
    return render_template('chat.html')

# API de Chat
@app.route('/api/chat', methods=['POST'])
def chat_api():
    data = request.json
    user_message = data.get('message', '')
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{
                "role": "user",
                "content": user_message
            }],
            assistant_id=app.config['ASSISTANT_ID']
        )
        return jsonify({'response': response['choices'][0]['message']['content']})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
