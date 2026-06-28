from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_login import LoginManager, current_user, login_required
import stripe
import os

# 1. Importamos la BD y los Modelos
from models import db, User, Jugador, Favorito

# Importamos tu archivo de datos local
from datos import jugadores as lista_jugadores 

login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'usuarios.db')
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'clave_super_secreta_proyecto_fc')
    
    # Configuración de Stripe
    # Configuración de Stripe (Limpio y seguro)
    stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')
    ENDPOINT_SECRET = os.environ.get('STRIPE_WEBHOOK_SECRET')

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from routes.auth import auth_bp
    from routes.carrera import carrera_bp
    from routes.fut import fut_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(carrera_bp)
    app.register_blueprint(fut_bp)

    # -------------------------------------------------------------------
    # DICCIONARIO DE PRECIOS STRIPE
    # Sustituye estos valores por los IDs reales cuando crees los productos en Stripe
    # -------------------------------------------------------------------
    PRECIOS_STRIPE = {
        'Manager Pro': 'price_1TmWSB0BI92fS3V5DtvdISP5',
        'Clase  Mundial': 'price_1TmWSo0BI92fS3V5L5Q0bCOd'
    }

    # -------------------------------------------------------------------
    # RUTAS DE PAGO Y SUSCRIPCIÓN
    # -------------------------------------------------------------------
    
    @app.route('/checkout/<plan_id>')
    @login_required
    def crear_checkout(plan_id):
        if plan_id not in PRECIOS_STRIPE:
            flash("El plan seleccionado no es válido.", "error")
            return redirect(url_for('home'))

        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price': PRECIOS_STRIPE[plan_id],
                        'quantity': 1,
                    },
                ],
                mode='payment', # Cambiar a 'subscription' si decides hacer cobros mensuales
                success_url= request.url_root + 'pago-exitoso?session_id={CHECKOUT_SESSION_ID}&plan=' + plan_id,
                cancel_url= request.url_root + 'dashboard',
                client_reference_id= str(current_user.id),
                metadata={'plan_id': plan_id} # Enviamos el plan elegido de forma invisible
            )
            return redirect(checkout_session.url, code=303)
            
        except Exception as e:
            flash(f"Error al conectar con la pasarela de pago: {str(e)}", "error")
            return redirect(url_for('home'))

    @app.route('/pago-exitoso')
    @login_required
    def pago_exitoso():
        plan_comprado = request.args.get('plan', 'Premium')
        # Mapeamos el ID de la URL a un nombre bonito para la vista
        nombres_planes = {
            'aficionado': 'Aficionado',
            'profesional': 'Profesional',
            'clasemundial': 'Clase Mundial'
        }
        nombre_bonito = nombres_planes.get(plan_comprado, plan_comprado.capitalize())
        return render_template('pago_exitoso.html', plan=nombre_bonito)

    @app.route('/webhook', methods=['POST'])
    def webhook_stripe():
        payload = request.data
        sig_header = request.headers.get('Stripe-Signature')

        try:
            event = stripe.Webhook.construct_event(payload, sig_header, ENDPOINT_SECRET)
        except ValueError as e:
            return 'Payload inválido', 400
        except stripe.error.SignatureVerificationError as e:
            return 'Firma inválida', 400

        # Si el pago se ha completado correctamente...
        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            usuario_id = session.get('client_reference_id')
            plan_comprado = session.get('metadata', {}).get('plan_id')

            if usuario_id and plan_comprado:
                # Diccionario para mapear el ID del plan de Stripe con el de tu Base de Datos
                tier_mapping = {
                    'aficionado': 'Aficionado',
                    'profesional': 'Profesional',
                    'clasemundial': 'Clase Mundial'
                }
                
                # Actualizamos el usuario en la BD de forma segura
                user = User.query.get(int(usuario_id))
                if user:
                    user.tier = tier_mapping.get(plan_comprado, 'Aficionado')
                    db.session.commit()
                    print(f"ÉXITO: Usuario {user.username} actualizado al nivel {user.tier}")

        return jsonify(success=True), 200

    # -------------------------------------------------------------------
    # VOLCADO DE DATOS Y RUTA PRINCIPAL
    # -------------------------------------------------------------------

    with app.app_context():
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