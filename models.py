from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

# Inicializamos la base de datos AQUÍ para evitar conflictos
db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    tier = db.Column(db.String(20), default='Aficionado')