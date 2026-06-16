from flask import Flask, render_template
from flask_login import LoginManager
import stripe
import os

# 1. Importamos la BD y el Modelo desde el nuevo archivo
from models import db, User

login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    # 2. Configuración con Ruta Absoluta (¡Clave para Render!)
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'usuarios.db')
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'clave_super_secreta_proyecto_fc')
    stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')

    # 3. Conectamos las extensiones
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # 4. Registramos los módulos
    from routes.auth import auth_bp
    from routes.carrera import carrera_bp
    from routes.fut import fut_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(carrera_bp)
    app.register_blueprint(fut_bp)

    # 5. Forzamos la creación de tablas
    with app.app_context():
        db.create_all()

    @app.route('/')
    def home():
        return render_template('index.html')

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)