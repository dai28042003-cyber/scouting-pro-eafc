from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import stripe
import os

# 1. Inicializamos las extensiones vacías
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    # 2. Configuración
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'clave_super_secreta_proyecto_fc')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usuarios.db'
    stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')

    # 3. Conectamos las extensiones a la app
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login' # Ahora apunta al blueprint

    # 4. Importamos los modelos (para que la BD los reconozca)
    from models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # 5. Importamos y registramos los Blueprints (Los módulos)
    from routes.auth import auth_bp
    from routes.carrera import carrera_bp
    from routes.fut import fut_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(carrera_bp)
    app.register_blueprint(fut_bp)

    # 6. Creamos las tablas si no existen
    with app.app_context():
        db.create_all()

    # Ruta principal (Landing page)
    @app.route('/')
    def home():
        return render_template('landing.html')

    return app

# Arrancamos la aplicación
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)