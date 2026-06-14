import pandas as pd
import numpy as np

print("Iniciando motor de Business Analytics...")
df = pd.read_csv('scouting_data.csv')

# Conversiones básicas
df['Edad'] = pd.to_numeric(df['Edad'], errors='coerce')
df['Media'] = pd.to_numeric(df['Media'], errors='coerce')
df['Potencial'] = pd.to_numeric(df['Potencial'], errors='coerce')

def limpiar_dinero(valor):
    if pd.isna(valor) or valor == 'Desconocido': return 0
    valor_str = str(valor).replace('€', '').strip()
    try:
        if 'M' in valor_str: return float(valor_str.replace('M', '')) * 1000000
        elif 'K' in valor_str: return float(valor_str.replace('K', '')) * 1000
        return float(valor_str)
    except: return 0

df['Valor Real (€)'] = df['Valor'].apply(limpiar_dinero)
df['Sueldo Real (€)'] = df['Sueldo'].apply(limpiar_dinero)
df['Valor Seguro'] = df['Valor Real (€)'].replace(0, 1) 

# ---------------------------------------------------------
# LAS MÉTRICAS PREMIUM (El verdadero valor del producto)
# ---------------------------------------------------------

# 1. Margen Físico y Ganga Score
df['Margen de Crecimiento'] = df['Potencial'] - df['Media']
df['Ganga Score'] = ((df['Margen de Crecimiento'] * 1000000) / df['Valor Seguro']).round(2)

# 2. ROI Proyectado (%) - Retorno de Inversión
# Estima cuánto valdrá el jugador cuando alcance su potencial (crecimiento exponencial)
df['Valor Futuro Estimado'] = df['Valor Real (€)'] * ((df['Potencial'] / df['Media']) ** 2.5)
df['ROI (%)'] = (((df['Valor Futuro Estimado'] - df['Valor Real (€)']) / df['Valor Seguro']) * 100).round(0)

# 3. Coste Real Año 1 (Impacto en Presupuesto)
# Un fichaje "barato" puede arruinarte si su sueldo es altísimo. Esto suma el traspaso + 52 semanas de sueldo.
df['Coste Total Año 1 (€)'] = df['Valor Real (€)'] + (df['Sueldo Real (€)'] * 52)

# 4. Eficiencia Salarial (Rendimiento por Euro)
# ¿Cuántos puntos de media obtienes por cada 1.000€ de sueldo que pagas? Ideal para equipos pequeños.
df['Eficiencia Salarial'] = ((df['Media'] * 1000) / df['Sueldo Real (€)'].replace(0, 1)).round(2)

# 5. Ventana de Desarrollo (Años hasta el Prime)
# En el Modo Manager, el prime físico/técnico se suele alcanzar a los 27 años.
df['Años hasta Prime'] = 27 - df['Edad']
df['Años hasta Prime'] = df['Años hasta Prime'].apply(lambda x: 0 if x < 0 else x) # Si tiene más de 27, es 0

# 6. Inteligencia Artificial Básica: Etiquetado de Rol Automático
def asignar_rol(fila):
    if fila['Edad'] <= 21 and fila['Potencial'] >= 86:
        return "💎 Wonderkid (Fichar Ya)"
    elif fila['Edad'] > 31 and fila['Valor Real (€)'] == 0:
        return "👴 Veterano Libre"
    elif fila['ROI (%)'] > 300 and fila['Edad'] < 24:
        return "📈 Inversión Pura"
    elif fila['Eficiencia Salarial'] > 50 and fila['Media'] > 75:
        return "⚖️ Low-Cost Rentable"
    elif fila['Media'] >= 84:
        return "⭐ Titular Inmediato"
    else:
        return "🔄 Jugador de Rotación"

df['Perfil Analítico'] = df.apply(asignar_rol, axis=1)

# Ordenamos por las mejores oportunidades de mercado combinadas
df_premium = df.sort_values(by=['Ganga Score', 'ROI (%)'], ascending=[False, False])
df_premium.to_csv('scouting_premium.csv', index=False, encoding='utf-8')
print("¡Métricas inyectadas! El dataset es ahora nivel profesional.")