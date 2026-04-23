import os
from datetime import timedelta

class Config:
    # Clave secreta generada de forma aleatoria (NO hardcoded)
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(32)

    # Base de datos (usa variable de entorno en producción)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REMEMBER_COOKIE_DURATION = timedelta(days=7)
    
    # Sesiones seguras
    SESSION_COOKIE_SECURE = True      # Solo HTTPS
    SESSION_COOKIE_HTTPONLY = True     # No accesible por JS
    SESSION_COOKIE_SAMESITE = 'Lax'   # Protección CSRF
    REMEMBER_COOKIE_SECURE = True
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    WTF_CSRF_ENABLED = True

class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = True
    TEMPLATES_AUTO_RELOAD = True
    WTF_CSRF_ENABLED = False  # Desactivar CSRF en desarrollo para facilitar pruebas

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}