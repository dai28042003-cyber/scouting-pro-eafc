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
        raise Exception("Falta la RESEND_API_KEY en las variables de entorno.")

    print(f"\n🤫 TRUCO DE MÁNAGER - El código para {destinatario} es: {codigo}\n", flush=True)

    try:
        resend.Emails.send({
            "from": "Scouting PRO <onboarding@resend.dev>",
            "to": destinatario,
            "subject": "Código de Verificación - Scouting PRO",
            "text": f"Bienvenido Mánager.\n\nTu código para Scouting PRO es: {codigo}"
        })
        return True
    except Exception as e:
        print(f"⚠️ AVISO RESEND: Correo no enviado. Usa el código de consola.", flush=True)
        return False

# --- RUTAS DE USUARIO ---
@auth_bp.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        apellido1 = request.form.get('apellido1')
        apellido2 = request.form.get('apellido2', '')
        username = request.form.get('username')
        email = request.form.get('email')
        password_input = request.form.get('password')
        
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
            tier='Aficionado', verificado=False, codigo_verificacion=codigo_secreto
        )
        db.session.add(nuevo_usuario)
        db.session.commit()
        
        login_user(nuevo_usuario)
        return redirect(url_for('auth.verificacion')) 
        
    return render_template('registro.html')

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

    # Forzamos HTTPS para Render y pasamos el plan por URL directamente
    base_url = request.url_root.replace("http://", "https://") if "onrender.com" in request.url_root else request.url_root
    url_exito = f"{base_url}pago-exitoso?session_id={{CHECKOUT_SESSION_ID}}&plan={plan}"
    url_cancel = f"{base_url}vestuario"

    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card', 'bizum', 'link'],
            line_items=[{'price_data': {'currency': 'eur', 'product_data': {'name': nombre_plan}, 'unit_amount': precio_centimos}, 'quantity': 1}],
            mode='payment',
            success_url=url_exito,
            cancel_url=url_cancel,
            client_reference_id=str(current_user.id)
        )
        return redirect(checkout_session.url)
    except Exception as e:
        error_trace = traceback.format_exc()
        return f"<div style='background:#111; color:#ff4444; padding:30px;'><h2>🚨 ERROR INICIANDO STRIPE 🚨</h2><pre>{e}\n\n{error_trace}</pre></div>"

# AUTO-VERIFICACIÓN AL VOLVER DE STRIPE (A prueba de balas)
@auth_bp.route('/pago-exitoso')
@login_required
def pago_exitoso():
    session_id = request.args.get('session_id')
    plan_url = request.args.get('plan', 'profesional')
    
    # Trampa anti-fallos silenciosos
    if not session_id:
        return "<div style='background:#111; color:#ff4444; padding:30px; font-family:monospace;'><h2>🚨 ERROR CRÍTICO 🚨</h2><p>Has vuelto de Stripe pero se ha perdido el session_id. Render ha cortado la URL.</p></div>"

    try:
        stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')
        session = stripe.checkout.Session.retrieve(session_id)
        
        if session.payment_status == 'paid':
            tier_map = {'aficionado': 'Aficionado', 'profesional': 'Profesional', 'clasemundial': 'Clase Mundial'}
            nuevo_nivel = tier_map.get(plan_url, 'Profesional')
            
            # ¡EL PARCHE DEFINITIVO! Actualizamos la columna normal Y la de carrera
            current_user.tier = nuevo_nivel
            if hasattr(current_user, 'carrera_tier'):
                current_user.carrera_tier = nuevo_nivel
                
            db.session.commit()
            return render_template('pago_exitoso.html', plan=current_user.tier)
        else:
            return f"<div style='background:#111; color:#ffaa00; padding:30px; font-family:monospace;'><h2>⏳ PAGO PENDIENTE ⏳</h2><p>Stripe nos dice que el pago está: {session.payment_status}.</p></div>"
            
    except Exception as e:
        error_trace = traceback.format_exc()
        return f"<div style='background:#111; color:#ff4444; padding:30px; font-family:monospace;'><h2>🚨 ERROR EN LA BASE DE DATOS/STRIPE 🚨</h2><pre>{e}\n\n{error_trace}</pre></div>"

# RUTA DE ADMINISTRADOR (Blindada)
@auth_bp.route('/bajar-nivel')
@login_required
def bajar_nivel():
    current_user.tier = 'Aficionado'
    if hasattr(current_user, 'carrera_tier'):
        current_user.carrera_tier = 'Aficionado'
    db.session.commit()
    flash("Nivel reseteado. ¡Ya eres Aficionado de verdad!")
    return redirect(url_for('auth.vestuario'))