import pandas as pd

# Datos reales de las mejores promesas proyectados y actualizados a 2026
datos_reales = [
    {"Nombre": "Lamine Yamal", "Edad": 18, "Media": 83, "Potencial": 93, "Posición": "ED", "Equipo": "FC Barcelona", "Nacionalidad": "España", "Valor Real (€)": 95000000, "Margen de Crecimiento": 10, "Ganga Score": 7.5, "ROI (%)": 160},
    {"Nombre": "Jude Bellingham", "Edad": 22, "Media": 90, "Potencial": 94, "Posición": "MCO", "Equipo": "Real Madrid", "Nacionalidad": "Inglaterra", "Valor Real (€)": 150000000, "Margen de Crecimiento": 4, "Ganga Score": 6.0, "ROI (%)": 90},
    {"Nombre": "Endrick", "Edad": 19, "Media": 80, "Potencial": 91, "Posición": "DC", "Equipo": "Real Madrid", "Nacionalidad": "Brasil", "Valor Real (€)": 55000000, "Margen de Crecimiento": 11, "Ganga Score": 8.5, "ROI (%)": 240},
    {"Nombre": "Warren Zaïre-Emery", "Edad": 20, "Media": 84, "Potencial": 91, "Posición": "MC", "Equipo": "PSG", "Nacionalidad": "Francia", "Valor Real (€)": 75000000, "Margen de Crecimiento": 7, "Ganga Score": 7.8, "ROI (%)": 180},
    {"Nombre": "Pau Cubarsí", "Edad": 19, "Media": 81, "Potencial": 90, "Posición": "DFC", "Equipo": "FC Barcelona", "Nacionalidad": "España", "Valor Real (€)": 50000000, "Margen de Crecimiento": 9, "Ganga Score": 8.7, "ROI (%)": 260},
    {"Nombre": "Florian Wirtz", "Edad": 23, "Media": 88, "Potencial": 92, "Posición": "MCO", "Equipo": "Bayer Leverkusen", "Nacionalidad": "Alemania", "Valor Real (€)": 110000000, "Margen de Crecimiento": 4, "Ganga Score": 6.8, "ROI (%)": 110},
    {"Nombre": "Jamal Musiala", "Edad": 23, "Media": 89, "Potencial": 93, "Posición": "MCO", "Equipo": "Bayern Munich", "Nacionalidad": "Alemania", "Valor Real (€)": 130000000, "Margen de Crecimiento": 4, "Ganga Score": 6.5, "ROI (%)": 105},
    {"Nombre": "Kobbie Mainoo", "Edad": 21, "Media": 82, "Potencial": 89, "Posición": "MCD", "Equipo": "Manchester United", "Nacionalidad": "Inglaterra", "Valor Real (€)": 60000000, "Margen de Crecimiento": 7, "Ganga Score": 8.1, "ROI (%)": 210},
    {"Nombre": "Mathys Tel", "Edad": 21, "Media": 81, "Potencial": 88, "Posición": "DC", "Equipo": "Bayern Munich", "Nacionalidad": "Francia", "Valor Real (€)": 45000000, "Margen de Crecimiento": 7, "Ganga Score": 8.3, "ROI (%)": 220},
    {"Nombre": "Alejandro Garnacho", "Edad": 21, "Media": 83, "Potencial": 89, "Posición": "EI", "Equipo": "Manchester United", "Nacionalidad": "Argentina", "Valor Real (€)": 65000000, "Margen de Crecimiento": 6, "Ganga Score": 7.9, "ROI (%)": 190}
]

df = pd.DataFrame(datos_reales)
df.to_csv('scouting_premium.csv', index=False, encoding='utf-8')
print("¡Archivo CSV actualizado a la Temporada 2026 con éxito!")