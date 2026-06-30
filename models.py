from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

# 1. TABLA DE CLIENTES (MÁNAGERS)
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido1 = db.Column(db.String(100), nullable=False)
    apellido2 = db.Column(db.String(100), nullable=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
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
    nombre = db.Column(db.String(150))          # Ampliado a 150
    posicion = db.Column(db.String(50))         # Ampliado a 50 (¡Este era el culpable!)
    equipo = db.Column(db.String(150))          # Ampliado a 150
    nacionalidad = db.Column(db.String(100))    # Ampliado a 100
    edad = db.Column(db.Integer)
    media = db.Column(db.Integer)
    potencial = db.Column(db.Integer)
    valor = db.Column(db.Float)
    foto = db.Column(db.String(300))            # Las URLs pueden ser muy largas
    ganga_score = db.Column(db.Float)
    roi = db.Column(db.Float)
    margen_crecimiento = db.Column(db.Integer)

    # Relación: Un jugador puede estar en la libreta de muchos Mánagers
    seguidores = db.relationship('Favorito', backref='jugador_asociado', lazy=True, cascade="all, delete-orphan")

# 3. TABLA DE LA LIBRETA DE OJEO (CONEXIÓN ENTRE MÁNAGER Y JUGADOR)
class Favorito(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    jugador_id = db.Column(db.Integer, db.ForeignKey('jugador.id'), nullable=False)