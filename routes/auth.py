from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
import stripe
from models import User

# Importamos la base de datos desde app.py (evitando importaciones circulares)
from models import db 

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        tier = request.form.get('tier', 'Aficionado') 
        
        user = User.query.filter_by(username=username).first()
        if user:
            flash('El usuario ya existe')
            return redirect(url_for('auth.registro'))
            
        nuevo_usuario = User(
            username=username, 
            password_hash=generate_password_hash(password),
            tier=tier
        )
        db.session.add(nuevo_usuario)
        db.session.commit()
        
        login_user(nuevo_usuario)
        # Redirige al nuevo Hub Central
        return redirect(url_for('auth.vestuario')) 
        
    return render_template('registro.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            # Redirige al nuevo Hub Central
            return redirect(url_for('auth.vestuario')) 
        flash('Datos incorrectos')
    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@auth_bp.route('/checkout/<plan>')
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
            success_url=url_for('auth.pago_exitoso', _external=True) + f"?session_id={{CHECKOUT_SESSION_ID}}&plan={plan}",
            cancel_url=url_for('home', _external=True),
            client_reference_id=current_user.id
        )
        return redirect(checkout_session.url)
    except Exception as e:
        flash(f"Error al conectar con la pasarela de pago: {e}")
        return redirect(url_for('auth.vestuario'))

@auth_bp.route('/pago-exitoso')
@login_required
def pago_exitoso():
    plan_comprado = request.args.get('plan', 'profesional')
    tier_map = {
        'aficionado': 'Aficionado',
        'profesional': 'Profesional',
        'clasemundial': 'Clase Mundial'
    }
    
    current_user.tier = tier_map.get(plan_comprado, 'Profesional')
    db.session.commit()
    
    return render_template('pago_exitoso.html', plan=current_user.tier)

# ==========================================
# EL VESTUARIO (HUB CENTRAL)
# ==========================================
@auth_bp.route('/vestuario')
@login_required
def vestuario():
    return render_template('vestuario.html', tier=current_user.tier)