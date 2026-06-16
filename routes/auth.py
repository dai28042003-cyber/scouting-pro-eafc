from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
import stripe
import re
import traceback
from models import User

# Importamos la base de datos desde app.py (evitando importaciones circulares)
from models import db 

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/registro', methods=['GET', 'POST'])
def registro():
    try:
        if request.method == 'POST':
            nombre = request.form.get('nombre')
            apellido1 = request.form.get('apellido1')
            apellido2 = request.form.get('apellido2', '') # Opcional
            username = request.form.get('username')
            email = request.form.get('email')
            password_input = request.form.get('password')
            tier = request.form.get('tier', 'Aficionado') 
            
            # 1. LA LEY DE LA CONTRASEÑA FUERTE (8 chars, 1 mayúscula, 1 número)
            if not re.match(r'^(?=.*[A-Z])(?=.*\d).{8,}$', password_input):
                flash("Tu contraseña es muy débil. Mínimo 8 caracteres, una mayúscula y un número.")
                return redirect(url_for('auth.registro'))

            # 2. Comprobar que no nos intentan colar un usuario repetido
            if User.query.filter_by(username=username).first():
                flash("Este Nombre de Usuario ya está pillado. Elige otro.")
                return redirect(url_for('auth.registro'))
                
            if User.query.filter_by(email=email).first():
                flash("Este correo ya pertenece a un Director Deportivo.")
                return redirect(url_for('auth.registro'))
                
            # 3. Guardar en la nueva base de datos (CORREGIDO 'password')
            nuevo_usuario = User(
                nombre=nombre,
                apellido1=apellido1,
                apellido2=apellido2,
                username=username,
                email=email,
                password=generate_password_hash(password_input),
                tier=tier
            )
            db.session.add(nuevo_usuario)
            db.session.commit()
            
            login_user(nuevo_usuario)
            # Redirige al nuevo Hub Central
            return redirect(url_for('auth.vestuario')) 
            
        return render_template('registro.html')

    except Exception as e:
        # TRAMPA PARA CAZAR EL ERROR 500 EN EL REGISTRO
        error_trace = traceback.format_exc()
        return f"""
        <div style='background:#111; color:#ff4444; padding:30px; font-family:monospace; font-size:16px; line-height:1.5; min-height:100vh;'>
            <h2 style='color:white; margin-bottom:20px; font-family:sans-serif;'>🚨 Autopsia del Error 500 (Registro) 🚨</h2>
            <p>El servidor se ha estrellado al intentar registrar al usuario. Aquí tienes el motivo exacto:</p>
            <pre style='background:#000; padding:20px; overflow-x:auto; border:1px solid #ff4444;'>{error_trace}</pre>
            <p style='color:white; margin-top:20px;'>Copia todo este bloque de texto negro y pásamelo.</p>
        </div>
        """

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password_input = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        # CORREGIDO: user.password en lugar de user.password_hash
        if user and check_password_hash(user.password, password_input):
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