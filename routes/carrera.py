from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
import pandas as pd
from models import db

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
    try:
        df = pd.read_csv('scouting_premium.csv')
        
        edad_max = request.args.get('edad_max', default=40, type=int)
        presupuesto_max = request.args.get('presupuesto_max', default=1000000000, type=float)
        
        df_filtrado = df[(df['Edad'] <= edad_max) & (df['Valor Real (€)'] <= presupuesto_max)]
        
        if 'Ganga Score' in df_filtrado.columns and 'ROI (%)' in df_filtrado.columns:
            df_filtrado = df_filtrado.sort_values(by=['Ganga Score', 'ROI (%)'], ascending=[False, False])
        
        if current_user.tier == 'Aficionado':
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
                           tier=current_user.tier, 
                           graficos=graficos,
                           edad_max=edad_max,
                           presupuesto_max=presupuesto_max)

@carrera_bp.route('/jugador/<nombre>')
@login_required
def perfil_jugador(nombre):
    try:
        df = pd.read_csv('scouting_premium.csv')
        datos_jugador = df[df['Nombre'] == nombre].to_dict(orient='records')
        
        if not datos_jugador:
            flash("Jugador no encontrado en la base de datos.")
            return redirect(url_for('carrera.dashboard'))
            
        return render_template('perfil.html', jugador=datos_jugador[0], tier=current_user.tier)
    except Exception as e:
        print(f"Error al cargar perfil: {e}")
        return redirect(url_for('carrera.dashboard'))

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
        current_user.tier = nivel_formateado
        db.session.commit()
        flash(f'Modo Dios activado: Ahora eres {nivel_formateado}')
    
    return redirect(url_for('carrera.dashboard'))