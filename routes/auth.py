from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
import stripe
import re
import traceback
import random
import os
import resend
from models import User, db 

auth_bp = Blueprint('auth', __name__)

# --- MOTOR DE CORREO PROFESIONAL (RESEND API) ---
def enviar_codigo(destinatario, codigo):
    resend.api_key = os.environ.get('RESEND_API_KEY')
    if not resend.api_key:
        raise Exception("Falta la RESEND_API_KEY en las variables de entorno de Render.")

    print(f"\n🤫 TRUCO DE MÁNAGER - El código secreto para {destinatario} es: {codigo}\n", flush=True)

    try:
        resend.Emails.send({
            "from": "Scouting PRO <onboarding@resend.dev>",
            "to": destinatario,
            "subject": "Código de Verificación - Scouting PRO",
            "text": f"Bienvenido Mánager.\n\nTu código para Scouting PRO es: {codigo}"
        })
        return True
    except Exception as e:
        print(f"⚠️ AVISO RESEND: Correo no enviado por límite de prueba. Usa el código de la consola.", flush=True)
        return False

# --- RUTAS DE USUARIO ---
@auth_bp.route('/registro', methods=['GET', 'POST'])
def registro():
    try:
        if request.method == 'POST':
            nombre = request.form.get('nombre')
            apellido1 = request.form.get('apellido1')
            apellido2 = request.form.get('apellido2', '')
            username = request.form.get('username')
            email = request.form.get('email')
            password_input = request.form.get('password')
            tier = 'Aficionado'
            
            if not re.match(r'^(?=.*[A-Z])(?=.*\d).{8,}$', password_input):
                flash("Tu contraseña es muy débil. Mínimo 8 caracteres, 1 mayúscula y 1 número.")
                return redirect(url_for('auth.registro'))

            if User.query.filter_by(username=username).first():
                flash("Este Nombre de Usuario ya está pillado.")
                return redirect(url_for('auth.registro'))
                
            if User.query.filter_by(email=email).first():
                flash("Este correo ya pertenece a un Director Deportivo.")
                return redirect(url_for('auth.registro'))
                
            codigo_secreto = str(random.randint(100000, 999999))
            enviar_codigo(email, codigo_secreto)
            
            nuevo_usuario = User(
                nombre=nombre, apellido1=apellido1, apellido2=apellido2,
                username=username, email=email, password=generate_password_hash(password_input),
                tier=tier, verificado=False, codigo_verificacion=codigo_secreto
            )
            db.session.add(nuevo_usuario)
            db.session.commit()
            
            login_user(nuevo_usuario)
            return redirect(url_for('auth.verificacion')) 
            
        return render_template('registro.html')
    except Exception as e:
        error_trace = traceback.format_exc()
        return f"<div style='background:#111; color:#ff4444; padding:30px;'><pre>{error_trace}</pre></div>"

@auth_bp.route('/verificacion', methods=['GET', 'POST'])
@login_required
def verificacion():
    if current_user.verificado:
        return redirect(url_for('auth.vestuario'))

    if request.method == 'POST':
        if request.form.get('codigo') == current_user.codigo_verificacion:
            current_user.verificado = True
            db.session.commit()
            flash("¡Identidad confirmada! Bienvenido al Vestuario.")
            return redirect(url_for('auth.vestuario'))
        else:
            flash("El código es incorrecto.")
            
    return render_template('verificar.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form.get('username')).first()
        if user and check_password_hash(user.password, request.form.get('password')):
            login_user(user)
            return redirect(url_for('auth.vestuario')) 
        flash('Datos incorrectos')
    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@auth_bp.route('/vestuario')
@login_required
def vestuario():
    if not current_user.verificado:
        return redirect(url_for('auth.verificacion'))
    return render_template('vestuario.html', tier=current_user.tier)

# --- RUTAS DE FINANZAS Y STRIPE ---
@auth_bp.route('/checkout/<plan>')
@login_required
def checkout(plan):
    if not current_user.verificado:
        return redirect(url_for('auth.verificacion'))
        
    stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')
    precios = {'aficionado': 399, 'profesional': 599, 'clasemundial': 899}
    precio_centimos = precios.get(plan, 999)
    nombre_plan = f"Plan {plan.capitalize()} - Scouting PRO"

    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card', 'bizum', 'link'],
            line_items=[{'price_data': {'currency': 'eur', 'product_data': {'name': nombre_plan}, 'unit_amount': precio_centimos}, 'quantity': 1}],
            mode='payment',
            success_url=url_for('auth.pago_exitoso', _external=True),
            cancel_url=url_for('home', _external=True),
            client_reference_id=str(current_user.id),
            metadata={'plan_id': plan} # Pasamos el plan de forma segura en la metadata
        )
        return redirect(checkout_session.url)
    except Exception as e:
        error_trace = traceback.format_exc()
        return f"<div style='background:#111; color:#ff4444; padding:30px;'><h2>🚨 ERROR DE STRIPE 🚨</h2><pre>{e}\n\n{error_trace}</pre></div>"

# LA PUERTA TRASERA CERRADA (Ya no regala niveles)
@auth_bp.route('/pago-exitoso')
@login_required
def pago_exitoso():
    return render_template('pago_exitoso.html', plan=current_user.tier)

# EL WEBHOOK (El vigilante de seguridad de Stripe)
@auth_bp.route('/webhook', methods=['POST'])
def webhook_stripe():
    stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')
    endpoint_secret = os.environ.get('STRIPE_WEBHOOK_SECRET')
    
    payload = request.data
    sig_header = request.headers.get('Stripe-Signature')

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except Exception as e:
        return jsonify(error=str(e)), 400

    # Solo si el pago es 100% real y exitoso
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        usuario_id = session.get('client_reference_id')
        plan_comprado = session.get('metadata', {}).get('plan_id', 'profesional')

        if usuario_id:
            user = User.query.get(int(usuario_id))
            if user:
                tier_map = {'aficionado': 'Aficionado', 'profesional': 'Profesional', 'clasemundial': 'Clase Mundial'}
                user.tier = tier_map.get(plan_comprado, 'Profesional')
                db.session.commit() # AQUÍ es donde se sube de nivel de forma segura

    return jsonify(success=True), 200

# RUTA DE ADMINISTRADOR
@auth_bp.route('/bajar-nivel')
@login_required
def bajar_nivel():
    current_user.tier = 'Aficionado'
    db.session.commit()
    flash("Nivel reseteado. ¡Ya eres Aficionado!")
    return redirect(url_for('auth.vestuario'))