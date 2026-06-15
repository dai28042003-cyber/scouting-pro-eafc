from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

# ==========================================
# TABLA DE USUARIOS
# ==========================================
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    
    # SEPARACIÓN DE NEGOCIO: Un plan para cada módulo
    carrera_tier = db.Column(db.String(20), default='Aficionado')
    fut_tier = db.Column(db.String(20), default='Gratis')
    
    # Mantenemos 'tier' temporalmente para no romper el código antiguo
    tier = db.Column(db.String(20), default='Aficionado')

# ==========================================
# TABLA DE FAVORITOS (Listas de seguimiento)
# ==========================================
class Favorito(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Identifica a qué usuario pertenece esta carpeta
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # Identifica al jugador que ha guardado
    nombre_jugador = db.Column(db.String(100), nullable=False)
    
    # Conexión virtual para acceder a los favoritos rápidamente
    user = db.relationship('User', backref=db.backref('favoritos', lazy=True))