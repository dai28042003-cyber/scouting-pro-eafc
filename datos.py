import random

# ==========================================
# BASE DE DATOS DE PROMESAS REALES (FC 26)
# ==========================================

datos_reales = [
    {"Nombre": "Lamine Yamal", "Edad": 18, "Media": 84, "Potencial": 94, "Posición": "ED", "Equipo": "FC Barcelona", "Nacionalidad": "España", "Valor Real (€)": 110000000, "Margen de Crecimiento": 10, "Ganga Score": 7.8, "ROI (%)": 150},
    {"Nombre": "Jude Bellingham", "Edad": 22, "Media": 90, "Potencial": 95, "Posición": "MCO", "Equipo": "Real Madrid", "Nacionalidad": "Inglaterra", "Valor Real (€)": 160000000, "Margen de Crecimiento": 5, "Ganga Score": 6.2, "ROI (%)": 85},
    {"Nombre": "Florian Wirtz", "Edad": 23, "Media": 89, "Potencial": 93, "Posición": "MCO", "Equipo": "Bayer Leverkusen", "Nacionalidad": "Alemania", "Valor Real (€)": 120000000, "Margen de Crecimiento": 4, "Ganga Score": 6.5, "ROI (%)": 95},
    {"Nombre": "Jamal Musiala", "Edad": 23, "Media": 89, "Potencial": 94, "Posición": "MCO", "Equipo": "Bayern Munich", "Nacionalidad": "Alemania", "Valor Real (€)": 125000000, "Margen de Crecimiento": 5, "Ganga Score": 6.4, "ROI (%)": 100},
    {"Nombre": "Pedri", "Edad": 23, "Media": 88, "Potencial": 92, "Posición": "MC", "Equipo": "FC Barcelona", "Nacionalidad": "España", "Valor Real (€)": 105000000, "Margen de Crecimiento": 4, "Ganga Score": 6.6, "ROI (%)": 90},
    {"Nombre": "Eduardo Camavinga", "Edad": 23, "Media": 86, "Potencial": 92, "Posición": "MCD", "Equipo": "Real Madrid", "Nacionalidad": "Francia", "Valor Real (€)": 95000000, "Margen de Crecimiento": 6, "Ganga Score": 7.0, "ROI (%)": 110},
    {"Nombre": "Gavi", "Edad": 21, "Media": 85, "Potencial": 91, "Posición": "MC", "Equipo": "FC Barcelona", "Nacionalidad": "España", "Valor Real (€)": 88000000, "Margen de Crecimiento": 6, "Ganga Score": 7.3, "ROI (%)": 130},
    {"Nombre": "Warren Zaïre-Emery", "Edad": 20, "Media": 84, "Potencial": 92, "Posición": "MC", "Equipo": "PSG", "Nacionalidad": "Francia", "Valor Real (€)": 80000000, "Margen de Crecimiento": 8, "Ganga Score": 7.9, "ROI (%)": 165},
    {"Nombre": "Endrick", "Edad": 19, "Media": 81, "Potencial": 92, "Posición": "DC", "Equipo": "Real Madrid", "Nacionalidad": "Brasil", "Valor Real (€)": 60000000, "Margen de Crecimiento": 11, "Ganga Score": 8.4, "ROI (%)": 220},
    {"Nombre": "Pau Cubarsí", "Edad": 19, "Media": 82, "Potencial": 91, "Posición": "DFC", "Equipo": "FC Barcelona", "Nacionalidad": "España", "Valor Real (€)": 55000000, "Margen de Crecimiento": 9, "Ganga Score": 8.6, "ROI (%)": 240},
    {"Nombre": "Kobbie Mainoo", "Edad": 21, "Media": 83, "Potencial": 90, "Posición": "MCD", "Equipo": "Manchester United", "Nacionalidad": "Inglaterra", "Valor Real (€)": 65000000, "Margen de Crecimiento": 7, "Ganga Score": 8.0, "ROI (%)": 190},
    {"Nombre": "Alejandro Garnacho", "Edad": 21, "Media": 84, "Potencial": 90, "Posición": "EI", "Equipo": "Manchester United", "Nacionalidad": "Argentina", "Valor Real (€)": 70000000, "Margen de Crecimiento": 6, "Ganga Score": 7.7, "ROI (%)": 170},
    {"Nombre": "Xavi Simons", "Edad": 23, "Media": 86, "Potencial": 91, "Posición": "MCO", "Equipo": "RB Leipzig", "Nacionalidad": "Países Bajos", "Valor Real (€)": 85000000, "Margen de Crecimiento": 5, "Ganga Score": 7.1, "ROI (%)": 120},
    {"Nombre": "Savinho", "Edad": 22, "Media": 84, "Potencial": 90, "Posición": "ED", "Equipo": "Manchester City", "Nacionalidad": "Brasil", "Valor Real (€)": 72000000, "Margen de Crecimiento": 6, "Ganga Score": 7.8, "ROI (%)": 160},
    {"Nombre": "Bradley Barcola", "Edad": 23, "Media": 85, "Potencial": 90, "Posición": "EI", "Equipo": "PSG", "Nacionalidad": "Francia", "Valor Real (€)": 75000000, "Margen de Crecimiento": 5, "Ganga Score": 7.5, "ROI (%)": 140},
    {"Nombre": "Arda Güler", "Edad": 21, "Media": 82, "Potencial": 90, "Posición": "MCO", "Equipo": "Real Madrid", "Nacionalidad": "Turquía", "Valor Real (€)": 55000000, "Margen de Crecimiento": 8, "Ganga Score": 8.5, "ROI (%)": 250},
    {"Nombre": "João Neves", "Edad": 21, "Media": 83, "Potencial": 91, "Posición": "MC", "Equipo": "PSG", "Nacionalidad": "Portugal", "Valor Real (€)": 75000000, "Margen de Crecimiento": 8, "Ganga Score": 8.0, "ROI (%)": 195},
    {"Nombre": "Leny Yoro", "Edad": 20, "Media": 81, "Potencial": 90, "Posición": "DFC", "Equipo": "Manchester United", "Nacionalidad": "Francia", "Valor Real (€)": 50000000, "Margen de Crecimiento": 9, "Ganga Score": 8.8, "ROI (%)": 260},
    {"Nombre": "Jarrad Branthwaite", "Edad": 23, "Media": 84, "Potencial": 89, "Posición": "DFC", "Equipo": "Everton", "Nacionalidad": "Inglaterra", "Valor Real (€)": 65000000, "Margen de Crecimiento": 5, "Ganga Score": 7.5, "ROI (%)": 145},
    {"Nombre": "Evan Ferguson", "Edad": 21, "Media": 82, "Potencial": 89, "Posición": "DC", "Equipo": "Brighton", "Nacionalidad": "Irlanda", "Valor Real (€)": 52000000, "Margen de Crecimiento": 7, "Ganga Score": 8.2, "ROI (%)": 210},
    {"Nombre": "Giorgio Scalvini", "Edad": 22, "Media": 83, "Potencial": 89, "Posición": "DFC", "Equipo": "Atalanta", "Nacionalidad": "Italia", "Valor Real (€)": 58000000, "Margen de Crecimiento": 6, "Ganga Score": 7.9, "ROI (%)": 175},
    {"Nombre": "Destiny Udogie", "Edad": 23, "Media": 85, "Potencial": 89, "Posición": "LI", "Equipo": "Tottenham", "Nacionalidad": "Italia", "Valor Real (€)": 68000000, "Margen de Crecimiento": 4, "Ganga Score": 7.3, "ROI (%)": 130},
    {"Nombre": "Rico Lewis", "Edad": 21, "Media": 82, "Potencial": 89, "Posición": "LD", "Equipo": "Manchester City", "Nacionalidad": "Inglaterra", "Valor Real (€)": 56000000, "Margen de Crecimiento": 7, "Ganga Score": 8.1, "ROI (%)": 205},
    {"Nombre": "Antonio Silva", "Edad": 22, "Media": 83, "Potencial": 89, "Posición": "DFC", "Equipo": "Benfica", "Nacionalidad": "Portugal", "Valor Real (€)": 62000000, "Margen de Crecimiento": 6, "Ganga Score": 7.8, "ROI (%)": 165},
    {"Nombre": "Mathys Tel", "Edad": 21, "Media": 82, "Potencial": 89, "Posición": "DC", "Equipo": "Bayern Munich", "Nacionalidad": "Francia", "Valor Real (€)": 48000000, "Margen de Crecimiento": 7, "Ganga Score": 8.3, "ROI (%)": 225},
    {"Nombre": "Arthur Vermeeren", "Edad": 21, "Media": 80, "Potencial": 88, "Posición": "MCD", "Equipo": "Atlético de Madrid", "Nacionalidad": "Bélgica", "Valor Real (€)": 38000000, "Margen de Crecimiento": 8, "Ganga Score": 8.9, "ROI (%)": 290},
    {"Nombre": "Jorrel Hato", "Edad": 20, "Media": 79, "Potencial": 89, "Posición": "DFC", "Equipo": "Ajax", "Nacionalidad": "Países Bajos", "Valor Real (€)": 32000000, "Margen de Crecimiento": 10, "Ganga Score": 9.3, "ROI (%)": 370},
    {"Nombre": "Ousmane Diomande", "Edad": 22, "Media": 82, "Potencial": 88, "Posición": "DFC", "Equipo": "Sporting CP", "Nacionalidad": "Costa de Marfil", "Valor Real (€)": 42000000, "Margen de Crecimiento": 6, "Ganga Score": 8.4, "ROI (%)": 210},
    {"Nombre": "Johan Bakayoko", "Edad": 23, "Media": 83, "Potencial": 88, "Posición": "ED", "Equipo": "PSV", "Nacionalidad": "Bélgica", "Valor Real (€)": 45000000, "Margen de Crecimiento": 5, "Ganga Score": 8.0, "ROI (%)": 180},
    {"Nombre": "Harvey Elliott", "Edad": 23, "Media": 82, "Potencial": 87, "Posición": "MCO", "Equipo": "Liverpool", "Nacionalidad": "Inglaterra", "Valor Real (€)": 44000000, "Margen de Crecimiento": 5, "Ganga Score": 7.9, "ROI (%)": 160},
    {"Nombre": "Oscar Gloukh", "Edad": 22, "Media": 80, "Potencial": 87, "Posición": "MCO", "Equipo": "RB Salzburg", "Nacionalidad": "Israel", "Valor Real (€)": 36000000, "Margen de Crecimiento": 7, "Ganga Score": 8.7, "ROI (%)": 260},
    {"Nombre": "Antonio Nusa", "Edad": 21, "Media": 79, "Potencial": 88, "Posición": "EI", "Equipo": "RB Leipzig", "Nacionalidad": "Noruega", "Valor Real (€)": 32000000, "Margen de Crecimiento": 9, "Ganga Score": 9.2, "ROI (%)": 330},
    {"Nombre": "Désiré Doué", "Edad": 21, "Media": 80, "Potencial": 89, "Posición": "MI", "Equipo": "PSG", "Nacionalidad": "Francia", "Valor Real (€)": 38000000, "Margen de Crecimiento": 9, "Ganga Score": 9.0, "ROI (%)": 310},
    {"Nombre": "Guillaume Restes", "Edad": 21, "Media": 79, "Potencial": 88, "Posición": "POR", "Equipo": "Toulouse", "Nacionalidad": "Francia", "Valor Real (€)": 28000000, "Margen de Crecimiento": 9, "Ganga Score": 9.4, "ROI (%)": 360},
    {"Nombre": "Bart Verbruggen", "Edad": 23, "Media": 82, "Potencial": 88, "Posición": "POR", "Equipo": "Brighton", "Nacionalidad": "Países Bajos", "Valor Real (€)": 35000000, "Margen de Crecimiento": 6, "Ganga Score": 8.2, "ROI (%)": 190},
    {"Nombre": "Valentin Barco", "Edad": 21, "Media": 78, "Potencial": 87, "Posición": "LI", "Equipo": "Sevilla FC", "Nacionalidad": "Argentina", "Valor Real (€)": 24000000, "Margen de Crecimiento": 9, "Ganga Score": 9.3, "ROI (%)": 350},
    {"Nombre": "Claudio Echeverri", "Edad": 20, "Media": 78, "Potencial": 89, "Posición": "MCO", "Equipo": "River Plate", "Nacionalidad": "Argentina", "Valor Real (€)": 26000000, "Margen de Crecimiento": 11, "Ganga Score": 9.6, "ROI (%)": 430},
    {"Nombre": "Oscar Bobb", "Edad": 22, "Media": 80, "Potencial": 87, "Posición": "ED", "Equipo": "Manchester City", "Nacionalidad": "Noruega", "Valor Real (€)": 34000000, "Margen de Crecimiento": 7, "Ganga Score": 8.6, "ROI (%)": 250},
    {"Nombre": "Stefan Bajcetic", "Edad": 21, "Media": 79, "Potencial": 87, "Posición": "MCD", "Equipo": "RB Salzburg", "Nacionalidad": "España", "Valor Real (€)": 28000000, "Margen de Crecimiento": 8, "Ganga Score": 9.1, "ROI (%)": 320},
    {"Nombre": "Conor Bradley", "Edad": 22, "Media": 81, "Potencial": 87, "Posición": "LD", "Equipo": "Liverpool", "Nacionalidad": "Irlanda del Norte", "Valor Real (€)": 32000000, "Margen de Crecimiento": 6, "Ganga Score": 8.5, "ROI (%)": 220},
    {"Nombre": "Jarell Quansah", "Edad": 23, "Media": 81, "Potencial": 87, "Posición": "DFC", "Equipo": "Liverpool", "Nacionalidad": "Inglaterra", "Valor Real (€)": 30000000, "Margen de Crecimiento": 6, "Ganga Score": 8.4, "ROI (%)": 210},
    {"Nombre": "Kenan Yildiz", "Edad": 21, "Media": 80, "Potencial": 89, "Posición": "SD", "Equipo": "Juventus", "Nacionalidad": "Turquía", "Valor Real (€)": 38000000, "Margen de Crecimiento": 9, "Ganga Score": 9.0, "ROI (%)": 340},
    {"Nombre": "Matias Soulé", "Edad": 23, "Media": 83, "Potencial": 88, "Posición": "ED", "Equipo": "Roma", "Nacionalidad": "Argentina", "Valor Real (€)": 42000000, "Margen de Crecimiento": 5, "Ganga Score": 8.1, "ROI (%)": 190},
    {"Nombre": "Vitor Roque", "Edad": 21, "Media": 80, "Potencial": 89, "Posición": "DC", "Equipo": "Real Betis", "Nacionalidad": "Brasil", "Valor Real (€)": 34000000, "Margen de Crecimiento": 9, "Ganga Score": 8.9, "ROI (%)": 300},
    {"Nombre": "Lucas Beraldo", "Edad": 22, "Media": 81, "Potencial": 88, "Posición": "DFC", "Equipo": "PSG", "Nacionalidad": "Brasil", "Valor Real (€)": 38000000, "Margen de Crecimiento": 7, "Ganga Score": 8.3, "ROI (%)": 220},
    {"Nombre": "Levi Colwill", "Edad": 23, "Media": 83, "Potencial": 88, "Posición": "DFC", "Equipo": "Chelsea", "Nacionalidad": "Inglaterra", "Valor Real (€)": 45000000, "Margen de Crecimiento": 5, "Ganga Score": 7.9, "ROI (%)": 170},
    {"Nombre": "Gianluca Prestianni", "Edad": 20, "Media": 77, "Potencial": 87, "Posición": "ED", "Equipo": "Benfica", "Nacionalidad": "Argentina", "Valor Real (€)": 14000000, "Margen de Crecimiento": 10, "Ganga Score": 9.6, "ROI (%)": 490},
    {"Nombre": "Kendry Páez", "Edad": 19, "Media": 76, "Potencial": 89, "Posición": "MC", "Equipo": "Ind. del Valle", "Nacionalidad": "Ecuador", "Valor Real (€)": 16000000, "Margen de Crecimiento": 13, "Ganga Score": 9.7, "ROI (%)": 530},
    {"Nombre": "Estevão Willian", "Edad": 19, "Media": 77, "Potencial": 90, "Posición": "ED", "Equipo": "Palmeiras", "Nacionalidad": "Brasil", "Valor Real (€)": 19000000, "Margen de Crecimiento": 13, "Ganga Score": 9.8, "ROI (%)": 560},
    {"Nombre": "Franco Mastantuono", "Edad": 18, "Media": 75, "Potencial": 89, "Posición": "MCO", "Equipo": "River Plate", "Nacionalidad": "Argentina", "Valor Real (€)": 15000000, "Margen de Crecimiento": 14, "Ganga Score": 9.9, "ROI (%)": 620},
    {"Nombre": "Roony Bardghji", "Edad": 20, "Media": 77, "Potencial": 87, "Posición": "ED", "Equipo": "FC Copenhague", "Nacionalidad": "Suecia", "Valor Real (€)": 16000000, "Margen de Crecimiento": 10, "Ganga Score": 9.5, "ROI (%)": 410},
    {"Nombre": "Lewis Miley", "Edad": 20, "Media": 78, "Potencial": 88, "Posición": "MC", "Equipo": "Newcastle", "Nacionalidad": "Inglaterra", "Valor Real (€)": 18000000, "Margen de Crecimiento": 10, "Ganga Score": 9.4, "ROI (%)": 420},
    {"Nombre": "Archie Gray", "Edad": 20, "Media": 78, "Potencial": 88, "Posición": "MC", "Equipo": "Tottenham", "Nacionalidad": "Inglaterra", "Valor Real (€)": 22000000, "Margen de Crecimiento": 10, "Ganga Score": 9.5, "ROI (%)": 390},
    {"Nombre": "Ethan Nwaneri", "Edad": 19, "Media": 74, "Potencial": 89, "Posición": "MCO", "Equipo": "Arsenal", "Nacionalidad": "Inglaterra", "Valor Real (€)": 12000000, "Margen de Crecimiento": 15, "Ganga Score": 9.9, "ROI (%)": 660},
    {"Nombre": "Mikey Moore", "Edad": 18, "Media": 72, "Potencial": 88, "Posición": "EI", "Equipo": "Tottenham", "Nacionalidad": "Inglaterra", "Valor Real (€)": 8000000, "Margen de Crecimiento": 16, "Ganga Score": 9.9, "ROI (%)": 720},
    {"Nombre": "Francesco Camarda", "Edad": 18, "Media": 73, "Potencial": 89, "Posición": "DC", "Equipo": "AC Milan", "Nacionalidad": "Italia", "Valor Real (€)": 9000000, "Margen de Crecimiento": 16, "Ganga Score": 9.9, "ROI (%)": 700},
    {"Nombre": "Jamie Bynoe-Gittens", "Edad": 21, "Media": 80, "Potencial": 87, "Posición": "MI", "Equipo": "Borussia Dortmund", "Nacionalidad": "Inglaterra", "Valor Real (€)": 24000000, "Margen de Crecimiento": 7, "Ganga Score": 8.8, "ROI (%)": 290},
    {"Nombre": "Youssoufa Moukoko", "Edad": 21, "Media": 79, "Potencial": 87, "Posición": "DC", "Equipo": "OGC Niza", "Nacionalidad": "Alemania", "Valor Real (€)": 22000000, "Margen de Crecimiento": 8, "Ganga Score": 8.9, "ROI (%)": 310},
    {"Nombre": "Marcos Leonardo", "Edad": 23, "Media": 81, "Potencial": 86, "Posición": "DC", "Equipo": "Al Hilal", "Nacionalidad": "Brasil", "Valor Real (€)": 25000000, "Margen de Crecimiento": 5, "Ganga Score": 8.2, "ROI (%)": 190}
]

