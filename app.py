import re
import os

from flask import Flask, request, render_template, flash, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from config import ProductionConfig, DevelopmentConfig
from models import db, User

app = Flask(__name__)

env = os.environ.get('FLASK_ENV', 'development')
if env == 'production':
    app.config.from_object(ProductionConfig)
else:
    app.config.from_object(DevelopmentConfig)

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Por favor inicia sesión para acceder.'

limiter = Limiter(app=app, key_func=get_remote_address, default_limits=['200 per day', '50 per hour'])

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Validación de entradas con regex
def validar_entrada(texto):
    if not texto or len(texto) > 50:
        return False
    if not re.match(r'^[a-zA-Z0-9_.]+$', texto):
        return False
    return True

@app.route('/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        # Validación de entradas vacías
        if not username or not password:
            flash('Usuario y contraseña son obligatorios', 'error')
            return render_template('login.html')

        # Validación de formato con lista blanca
        if not validar_entrada(username) or not validar_entrada(password):
            flash('Caracteres no permitidos detectados', 'error')
            return render_template('login.html')

        # Consulta segura con ORM (previene SQLi)
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user, remember=True)
            return redirect(url_for('dashboard'))
        else:
            flash("Usuario o contraseña incorrectos", "error")
            return render_template('login.html')

    return render_template('login.html')

@app.route("/dashboard")
@login_required # ✅ Control de acceso (Informe R-05)
def dashboard():
    return render_template('dashboard.html', user=current_user)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Sesión cerrada correctamente", "success")
    return redirect(url_for('login'))

@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "
        "style-src 'self' 'unsafe-inline'; "
        "script-src 'self'"
    )
    return response

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=app.config.get('DEBUG', False))