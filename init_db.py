from app import app
from models import db, User

with app.app_context():
    db.create_all()

    users = [
        ('admin', 'admin123', 'admin'),
        ('ema',   'emaema',   'user'),
        ('yuri',  'yuri123',  'user'),
        ('gene',  'gene123',  'user'),
    ]

    for username, password, role in users:
        if not User.query.filter_by(username=username).first():
            u = User(username=username, role=role)
            u.set_password(password)
            db.session.add(u)

    db.session.commit()
    print("Base de datos inicializada con usuarios de prueba.")