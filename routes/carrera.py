import os
import io
import csv
import google.generativeai as genai
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, Response
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

        # 🔥 MISIÓN 3: SIMULADOR DE CAMBIO DE POSICIÓN
        pos_original = jugador_encontrado.get('Posición', 'POS').split(',')[0].strip()
        pos_simulada = request.args.get('simular_pos', pos_original)
        edad = int(jugador_encontrado.get('Edad', 20))
        margen = int(jugador_encontrado.get('Margen de Crecimiento', 0))

        roles_meta = {
            'POR': ['Portero Gato', 'Reflejos y Estirada'],
            'DFC': ['Defensa de Toque', 'Pase y Regate defensivo'],
            'LD': ['Carrilero Ofensivo', 'Ritmo y Centros'],
            'LI': ['Carrilero Ofensivo', 'Ritmo y Centros'],
            'MCD': ['Pivote Destructor', 'Físico y Defensa'],
            'MC': ['Box-to-Box', 'Resistencia y Llegada'],
            'MCO': ['Atacante en la Sombra', 'Tiro y Aceleración'],
            'ED': ['Extremo Invertido', 'Tiro y Regate'],
            'EI': ['Extremo Invertido', 'Tiro y Regate'],
            'DC': ['Cazagoles', 'Finalización y Posicionamiento'],
            'CAD': ['Carrilero Físico', 'Resistencia y Centros'],
            'CAI': ['Carrilero Físico', 'Resistencia y Centros']
        }
        
        rol_data = roles_meta.get(pos_simulada, ['Equilibrado', 'Todas las estadísticas'])
        
        # Penalización matemática si le cambias de posición
        penalizacion_semanas = 4 if pos_simulada != pos_original else 0
            
        if edad <= 22 and margen >= 5:
            intensidad = "Alta Intensidad (Acelerado)"
            color_int = "text-red-500"
            semanas_calc = max(2, 6 - (margen // 3)) + penalizacion_semanas
            semanas = str(semanas_calc)
        elif margen > 0:
            intensidad = "Desarrollo Normal"
            color_int = "text-green-500"
            semanas_calc = 5 + (edad - 20) // 2 + penalizacion_semanas
            semanas = str(semanas_calc)
        else:
            intensidad = "Plan de Conservación"
            color_int = "text-yellow-500"
            semanas = "Máx. Potencial" if pos_simulada == pos_original else f"{penalizacion_semanas} (Adaptación)"

        plan_entrenamiento = {
            "rol": rol_data[0],
            "enfoque": rol_data[1],
            "intensidad": intensidad,
            "color_int": color_int,
            "semanas": semanas,
            "pos_original": pos_original,
            "pos_simulada": pos_simulada
        }
                
        return render_template('perfil.html', 
                               jugador=jugador_encontrado, 
                               tier=tier_actual, 
                               es_favorito=es_favorito,
                               plan=plan_entrenamiento)
        
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        return f"<h2>Error 500</h2><pre>{error_trace}</pre>"

@carrera_bp.route('/favorito/<nombre>', methods=['POST'])
@login_required
def toggle_favorito(nombre):
    tier_actual = getattr(current_user, 'carrera_tier', current_user.tier)
    jugador_db = Jugador.query.filter_by(nombre=nombre).first()
    
    if not jugador_db:
        return redirect(request.referrer)

    fav = Favorito.query.filter_by(user_id=current_user.id, jugador_id=jugador_db.id).first()
    
    if fav:
        db.session.delete(fav)
    else:
        nuevo_fav = Favorito(user_id=current_user.id, jugador_id=jugador_db.id)
        db.session.add(nuevo_fav)
            
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

# 🔥 MISIÓN 1: EXPORTACIÓN DE BIG DATA (VIP)
@carrera_bp.route('/api/exportar-libreta')
@login_required
def exportar_libreta():
    tier_actual = getattr(current_user, 'carrera_tier', current_user.tier)
    if tier_actual != 'Clase Mundial':
        flash("La exportación de datos es exclusiva para el nivel Clase Mundial.")
        return redirect(url_for('carrera.mis_promesas'))
        
    favoritos_db = Favorito.query.filter_by(user_id=current_user.id).all()
    ids_guardados = [fav.jugador_id for fav in favoritos_db]
    jugadores_db = Jugador.query.filter(Jugador.id.in_(ids_guardados)).all()
    nombres_guardados = [j.nombre for j in jugadores_db]
    mis_jugadores = [j for j in datos_reales if j['Nombre'] in nombres_guardados]

    # Crear el archivo CSV en la memoria
    output = io.StringIO()
    writer = csv.writer(output, delimiter=';') # Usamos punto y coma para el Excel europeo
    writer.writerow(['Nombre', 'Edad', 'Posicion', 'OVR Actual', 'Potencial', 'Valor Mercado', 'Ganga Score'])
    
    for j in mis_jugadores:
        writer.writerow([
            j['Nombre'], 
            j['Edad'], 
            j.get('Posición', ''), 
            j['Media'], 
            j['Potencial'], 
            j.get('Valor Real (€)', 0), 
            j.get('Ganga Score', 0)
        ])
        
    return Response(output.getvalue(), 
                    mimetype="text/csv", 
                    headers={"Content-Disposition": "attachment;filename=Mis_Promesas_ScoutingPRO.csv"})

@carrera_bp.route('/comparar')
@login_required
def comparar():
    tier_actual = getattr(current_user, 'carrera_tier', current_user.tier)
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

@carrera_bp.route('/api/informe-ia/<nombre>')
@login_required
def informe_ia(nombre):
    tier_actual = getattr(current_user, 'carrera_tier', current_user.tier)
    if tier_actual not in ['Profesional', 'Clase Mundial']:
        return jsonify({"error": "🔒 Acceso Denegado. Mejora tu licencia a VIP."}), 403
        
    jugador = next((j for j in datos_reales if j['Nombre'] == nombre), None)
    api_key = os.environ.get("GEMINI_API_KEY")
    genai.configure(api_key=api_key)
    
    prompt = f"Actúa como Ojeador. Haz un reporte táctico breve de {jugador['Nombre']}, {jugador['Edad']} años, {jugador['Media']} OVR, Potencial {jugador['Potencial']}. Usa HTML <b> y <br>."
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(prompt)
        return jsonify({"informe": response.text.replace('```html', '').replace('```', '').strip()})
    except Exception as e:
        return jsonify({"error": "El ojeador está ocupado."}), 500

@carrera_bp.route('/pizarra')
@login_required
def pizarra_tactica():
    tier_actual = getattr(current_user, 'carrera_tier', current_user.tier)
    favoritos_db = Favorito.query.filter_by(user_id=current_user.id).all()
    ids_guardados = [fav.jugador_id for fav in favoritos_db]
    jugadores_db = Jugador.query.filter(Jugador.id.in_(ids_guardados)).all()
    nombres_guardados = [j.nombre for j in jugadores_db]
    mis_jugadores = [j for j in datos_reales if j['Nombre'] in nombres_guardados]

    return render_template('pizarra.html', tier=tier_actual, jugadores=mis_jugadores)