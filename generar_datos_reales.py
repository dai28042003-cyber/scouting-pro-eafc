import pandas as pd

# Datos reales de las mejores promesas de FC 24
datos_reales = [
    {"Nombre": "Jude Bellingham", "Edad": 20, "Media": 86, "Potencial": 91, "Posición": "MC", "Equipo": "Real Madrid", "Nacionalidad": "Inglaterra", "Valor Real (€)": 100000000, "Margen de Crecimiento": 5, "Ganga Score": 6.5, "ROI (%)": 120},
    {"Nombre": "Jamal Musiala", "Edad": 20, "Media": 86, "Potencial": 93, "Posición": "MCO", "Equipo": "Bayern Munich", "Nacionalidad": "Alemania", "Valor Real (€)": 110000000, "Margen de Crecimiento": 7, "Ganga Score": 7.0, "ROI (%)": 150},
    {"Nombre": "Pedri", "Edad": 20, "Media": 86, "Potencial": 92, "Posición": "MC", "Equipo": "FC Barcelona", "Nacionalidad": "España", "Valor Real (€)": 105000000, "Margen de Crecimiento": 6, "Ganga Score": 6.8, "ROI (%)": 135},
    {"Nombre": "Gavi", "Edad": 18, "Media": 83, "Potencial": 90, "Posición": "MC", "Equipo": "FC Barcelona", "Nacionalidad": "España", "Valor Real (€)": 65000000, "Margen de Crecimiento": 7, "Ganga Score": 8.2, "ROI (%)": 210},
    {"Nombre": "Florian Wirtz", "Edad": 20, "Media": 85, "Potencial": 91, "Posición": "MCO", "Equipo": "Bayer Leverkusen", "Nacionalidad": "Alemania", "Valor Real (€)": 80000000, "Margen de Crecimiento": 6, "Ganga Score": 7.5, "ROI (%)": 180},
    {"Nombre": "Alejandro Balde", "Edad": 19, "Media": 81, "Potencial": 89, "Posición": "LI", "Equipo": "FC Barcelona", "Nacionalidad": "España", "Valor Real (€)": 45000000, "Margen de Crecimiento": 8, "Ganga Score": 8.8, "ROI (%)": 250},
    {"Nombre": "Xavi Simons", "Edad": 20, "Media": 79, "Potencial": 89, "Posición": "MCO", "Equipo": "RB Leipzig", "Nacionalidad": "Países Bajos", "Valor Real (€)": 40000000, "Margen de Crecimiento": 10, "Ganga Score": 9.1, "ROI (%)": 310},
    {"Nombre": "Mathys Tel", "Edad": 18, "Media": 71, "Potencial": 86, "Posición": "DC", "Equipo": "Bayern Munich", "Nacionalidad": "Francia", "Valor Real (€)": 5000000, "Margen de Crecimiento": 15, "Ganga Score": 9.8, "ROI (%)": 550},
    {"Nombre": "Arthur Vermeeren", "Edad": 18, "Media": 71, "Potencial": 87, "Posición": "MCD", "Equipo": "Atlético de Madrid", "Nacionalidad": "Bélgica", "Valor Real (€)": 4500000, "Margen de Crecimiento": 16, "Ganga Score": 9.9, "ROI (%)": 620},
    {"Nombre": "Lamine Yamal", "Edad": 16, "Media": 76, "Potencial": 89, "Posición": "ED", "Equipo": "FC Barcelona", "Nacionalidad": "España", "Valor Real (€)": 16000000, "Margen de Crecimiento": 13, "Ganga Score": 9.5, "ROI (%)": 480}
]

df = pd.DataFrame(datos_reales)
df.to_csv('scouting_premium.csv', index=False, encoding='utf-8')
print("¡Archivo CSV creado con datos reales y codificación UTF-8 segura!")