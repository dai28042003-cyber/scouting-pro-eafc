from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
import pandas as pd
from models import db, Favorito

carrera_bp = Blueprint('carrera', __name__)

@carrera_bp.route('/demo')
def demo():
    try:
        df = pd.read_csv('scouting_premium.csv')
        jugadores = df.head(10).to_dict(orient='records')
    except:
        jugadores = []
    return render_template('index.html', jugadores=jugadores, demo_mode=True)

@carrera_bp.route('/dashboard')
@login_required
def dashboard():
    tier_actual = getattr(current_user, 'carrera_tier', current_user.tier)
    try:
        df = pd.read_csv('scouting_premium.csv')
        
        edad_max = request.args.get('edad_max', default=40, type=int)
        presupuesto_max = request.args.get('presupuesto_max', default=1000000000, type=float)
        
        df_filtrado = df[(df['Edad'] <= edad_max) & (df['Valor Real (€)'] <= presupuesto_max)]
        
        if 'Ganga Score' in df_filtrado.columns and 'ROI (%)' in df_filtrado.columns:
            df_filtrado = df_filtrado.sort_values(by=['Ganga Score', 'ROI (%)'], ascending=[False, False])
        
        if tier_actual == 'Aficionado':
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
                           tier=tier_actual, 
                           graficos=graficos,
                           edad_max=edad_max,
                           presupuesto_max=presupuesto_max)

@carrera_bp.route('/jugador/<nombre>')
@login_required
def perfil_jugador(nombre):
    tier_actual = getattr(current_user, 'carrera_tier', current_user.tier)
    try:
        df = pd.read_csv('scouting_premium.csv')
        datos_jugador = df[df['Nombre'] == nombre].to_dict(orient='records')
        
        if not datos_jugador:
            flash("Jugador no encontrado en la base de datos.")
            return redirect(url_for('carrera.dashboard'))
            
        # COMPROBAR SI YA ES FAVORITO
        es_favorito = Favorito.query.filter_by(user_id=current_user.id, nombre_jugador=nombre).first() is not None
            
        return render_template('perfil.html', jugador=datos_jugador[0], tier=tier_actual, es_favorito=es_favorito)
    except Exception as e:
        print(f"Error al cargar perfil: {e}")
        return redirect(url_for('carrera.dashboard'))

# ==========================================
# MOTOR DE FAVORITOS (AÑADIR/QUITAR)
# ==========================================
@carrera_bp.route('/favorito/<nombre>', methods=['POST'])
@login_required
def toggle_favorito(nombre):
    tier_actual = getattr(current_user, 'carrera_tier', current_user.tier)
    
    # Miramos si ya lo tiene guardado
    favorito_existente = Favorito.query.filter_by(user_id=current_user.id, nombre_jugador=nombre).first()
    
    if favorito_existente:
        # Si ya lo tiene, lo borramos
        db.session.delete(favorito_existente)
        db.session.commit()
        flash(f"{nombre} eliminado de tu libreta de seguimiento.")
    else:
        # Comprobamos el límite de 3 para cuentas gratis
        total_favoritos = Favorito.query.filter_by(user_id=current_user.id).count()
        
        if tier_actual == 'Aficionado' and total_favoritos >= 3:
            flash("Límite alcanzado. Mejora a Mánager Pro para seguir jugadores ilimitados.")
        else:
            nuevo_fav = Favorito(user_id=current_user.id, nombre_jugador=nombre)
            db.session.add(nuevo_fav)
            db.session.commit()
            flash(f"{nombre} añadido a tu libreta de seguimiento.")
            
    return redirect(url_for('carrera.perfil_jugador', nombre=nombre))

# ==========================================
# LA LIBRETA DEL MÁNAGER (MIS PROMESAS)
# ==========================================
@carrera_bp.route('/mis-promesas')
@login_required
def mis_promesas():
    tier_actual = getattr(current_user, 'carrera_tier', current_user.tier)
    
    # 1. Buscar los nombres de los jugadores guardados por este usuario
    favoritos_db = Favorito.query.filter_by(user_id=current_user.id).all()
    nombres_guardados = [fav.nombre_jugador for fav in favoritos_db]
    
    jugadores_favs = []
    try:
        if nombres_guardados:
            df = pd.read_csv('scouting_premium.csv')
            # 2. Filtrar el Excel para coger solo a los favoritos
            df_favs = df[df['Nombre'].isin(nombres_guardados)]
            jugadores_favs = df_favs.to_dict(orient='records')
    except Exception as e:
        print(f"Error cargando la libreta: {e}")

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