from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import pandas as pd

with sync_playwright() as p:
    print("Abriendo navegador...")
    browser = p.chromium.launch(headless=False) 
    page = browser.new_page()
    
    print("Entrando a SoFIFA... Resuelve el CAPTCHA si aparece.")
    page.goto("https://sofifa.com/players")
    
    try:
        page.wait_for_selector('table', timeout=60000)
        print("¡Muro destrozado! Extrayendo todos los datos financieros y deportivos...")
        html = page.content()
    except Exception as e:
        print("Tiempo agotado.")
        html = ""
    
    browser.close()

if html:
    soup = BeautifulSoup(html, 'html.parser')
    filas = soup.select('table tbody tr')
    
    # Creamos una lista vacía donde guardaremos el "oro"
    lista_jugadores = []
    
    for fila in filas:
        columnas = fila.find_all('td')
        
        # Nos aseguramos de que la fila tiene suficientes datos para no dar error
        if len(columnas) > 7:
            enlace_jugador = fila.find('a', href=lambda href: href and "/player/" in href)
            nombre = enlace_jugador.text.strip() if enlace_jugador else "Desconocido"
            
            # SoFIFA organiza los datos en estas columnas (td). Extraemos el texto limpio:
            try:
                edad = columnas[2].text.strip()
                media = columnas[3].text.strip()
                potencial = columnas[4].text.strip()
                valor = columnas[7].text.strip()
                sueldo = columnas[8].text.strip()
                
                # Guardamos cada jugador como un diccionario
                lista_jugadores.append({
                    "Nombre": nombre,
                    "Edad": edad,
                    "Media": media,
                    "Potencial": potencial,
                    "Valor": valor,
                    "Sueldo": sueldo
                })
            except IndexError:
                continue # Si hay un error en una fila rara, la salta y sigue trabajando
                
    # MAGIA ANALÍTICA: Convertimos la lista en un DataFrame de Pandas
    df = pd.DataFrame(lista_jugadores)
    
    # Exportamos a un archivo Excel/CSV
    df.to_csv("scouting_data.csv", index=False, encoding='utf-8')
    print(f"\n¡Éxito total! Se han guardado {len(df)} jugadores en 'scouting_data.csv'.")