# ==========================================
# GENERADOR AUTOMÁTICO DE TALENTOS OCULTOS
# (Para llegar a 200 jugadores de forma dinámica)
# ==========================================

random.seed(42) # Usamos una semilla para que los falsos sean siempre los mismos

equipos_extra = ["Ajax", "PSV", "Sporting CP", "Benfica", "Porto", "Feyenoord", "Brugge", "Anderlecht", "Boca Juniors", "Palmeiras", "Flamengo"]
paises_extra = ["Francia", "Brasil", "Argentina", "España", "Inglaterra", "Alemania", "Portugal", "Países Bajos", "Bélgica", "Italia", "Croacia", "Uruguay"]
posiciones_extra = ["DFC", "LI", "LD", "MC", "MCD", "MCO", "EI", "ED", "DC"]
nombres_base = ["Joao", "Matias", "Lucas", "Hugo", "Enzo", "Liam", "Noah", "Leo", "Theo", "Arthur", "Milan", "Luka", "Ivan", "Diego"]
apellidos_base = ["Silva", "García", "Fernandes", "Müller", "Dubois", "Rossi", "Smith", "Johnson", "Kovac", "Popov", "Costa", "Santos"]

for i in range(1, 141):
    nombre = f"{random.choice(nombres_base)} {random.choice(apellidos_base)} {i}"
    edad = random.randint(16, 21)
    media = random.randint(65, 75)
    potencial = random.randint(84, 88)
    posicion = random.choice(posiciones_extra)
    equipo = random.choice(equipos_extra)
    nacionalidad = random.choice(paises_extra)
    valor = random.randint(1500000, 8000000)
    margen = potencial - media
    ganga = round(random.uniform(8.0, 9.8), 1)
    roi = margen * random.randint(20, 45)
    
    datos_reales.append({
        "Nombre": nombre,
        "Edad": edad,
        "Media": media,
        "Potencial": potencial,
        "Posición": posicion,
        "Equipo": equipo,
        "Nacionalidad": nacionalidad,
        "Valor Real (€)": valor,
        "Margen de Crecimiento": margen,
        "Ganga Score": ganga,
        "ROI (%)": roi
    })