from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import pandas as pd
import stripe

app = Flask(__name__)

# ==========================================
# CONFIGURACIÓN GENERAL
# ==========================================
# Clave de seguridad para las sesiones (en producción debe ser secreta)
app.config['SECRET_KEY'] = 'clave_super_secreta_proyecto_fc'
# Conectamos una base de datos SQLite local
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usuarios.db'

# Clave de prueba de Stripe
stripe.api_key = "sk_test_tu_clave_secreta_aqui"

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# ==========================================
# MODELO DE BASE DE DATOS (Usuarios)
# ==========================================
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    # Niveles: 'Aficionado', 'Profesional', 'Clase Mundial'
    tier = db.Column(db.String(20), default='Aficionado') 

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ==========================================
# RUTAS PÚBLICAS
# ==========================================
@app.route('/')
def home():
    return render_template('landing.html')

@app.route('/demo')
def demo():
    # La demo que ya tenías, abierta para todos
    try:
        df = pd.read_csv('scouting_premium.csv')
        jugadores = df.head(10).to_dict(orient='records') # Solo enseñamos 10 en la demo
    except:
        jugadores = []
    return render_template('index.html', jugadores=jugadores, demo_mode=True)

# ==========================================
# SISTEMA DE AUTENTICACIÓN
# ==========================================
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        tier = request.form.get('tier') 
        
        user = User.query.filter_by(username=username).first()
        if user:
            flash('El usuario ya existe')
            return redirect(url_for('registro'))
            
        nuevo_usuario = User(
            username=username, 
            password_hash=generate_password_hash(password),
            tier=tier
        )
        db.session.add(nuevo_usuario)
        db.session.commit()
        
        login_user(nuevo_usuario)
        return redirect(url_for('dashboard'))
        
    return render_template('registro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Datos incorrectos')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

# ==========================================
# RUTAS PRIVADAS (Dashboard y Filtros)
# ==========================================
@app.route('/dashboard')
@login_required
def dashboard():
    try:
        df = pd.read_csv('scouting_premium.csv')
        
        # Capturamos los filtros de la web
        edad_max = request.args.get('edad_max', default=40, type=int)
        presupuesto_max = request.args.get('presupuesto_max', default=1000000000, type=float)
        
        # Aplicamos los filtros matemáticos
        df_filtrado = df[(df['Edad'] <= edad_max) & (df['Valor Real (€)'] <= presupuesto_max)]
        
        # Ordenamos por métricas de rentabilidad
        if 'Ganga Score' in df_filtrado.columns and 'ROI (%)' in df_filtrado.columns:
            df_filtrado = df_filtrado.sort_values(by=['Ganga Score', 'ROI (%)'], ascending=[False, False])
        
        # Restricciones de nivel de usuario
        if current_user.tier == 'Aficionado':
            jugadores = df_filtrado.head(50).to_dict(orient='records')
            graficos = False
        else:
            jugadores = df_filtrado.to_dict(orient='records') 
            graficos = True
            
    except Exception as e:
        print(f"Error procesando el dashboard: {e}")
        jugadores = []
        graficos = False
        edad_max = 40
        presupuesto_max = 1000000000

    return render_template('dashboard_privado.html', 
                           jugadores=jugadores, 
                           tier=current_user.tier, 
                           graficos=graficos,
                           edad_max=edad_max,
                           presupuesto_max=presupuesto_max)

# ==========================================
# RUTAS DE PAGO (Stripe)
# ==========================================
@app.route('/checkout/<plan>')
@login_required
def checkout(plan):
    precios = {
        'aficionado': 499,
        'profesional': 999,
        'clasemundial': 4999
    }
    
    precio_centimos = precios.get(plan, 999)
    nombre_plan = f"Plan {plan.capitalize()} - Scouting PRO"

    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'eur',
                    'product_data': {'name': nombre_plan},
                    'unit_amount': precio_centimos,
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=url_for('pago_exitoso', _external=True) + f"?session_id={{CHECKOUT_SESSION_ID}}&plan={plan}",
            cancel_url=url_for('home', _external=True),
            client_reference_id=current_user.id
        )
        return redirect(checkout_session.url)
    except Exception as e:
        flash(f"Error al conectar con la pasarela de pago: {e}")
        return redirect(url_for('dashboard'))

@app.route('/pago-exitoso')
@login_required
def pago_exitoso():
    plan_comprado = request.args.get('plan', 'profesional')
    
    tier_map = {
        'aficionado': 'Aficionado',
        'profesional': 'Profesional',
        'clasemundial': 'Clase Mundial'
    }
    
    # Actualiza el usuario en la base de datos tras el pago
    current_user.tier = tier_map.get(plan_comprado, 'Profesional')
    db.session.commit()
    
    return render_template('pago_exitoso.html', plan=current_user.tier)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)