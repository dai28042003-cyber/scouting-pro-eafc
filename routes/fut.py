from flask import Blueprint, render_template
from flask_login import login_required, current_user

fut_bp = Blueprint('fut', __name__)

@fut_bp.route('/fut/dashboard')
@login_required
def fut_dashboard():
    # En el futuro, aquí conectaremos la API de precios en vivo de EA/FUTBIN
    
    html_temporal = f"""
    <div style="background-color: #030712; color: white; height: 100vh; display: flex; flex-direction: column; align-items: center; justify-content: center; font-family: sans-serif;">
        <h1 style="color: #22c55e; font-size: 3rem; margin-bottom: 10px;">TRADER ÉLITE - ULTIMATE TEAM</h1>
        <p style="color: #9ca3af; font-size: 1.2rem;">Conectando con el mercado de transferibles...</p>
        <div style="margin-top: 30px; padding: 20px; border: 1px solid #374151; border-radius: 10px; background-color: #111827;">
            Nivel actual: <strong>{current_user.tier}</strong>
        </div>
        <a href="/dashboard" style="margin-top: 30px; color: #60a5fa; text-decoration: none;">← Volver al Modo Carrera</a>
    </div>
    """
    
    # Restricción de acceso: Solo para el tier más alto o desarrollo
    if current_user.tier not in ['Clase Mundial', 'Trader Élite']:
        return "Acceso denegado. Necesitas el plan Trader Élite para entrar aquí.", 403
        
    return html_temporal