import pandas as pd
import random

print("Leyendo la base de datos...")
# Leer tu archivo actual
df = pd.read_csv('scouting_premium.csv')

# Añadir las columnas que falten con datos simulados si no existen
if 'Posición' not in df.columns:
    df['Posición'] = [random.choice(['POR', 'DFC', 'LI', 'LD', 'MC', 'MCO', 'ED', 'EI', 'DC']) for _ in range(len(df))]

if 'Equipo' not in df.columns:
    df['Equipo'] = [random.choice(['FC Barcelona', 'Real Madrid', 'Manchester City', 'Bayern Munich', 'Arsenal', 'AC Milan']) for _ in range(len(df))]

if 'Nacionalidad' not in df.columns:
    df['Nacionalidad'] = [random.choice(['España', 'Francia', 'Brasil', 'Argentina', 'Inglaterra', 'Alemania']) for _ in range(len(df))]

if 'Ganga Score' not in df.columns:
    df['Ganga Score'] = [round(random.uniform(7.5, 9.9), 1) for _ in range(len(df))]

if 'ROI (%)' not in df.columns:
    df['ROI (%)'] = [random.randint(150, 600) for _ in range(len(df))]

# Sobrescribir el archivo corregido
df.to_csv('scouting_premium.csv', index=False)
print("¡Archivo CSV actualizado con éxito! Ya tienes todos los datos.")