from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
import stripe
import re
import traceback
import random
import smtplib
import os
from email.mime.text import MIMEText
from models import User, db 

auth_bp = Blueprint('auth', __name__)

# --- MOTOR DE CORREO AUTOMÁTICO MEJORADO ---
def enviar_codigo(destinatario, codigo):
    remitente = os.environ.get('MAIL_USERNAME')
    password = os.environ.get('MAIL_PASSWORD')
    
    if not remitente or not password:
        raise Exception("Las variables MAIL_USERNAME o MAIL_PASSWORD no están configuradas en Render. Revisa la pestaña Environment.")

    msg = MIMEText(f"Bienvenido Mánager.\n\nTu código de acceso de 6 dígitos para Scouting PRO es: {codigo}\n\nIntroduce este código en la web para activar tu cuenta.")
    msg['Subject'] = 'Código de Verificación - Scouting PRO'
    msg['From'] = remitente
    msg['To'] = destinatario

    try:
        # Añadimos TIMEOUT de 10 segundos para que el servidor no se quede pillado
        server = smtplib.SMTP('smtp.gmail.com', 587, timeout=10)
        server.starttls()
        server.login(remitente, password)
        server.sendmail(remitente, destinatario, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        # Si Gmail lo bloquea, lanzamos el error para cazarlo en la pantalla negra
        raise Exception(f"Fallo al conectar con Gmail. Detalles: {e}")

# --- RUTAS ---
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
            tier = request.form.get('tier', 'Aficionado') 
            
            if not re.match(r'^(?=.*[A-Z])(?=.*\d).{8,}$', password_input):
                flash("Tu contraseña es muy débil. Mínimo 8 caracteres, 1 mayúscula y 1 número.")
                return redirect(url_for('auth.registro'))

            if User.query.filter_by(username=username).first():
                flash("Este Nombre de Usuario ya está pillado.")
                return redirect(url_for('auth.registro'))
                
            if User.query.filter_by(email=email).first():
                flash("Este correo ya pertenece a un Director Deportivo.")
                return redirect(url_for('auth.registro'))
                
            # Generamos el código secreto de 6 dígitos
            codigo_secreto = str(random.randint(100000, 999999))
            
            # ¡NUEVO ORDEN! 1º Enviamos el correo. Si falla, aborta y no guarda al usuario.
            enviar_codigo(email, codigo_secreto)
            
            # 2º Si el correo se envía bien, guardamos al usuario
            nuevo_usuario = User(
                nombre=nombre,
                apellido1=apellido1,
                apellido2=apellido2,
                username=username,
                email=email,
                password=generate_password_hash(password_input),
                tier=tier,
                verificado=False,
                codigo_verificacion=codigo_secreto
            )
            db.session.add(nuevo_usuario)
            db.session.commit()
            
            login_user(nuevo_usuario)
            return redirect(url_for('auth.verificacion')) 
            
        return render_template('registro.html')

    except Exception as e:
        error_trace = traceback.format_exc()
        return f"""
        <div style='background:#111; color:#ff4444; padding:30px; font-family:monospace; font-size:16px; min-height:100vh;'>
            <h2 style='color:white;'>🚨 Error de Correo Detectado 🚨</h2>
            <p>Gmail nos ha cortado el paso. Pásame este texto:</p>
            <pre style='background:#000; padding:20px; border:1px solid #ff4444;'>{error_trace}</pre>
        </div>
        """

@auth_bp.route('/verificacion', methods=['GET', 'POST'])
@login_required
def verificacion():
    if current_user.verificado:
        return redirect(url_for('auth.vestuario'))

    if request.method == 'POST':
        codigo_introducido = request.form.get('codigo')
        
        if codigo_introducido == current_user.codigo_verificacion:
            current_user.verificado = True
            db.session.commit()
            flash("¡Identidad confirmada! Bienvenido al Vestuario.")
            return redirect(url_for('auth.vestuario'))
        else:
            flash("El código es incorrecto. Revisa tu bandeja de entrada o SPAM.")
            
    return render_template('verificar.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password_input = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password_input):
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

@auth_bp.route('/checkout/<plan>')
@login_required
def checkout(plan):
    if not current_user.verificado:
        return redirect(url_for('auth.verificacion'))
        
    precios = {'aficionado': 399, 'profesional': 599, 'clasemundial': 899}
    precio_centimos = precios.get(plan, 999)
    nombre_plan = f"Plan {plan.capitalize()} - Scouting PRO"

    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{'price_data': {'currency': 'eur', 'product_data': {'name': nombre_plan}, 'unit_amount': precio_centimos}, 'quantity': 1}],
            mode='payment',
            success_url=url_for('auth.pago_exitoso', _external=True) + f"?session_id={{CHECKOUT_SESSION_ID}}&plan={plan}",
            cancel_url=url_for('home', _external=True),
            client_reference_id=current_user.id
        )
        return redirect(checkout_session.url)
    except Exception as e:
        flash(f"Error pasarela: {e}")
        return redirect(url_for('auth.vestuario'))

@auth_bp.route('/pago-exitoso')
@login_required
def pago_exitoso():
    plan_comprado = request.args.get('plan', 'profesional')
    tier_map = {'aficionado': 'Aficionado', 'profesional': 'Profesional', 'clasemundial': 'Clase Mundial'}
    current_user.tier = tier_map.get(plan_comprado, 'Profesional')
    db.session.commit()
    return render_template('pago_exitoso.html', plan=current_user.tier)