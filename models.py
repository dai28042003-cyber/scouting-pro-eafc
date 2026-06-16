from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

# ==========================================
# TABLA DE USUARIOS
# ==========================================
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido1 = db.Column(db.String(50), nullable=False)
    apellido2 = db.Column(db.String(50), nullable=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    tier = db.Column(db.String(50), default='Aficionado')
    
    # --- NUEVOS CAMPOS PARA EL ASALTO 2 ---
    verificado = db.Column(db.Boolean, default=False)
    codigo_verificacion = db.Column(db.String(6), nullable=True)

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