from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Favorito

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
    
    # 2. Filtramos la lista de Python directamente
    df_filtrado = [j for j in datos_reales if j['Edad'] <= edad_max and j['Valor Real (€)'] <= presupuesto_max]
    
    # 3. Ordenamos por Ganga Score y ROI
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
        es_favorito = Favorito.query.filter_by(user_id=current_user.id, nombre_jugador=nombre).first() is not None
            
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
            <p style='color:white; margin-top:20px;'>Copia todo este bloque de texto negro y pásamelo.</p>
        </div>
        """

@carrera_bp.route('/favorito/<nombre>', methods=['POST'])
@login_required
def toggle_favorito(nombre):
    tier_actual = getattr(current_user, 'carrera_tier', current_user.tier)
    
    favorito_existente = Favorito.query.filter_by(user_id=current_user.id, nombre_jugador=nombre).first()
    
    if favorito_existente:
        db.session.delete(favorito_existente)
        db.session.commit()
        flash(f"{nombre} eliminado de tu libreta de seguimiento.")
    else:
        total_favoritos = Favorito.query.filter_by(user_id=current_user.id).count()
        
        if tier_actual == 'Aficionado' and total_favoritos >= 3:
            flash("Límite alcanzado. Mejora a Mánager Pro para seguir jugadores ilimitados.")
        else:
            nuevo_fav = Favorito(user_id=current_user.id, nombre_jugador=nombre)
            db.session.add(nuevo_fav)
            db.session.commit()
            flash(f"{nombre} añadido a tu libreta de seguimiento.")
            
    return redirect(url_for('carrera.perfil_jugador', nombre=nombre))

@carrera_bp.route('/mis-promesas')
@login_required
def mis_promesas():
    tier_actual = getattr(current_user, 'carrera_tier', current_user.tier)
    
    favoritos_db = Favorito.query.filter_by(user_id=current_user.id).all()
    nombres_guardados = [fav.nombre_jugador for fav in favoritos_db]
    
    # 5. Filtramos los favoritos desde nuestra lista
    jugadores_favs = [j for j in datos_reales if j['Nombre'] in nombres_guardados]

    return render_template('mis_promesas.html', jugadores=jugadores_favs, tier=tier_actual)

@carrera_bp.route('/godmode/<nivel>')
@login_required
def godmode(nivel):
    niveles_validos = {
        'aficionado': 'Aficionado', 
        'profesional': 'Profesional', 
        'clasemundial': 'Clase Mundial'
    }
    nivel_formateado = niveles_validos.get(nivel.lower())
    
    if nivel_formateado:
        if hasattr(current_user, 'carrera_tier'):
            current_user.carrera_tier = nivel_formateado
        current_user.tier = nivel_formateado
        db.session.commit()
        flash(f'Modo Dios activado: Ahora eres {nivel_formateado}')
    
    return redirect(url_for('carrera.dashboard'))