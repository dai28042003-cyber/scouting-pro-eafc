from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_login import LoginManager, current_user, login_required
import os

# 1. Importamos la BD y los Modelos
from models import db, User, Jugador, Favorito

# Importamos tu archivo de datos local
from datos import jugadores as lista_jugadores 

login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    basedir = os.path.abspath(os.path.dirname(__file__))
    
    # --- CONEXIÓN INTELIGENTE A LA BASE DE DATOS ---
    database_url = os.environ.get('DATABASE_URL')
    if database_url:
        # SQLAlchemy exige que la URL empiece por postgresql:// en las versiones nuevas
        if database_url.startswith("postgres://"):
            database_url = database_url.replace("postgres://", "postgresql://", 1)
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    else:
        # Si estás probando en tu ordenador sin internet, usa el archivo local
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'usuarios.db')
        
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'clave_super_secreta_proyecto_fc')

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Importamos y registramos los Blueprints (Aquí es donde vive tu lógica real de Stripe)
    from routes.auth import auth_bp
    from routes.carrera import carrera_bp
    from routes.fut import fut_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(carrera_bp)
    app.register_blueprint(fut_bp)

    # -------------------------------------------------------------------
    # VOLCADO DE DATOS Y RUTA PRINCIPAL
    # -------------------------------------------------------------------

    with app.app_context():
        # 👇 PARCHE POSTGRESQL: Forzamos el borrado para aplicar los nuevos String(50) de models.py 👇
        db.drop_all()
        
        db.create_all()
        
        # Detector: ¿Está la tabla vacía?
        if not Jugador.query.first():
            print("Inyectando 200 jugadores en la base de datos...")
            for j in lista_jugadores:
                nuevo_jugador = Jugador(
                    nombre=j.get('Nombre'),
                    posicion=j.get('Posición'),
                    equipo=j.get('Equipo'),
                    nacionalidad=j.get('Nacionalidad'),
                    edad=int(j.get('Edad', 0)),
                    media=int(j.get('Media', 0)),
                    potencial=int(j.get('Potencial', 0)),
                    valor=float(j.get('Valor Real (€)', 0)),
                    foto=j.get('Foto'),
                    ganga_score=float(j.get('Ganga Score', 0)),
                    roi=float(j.get('ROI (%)', 0)),
                    margen_crecimiento=int(j.get('Margen de Crecimiento', 0))
                )
                db.session.add(nuevo_jugador)
            
            db.session.commit()
            print("¡Volcado de datos completado con éxito!")

    @app.route('/')
    def home():
        jugadores_portada = Jugador.query.limit(10).all()
        return render_template('landing.html', jugadores=jugadores_portada)

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)