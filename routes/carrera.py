import os
import google.generativeai as genai
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from models import db, Favorito, Jugador
from datos import jugadores as datos_reales

carrera_bp = Blueprint('carrera', __name__)

@carrera_bp.route('/demo')
def demo():
    jugadores = datos_reales[:10]
    return render_template('index.html', jugadores=jugadores, demo_mode=True)

@carrera_bp.route('/dashboard')
@login_required
def dashboard():
    tier_actual = getattr(current_user, 'carrera_tier', current_user.tier)
    edad_max = request.args.get('edad_max', default=40, type=int)
    presupuesto_max = request.args.get('presupuesto_max', default=1000000000, type=float)
    
    df_filtrado = [j for j in datos_reales if j['Edad'] <= edad_max and j['Valor Real (€)'] <= presupuesto_max]
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
        jugador_encontrado = next((j for j in datos_reales if j['Nombre'] == nombre), None)
        
        if not jugador_encontrado:
            flash("Jugador no encontrado en la base de datos.")
            return redirect(url_for('carrera.dashboard'))
            
        jugador_db = Jugador.query.filter_by(nombre=nombre).first()
        es_favorito = False
        if jugador_db:
            es_favorito = Favorito.query.filter_by(user_id=current_user.id, jugador_id=jugador_db.id).first() is not None
                
        return render_template('perfil.html', jugador=jugador_encontrado, tier=tier_actual, es_favorito=es_favorito)
        
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        return f"""
        <div style='background:#111; color:#ff4444; padding:30px; font-family:monospace; font-size:16px; line-height:1.5; min-height:100vh;'>
            <h2 style='color:white; margin-bottom:20px; font-family:sans-serif;'>🚨 Autopsia del Error 500 🚨</h2>
            <pre style='background:#000; padding:20px; overflow-x:auto; border:1px solid #ff4444;'>{error_trace}</pre>
        </div>
        """

@carrera_bp.route('/favorito/<nombre>', methods=['POST'])
@login_required
def toggle_favorito(nombre):
    tier_actual = getattr(current_user, 'carrera_tier', current_user.tier)
    jugador_db = Jugador.query.filter_by(nombre=nombre).first()
    
    if not jugador_db:
        flash("Error: El jugador no existe en la base de datos principal.")
        return redirect(request.referrer)

    fav = Favorito.query.filter_by(user_id=current_user.id, jugador_id=jugador_db.id).first()
    
    if fav:
        db.session.delete(fav)
        flash(f"Has quitado a {nombre} de tu libreta.")
    else:
        total_favoritos = Favorito.query.filter_by(user_id=current_user.id).count()
        if tier_actual == 'Aficionado' and total_favoritos >= 3:
            flash("Límite alcanzado. Mejora a Mánager Pro para seguir jugadores ilimitados.")
        else:
            nuevo_fav = Favorito(user_id=current_user.id, jugador_id=jugador_db.id)
            db.session.add(nuevo_fav)
            flash(f"Has guardado a {nombre} en tu libreta.")
            
    db.session.commit()
    return redirect(request.referrer)

@carrera_bp.route('/mis-promesas')
@login_required
def mis_promesas():
    tier_actual = getattr(current_user, 'carrera_tier', current_user.tier)
    favoritos_db = Favorito.query.filter_by(user_id=current_user.id).all()
    ids_guardados = [fav.jugador_id for fav in favoritos_db]
    
    jugadores_db = Jugador.query.filter(Jugador.id.in_(ids_guardados)).all()
    nombres_guardados = [j.nombre for j in jugadores_db]
    jugadores_favs = [j for j in datos_reales if j['Nombre'] in nombres_guardados]

    return render_template('mis_promesas.html', jugadores=jugadores_favs, tier=tier_actual)

@carrera_bp.route('/comparar')
@login_required
def comparar():
    tier_actual = getattr(current_user, 'carrera_tier', current_user.tier)
    if tier_actual == 'Aficionado':
        flash("La herramienta de comparación avanzada es exclusiva para miembros PRO o Clase Mundial.")
        return redirect(url_for('carrera.dashboard'))
        
    p1_nombre = request.args.get('p1')
    p2_nombre = request.args.get('p2')
    jugador1 = next((j for j in datos_reales if j['Nombre'] == p1_nombre), None) if p1_nombre else None
    jugador2 = next((j for j in datos_reales if j['Nombre'] == p2_nombre), None) if p2_nombre else None
        
    return render_template('comparador.html', jugadores=datos_reales, j1=jugador1, j2=jugador2, tier=tier_actual)

@carrera_bp.route('/mi-perfil')
@login_required
def mi_perfil():
    tier_actual = getattr(current_user, 'carrera_tier', current_user.tier)
    total_favoritos = Favorito.query.filter_by(user_id=current_user.id).count()
    return render_template('mi_perfil.html', tier=tier_actual, total_favoritos=total_favoritos)

# -------------------------------------------------------------------
# NUEVA RUTA: INFORME DE OJEADOR IA (MISIÓN B)
# -------------------------------------------------------------------
@carrera_bp.route('/api/informe-ia/<nombre>')
@login_required
def informe_ia(nombre):
    tier_actual = getattr(current_user, 'carrera_tier', current_user.tier)
    
    # 1. Filtro de exclusividad: Solo VIPs
    if tier_actual not in ['Profesional', 'Clase Mundial']:
        return jsonify({"error": "🔒 Acceso Denegado. Mejora tu licencia a VIP para contactar con el Ojeador IA."}), 403
        
    jugador = next((j for j in datos_reales if j['Nombre'] == nombre), None)
    if not jugador:
        return jsonify({"error": "Jugador no encontrado."}), 404

    # 2. Configurar llave de Gemini
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return jsonify({"error": "Error del servidor: API Key no configurada."}), 500
        
    genai.configure(api_key=api_key)
    
    # 3. El Prompt del Director Deportivo
    prompt = f"""
    Actúa como el Ojeador Jefe de un club de fútbol de élite. Redacta un informe de ojeo directo, clínico y profesional sobre esta promesa (máximo 120 palabras). 
    
    Datos a evaluar:
    - Nombre: {jugador['Nombre']} ({jugador.get('Posición', 'POS')})
    - Edad: {jugador['Edad']} años
    - Calidad: {jugador['Media']} OVR -> Potencial: {jugador['Potencial']}
    - Precio estimado: {jugador.get('Valor Real (€)', 0)}€
    - Ganga Score (0-10): {jugador.get('Ganga Score', 0)} (indica si está barato para su potencial).
    
    Escribe 3 párrafos cortos: 
    1. Perfil técnico y potencial de crecimiento.
    2. Evaluación económica (¿Es un precio justo?).
    3. Veredicto final: ¿Recomiendas ficharlo?
    
    No uses Markdown tradicional como asteriscos. Usa únicamente etiquetas HTML <b> para negritas y <br> para separar párrafos.
    """
    
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        
        # Limpiamos el texto para inyectarlo en el HTML directamente
        texto_limpio = response.text.replace('```html', '').replace('```', '').strip()
        texto_limpio = texto_limpio.replace('\n', '<br>')
        
        return jsonify({"informe": texto_limpio})
    except Exception as e:
        # 🔥 QUitamos el mensaje amistoso temporalmente para ver qué falla:
        return jsonify({"error": f"Error de Google: {str(e)}"}), 500