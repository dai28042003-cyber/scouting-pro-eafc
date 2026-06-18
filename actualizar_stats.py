import json
from datos import jugadores

for j in jugadores:
    is_gk = j['Posición'] == 'POR'
    ovr = j['Media']
    
    if is_gk:
        # Atributos principales de portero
        j['Estirada'] = j.get('Ritmo', ovr + 2)
        j['Parada'] = j.get('Tiro', ovr - 1)
        j['Saque'] = j.get('Pase', ovr)
        j['Reflejos'] = j.get('Regate', ovr + 3)
        j['Velocidad_POR'] = j.get('Defensa', 45)
        j['Colocación'] = j.get('Físico', ovr - 2)
        
        # Sub-atributos de portero
        j['Estirada_Sub'] = int(j['Estirada']) + 1
        j['Parada_Sub'] = int(j['Parada'])
        j['Saque_Sub'] = int(j['Saque'])
        j['Reflejos_Sub'] = int(j['Reflejos']) + 1
        j['Reacción'] = int(j['Reflejos']) - 2
        j['Aceleración_POR'] = int(j['Velocidad_POR']) + 2
        j['Vel_Sprint_POR'] = int(j['Velocidad_POR']) - 2
        j['Colocación_Sub'] = int(j['Colocación'])
    else:
        # Atributos principales jugador de campo
        ritmo = int(j.get('Ritmo', ovr))
        tiro = int(j.get('Tiro', ovr - 5))
        pase = int(j.get('Pase', ovr - 2))
        regate = int(j.get('Regate', ovr + 1))
        defensa = int(j.get('Defensa', 50))
        fisico = int(j.get('Físico', 65))
        
        # Ritmo
        j['Aceleración'] = ritmo + 2 if j['Posición'] in ['EI', 'ED', 'LI', 'LD'] else ritmo - 1
        j['Velocidad_Sprint'] = ritmo - 2 if j['Posición'] in ['EI', 'ED'] else ritmo + 1
        
        # Tiro
        j['Posicionamiento'] = tiro + 5 if 'DC' in j['Posición'] else tiro - 2
        j['Finalización'] = tiro + 3 if 'DC' in j['Posición'] else tiro - 4
        j['Potencia_Tiro'] = tiro + 1
        j['Tiros_Lejanos'] = tiro - 2
        j['Voleas'] = tiro - 5
        j['Penaltis'] = tiro - 1
        
        # Pase
        j['Visión'] = pase + 3 if 'MCO' in j['Posición'] else pase - 1
        j['Centros'] = pase + 5 if j['Posición'] in ['EI', 'ED', 'LI', 'LD'] else pase - 4
        j['Precisión_Falta'] = pase - 3
        j['Pase_Corto'] = pase + 4 if 'MC' in j['Posición'] else pase + 1
        j['Pase_Largo'] = pase - 2
        j['Efecto'] = pase - 1
        
        # Regate
        j['Agilidad'] = regate + 4 if j['Posición'] in ['EI', 'ED', 'MCO'] else regate - 3
        j['Equilibrio'] = regate + 1
        j['Reacciones'] = ovr - 2
        j['Control_Balón'] = regate + 2
        j['Regates'] = regate + 3 if j['Posición'] in ['EI', 'ED'] else regate - 1
        j['Compostura'] = ovr - 3
        
        # Defensa
        j['Intercepciones'] = defensa + 1
        j['Precisión_Cabeza'] = defensa + 4 if 'DFC' in j['Posición'] else defensa - 5
        j['Marcaje'] = defensa - 1
        j['Robos'] = defensa + 2 if 'DFC' in j['Posición'] else defensa
        j['Entradas'] = defensa + 1
        
        # Físico
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