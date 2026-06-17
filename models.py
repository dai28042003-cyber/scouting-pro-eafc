from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

# 1. TABLA DE CLIENTES (MÁNAGERS)
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido1 = db.Column(db.String(50), nullable=False)
    apellido2 = db.Column(db.String(50), nullable=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    tier = db.Column(db.String(50), default='Aficionado')
    verificado = db.Column(db.Boolean, default=False)
    codigo_verificacion = db.Column(db.String(6), nullable=True)

    # Relación: Un Mánager puede tener muchos jugadores guardados en su libreta
    favoritos = db.relationship('Favorito', backref='usuario', lazy=True, cascade="all, delete-orphan")

# 2. TABLA DE JUGADORES (LA BASE DE DATOS MASIVA)
class Jugador(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    posicion = db.Column(db.String(10), nullable=False)
    equipo = db.Column(db.String(100), nullable=True)
    nacionalidad = db.Column(db.String(100), nullable=True)
    edad = db.Column(db.Integer, nullable=False)
    media = db.Column(db.Integer, nullable=False)
    potencial = db.Column(db.Integer, nullable=False)
    valor = db.Column(db.Float, nullable=False) # En euros
    foto = db.Column(db.String(200), nullable=True)
    
    # Campos exclusivos para los cálculos PRO
    ganga_score = db.Column(db.Float, nullable=True)
    roi = db.Column(db.Float, nullable=True)
    margen_crecimiento = db.Column(db.Integer, nullable=True)

    # Relación: Un jugador puede estar en la libreta de muchos Mánagers
    seguidores = db.relationship('Favorito', backref='jugador_asociado', lazy=True, cascade="all, delete-orphan")

# 3. TABLA DE LA LIBRETA DE OJEO (CONEXIÓN ENTRE MÁNAGER Y JUGADOR)
class Favorito(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    jugador_id = db.Column(db.Integer, db.ForeignKey('jugador.id'), nullable=False)