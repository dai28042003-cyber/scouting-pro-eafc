from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
# IMPORTANTE: Hemos añadido Jugador a las importaciones
from models import db, Favorito, Jugador

# 1. IMPORTAMOS NUESTRA NUEVA BASE DE DATOS DE PYTHON
from datos import jugadores as datos_reales

carrera_bp = Blueprint('carrera', __name__)

@carrera_bp.route('/demo')
def demo():
    jugadores = datos_reales[:10] # Cogemos los 10 primeros
    return render_template('index.html', jugadores=jugadores, demo_mode=True)

@carrera_bp.route('/dashboard')
@login_required
def dashboard():
    tier_actual = getattr(current_user, 'carrera_tier', current_user.tier)
    
    edad_max = request.args.get('edad_max', default=40, type=int)
    presupuesto_max = request.args.get('presupuesto_max', default=1000000000, type=float)
    
    # Filtramos la lista de Python directamente
    df_filtrado = [j for j in datos_reales if j['Edad'] <= edad_max and j['Valor Real (€)'] <= presupuesto_max]
    
    # Ordenamos por Ganga Score y ROI
    df_filtrado.sort(key=lambda x: (x.get('Ganga Score', 0), x.get('ROI (%)', 0)), reverse=True)
    
    if tier_actual == 'Aficionado':
        jugadores = df_filtrado[:50]
        graficos = False
    else:
        jugadores = df_filtrado 
        graficos = True

    return render_template('dashboard_privado.html', 
                           jugadores=jugadores, 
                           tier=tier_actual, 
                           graficos=graficos,
                           edad_max=edad_max,
                           presupuesto_max=presupuesto_max)

@carrera_bp.route('/jugador/<nombre>')
@login_required
def perfil_jugador(nombre):
    try:
        tier_actual = getattr(current_user, 'carrera_tier', current_user.tier)
        
        # 1. Buscamos al jugador exacto en nuestra lista de Python
        jugador_encontrado = next((j for j in datos_reales if j['Nombre'] == nombre), None)
        
        if not jugador_encontrado:
            flash("Jugador no encontrado en la base de datos.")
            return redirect(url_for('carrera.dashboard'))
            
        # 2. Comprobamos si está en favoritos
        # Buscamos primero al jugador en la base de datos real
        jugador_db = Jugador.query.filter_by(nombre=nombre).first()
        
        # Comprobamos si su ID está en la libreta de este mánager
        es_favorito = False
        if jugador_db:
            es_favorito = Favorito.query.filter_by(user_id=current_user.id, jugador_id=jugador_db.id).first() is not None
                
        # 3. Intentamos renderizar la plantilla
        return render_template('perfil.html', jugador=jugador_encontrado, tier=tier_actual, es_favorito=es_favorito)
        
    except Exception as e:
        # TRAMPA PARA CAZAR EL ERROR 500
        import traceback
        error_trace = traceback.format_exc()
        return f"""
        <div style='background:#111; color:#ff4444; padding:30px; font-family:monospace; font-size:16px; line-height:1.5; min-height:100vh;'>
            <h2 style='color:white; margin-bottom:20px; font-family:sans-serif;'>🚨 Autopsia del Error 500 🚨</h2>
            <p>El servidor se ha estrellado al intentar cargar a <b>{nombre}</b>. Aquí tienes el motivo exacto:</p>
            <pre style='background:#000; padding:20px; overflow-x:auto; border:1px solid #ff4444;'>{error_trace}</pre>
            <p style='color:white; margin-top:20px;'>Copia todo este block de texto negro y pásamelo.</p>
        </div>
        """

@carrera_bp.route('/favorito/<nombre>', methods=['POST'])
@login_required
def toggle_favorito(nombre):
    tier_actual = getattr(current_user, 'carrera_tier', current_user.tier)
    
    # 1. Buscamos la ficha oficial del jugador en la BD
    jugador_db = Jugador.query.filter_by(nombre=nombre).first()
    
    if not jugador_db:
        flash("Error: El jugador no existe en la base de datos principal.")
        return redirect(request.referrer)

    # 2. Buscamos si ya está en la libreta del usuario usando el ID
    fav = Favorito.query.filter_by(user_id=current_user.id, jugador_id=jugador_db.id).first()
    
    if fav:
        # Si ya estaba, lo borramos (Dejar de seguir)
        db.session.delete(fav)
        flash(f"Has quitado a {nombre} de tu libreta.")
    else:
        # LÍMITE DE AFICIONADOS: Comprobamos cuántos tiene guardados
        total_favoritos = Favorito.query.filter_by(user_id=current_user.id).count()
        if tier_actual == 'Aficionado' and total_favoritos >= 3:
            flash("Límite alcanzado. Mejora a Mánager Pro para seguir jugadores ilimitados.")
        else:
            # Si no estaba y tiene hueco, lo añadimos usando las nuevas columnas
            nuevo_fav = Favorito(user_id=current_user.id, jugador_id=jugador_db.id)
            db.session.add(nuevo_fav)
            flash(f"Has guardado a {nombre} en tu libreta.")
            
    db.session.commit()
    return redirect(request.referrer)

@carrera_bp.route('/mis-promesas')
@login_required
def mis_promesas():
    tier_actual = getattr(current_user, 'carrera_tier', current_user.tier)
    
    # 1. Sacamos las relaciones de favoritos del usuario
    favoritos_db = Favorito.query.filter_by(user_id=current_user.id).all()
    ids_guardados = [fav.jugador_id for fav in favoritos_db]
    
    # 2. Obtenemos los nombres de esos IDs consultando a los jugadores
    jugadores_db = Jugador.query.filter(Jugador.id.in_(ids_guardados)).all()
    nombres_guardados = [j.nombre for j in jugadores_db]
    
    # 3. Filtramos nuestra lista de datos reales para enviar a Jinja
    jugadores_favs = [j for j in datos_reales if j['Nombre'] in nombres_guardados]

    return render_template('mis_promesas.html', jugadores=jugadores_favs, tier=tier_actual)