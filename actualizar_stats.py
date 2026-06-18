import json
from datos import jugadores

for j in jugadores:
    is_gk = j['Posición'] == 'POR'
    ovr = j['Media']
    
    if is_gk:
        j['Estirada'] = j.get('Ritmo', ovr + 2)
        j['Parada'] = j.get('Tiro', ovr - 1)
        j['Saque'] = j.get('Pase', ovr)
        j['Reflejos'] = j.get('Regate', ovr + 3)
        j['Velocidad_POR'] = j.get('Defensa', 45)
        j['Colocación'] = j.get('Físico', ovr - 2)
        
        # 4 Sub-atributos de POR
        j['Estirada_Sub'] = int(j['Estirada']) + 1
        j['Salto_POR'] = int(j['Estirada']) - 3
        j['Agilidad_POR'] = int(j['Reflejos']) - 2
        j['Elasticidad'] = int(j['Estirada']) + 2
        
        j['Paradas_Sub'] = int(j['Parada']) + 2
        j['Seguridad_POR'] = int(j['Parada']) - 1
        j['Blocaje'] = int(j['Parada']) + 3
        j['Anticipacion_POR'] = int(j['Colocación']) - 2
        
        j['Saque_Largo'] = int(j['Saque']) + 2
        j['Saque_Corto'] = int(j['Saque']) - 1
        j['Volea_POR'] = int(j['Saque']) - 4
        j['Vision_POR'] = int(j['Saque']) + 3
        
        j['Reflejos_Sub'] = int(j['Reflejos']) + 1
        j['Reaccion_POR'] = int(j['Reflejos']) - 2
        j['UnoVsUno'] = int(j['Reflejos']) + 3
        j['Recuperacion'] = int(j['Reflejos']) - 1
        
        j['Aceleracion_POR'] = int(j['Velocidad_POR']) + 3
        j['Sprint_POR'] = int(j['Velocidad_POR']) - 2
        j['Salidas'] = int(j['Velocidad_POR']) + 5
        j['Impulso'] = int(j['Velocidad_POR']) + 1
        
        j['Colocacion_Sub'] = int(j['Colocación']) + 2
        j['Posicionamiento_POR'] = int(j['Colocación']) + 1
        j['Cobertura'] = int(j['Colocación']) - 3
        j['Concentracion_POR'] = ovr - 2
        
    else:
        ritmo = int(j.get('Ritmo', ovr))
        tiro = int(j.get('Tiro', ovr - 5))
        pase = int(j.get('Pase', ovr - 2))
        regate = int(j.get('Regate', ovr + 1))
        defensa = int(j.get('Defensa', 50))
        fisico = int(j.get('Físico', 65))
        
        # 4 a 6 Sub-atributos de Jugador de Campo
        j['Aceleración'] = ritmo + 2 if j['Posición'] in ['EI', 'ED', 'LI', 'LD'] else ritmo - 1
        j['Vel_Sprint'] = ritmo - 2 if j['Posición'] in ['EI', 'ED'] else ritmo + 1
        j['Agilidad_Ritmo'] = regate + 2
        j['Reaccion_Ritmo'] = ovr - 1
        
        j['Posicionamiento'] = tiro + 5 if 'DC' in j['Posición'] else tiro - 2
        j['Finalización'] = tiro + 3 if 'DC' in j['Posición'] else tiro - 4
        j['Potencia_Tiro'] = tiro + 1
        j['Tiros_Lejanos'] = tiro - 2
        j['Voleas'] = tiro - 5
        j['Penaltis'] = tiro - 1
        
        j['Vision'] = pase + 3 if 'MCO' in j['Posición'] else pase - 1
        j['Centros'] = pase + 5 if j['Posición'] in ['EI', 'ED', 'LI', 'LD'] else pase - 4
        j['Faltas'] = pase - 3
        j['Pase_Corto'] = pase + 4 if 'MC' in j['Posición'] else pase + 1
        j['Pase_Largo'] = pase - 2
        j['Efecto'] = pase - 1
        
        j['Agilidad'] = regate + 4 if j['Posición'] in ['EI', 'ED', 'MCO'] else regate - 3
        j['Equilibrio'] = regate + 1
        j['Reacciones'] = ovr - 2
        j['Control_Balon'] = regate + 2
        j['Regates'] = regate + 3 if j['Posición'] in ['EI', 'ED'] else regate - 1
        j['Compostura'] = ovr - 3
        
        j['Intercepciones'] = defensa + 1
        j['Cabeza'] = defensa + 4 if 'DFC' in j['Posición'] else defensa - 5
        j['Marcaje'] = defensa - 1
        j['Robos'] = defensa + 2 if 'DFC' in j['Posición'] else defensa
        j['Entradas'] = defensa + 1
        
        j['Salto'] = fisico + 5 if 'DFC' in j['Posición'] else fisico - 2
        j['Resistencia'] = fisico + 8 if 'MC' in j['Posición'] or 'LI' in j['Posición'] else fisico + 1
        j['Fuerza'] = fisico + 5 if 'DFC' in j['Posición'] else fisico - 4
        j['Agresividad'] = fisico - 2

with open('datos.py', 'w', encoding='utf-8') as f:
    f.write('# ==========================================\n')
    f.write('# BASE DE DATOS DEFINITIVA (FC 26 - STATS Y SUB-STATS COMPLETAS)\n')
    f.write('# ==========================================\n\n')
    f.write('jugadores = [\n')
    for j in jugadores:
        f.write(f'    {json.dumps(j, ensure_ascii=False)},\n')
    f.write(']\n')

print("¡Hecho! Atributos desglosados e inyectados en datos.py")