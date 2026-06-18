import json

# Importamos tu lista actual
from datos import jugadores

for j in jugadores:
    is_gk = j['Posición'] == 'POR'
    
    if is_gk:
        # Atributos principales de portero
        ovr = j['Media']
        j['Estirada'] = j.get('Ritmo', ovr + 2) # Reusamos los campos viejos que pegamos antes
        j['Parada'] = j.get('Tiro', ovr - 1)
        j['Saque'] = j.get('Pase', ovr)
        j['Reflejos'] = j.get('Regate', ovr + 3)
        j['Velocidad_POR'] = j.get('Defensa', 45)
        j['Colocación'] = j.get('Físico', ovr - 2)
        
        # Sub-atributos de portero
        j['Salto_POR'] = int(j['Estirada']) - 2
        j['Seguridad'] = int(j['Parada']) + 1
        j['Pase_Largo_POR'] = int(j['Saque']) - 1
        j['Reacción'] = int(j['Reflejos']) + 2
        j['Aceleración_POR'] = int(j['Velocidad_POR']) + 3
        j['Visión_POR'] = int(j['Colocación']) - 5
    else:
        # Sub-atributos de jugador de campo basados en sus stats base
        ritmo = int(j.get('Ritmo', j['Media']))
        tiro = int(j.get('Tiro', j['Media'] - 5))
        pase = int(j.get('Pase', j['Media'] - 2))
        regate = int(j.get('Regate', j['Media'] + 1))
        defensa = int(j.get('Defensa', 50))
        fisico = int(j.get('Físico', 65))
        
        j['Aceleración'] = ritmo + 2 if j['Posición'] in ['EI', 'ED', 'LI', 'LD'] else ritmo - 1
        j['Velocidad_Sprint'] = ritmo - 2 if j['Posición'] in ['EI', 'ED'] else ritmo + 1
        
        j['Finalización'] = tiro + 3 if 'DC' in j['Posición'] else tiro - 4
        j['Potencia_Tiro'] = tiro + 1
        j['Tiros_Lejanos'] = tiro - 2
        
        j['Pase_Corto'] = pase + 4 if 'MC' in j['Posición'] else pase + 1
        j['Pase_Largo'] = pase - 2
        j['Visión'] = pase + 3 if 'MCO' in j['Posición'] else pase - 1
        
        j['Agilidad'] = regate + 4 if j['Posición'] in ['EI', 'ED', 'MCO'] else regate - 3
        j['Equilibrio'] = regate + 1
        j['Control_Balón'] = regate + 2
        
        j['Robos'] = defensa + 2 if 'DFC' in j['Posición'] else defensa
        j['Entradas'] = defensa + 1
        j['Marcaje'] = defensa - 1
        
        j['Fuerza'] = fisico + 5 if 'DFC' in j['Posición'] else fisico - 4
        j['Resistencia'] = fisico + 8 if 'MC' in j['Posición'] or 'LI' in j['Posición'] else fisico + 1
        j['Agresividad'] = fisico - 2

# Guardar el nuevo archivo sobreescribiendo el viejo
with open('datos.py', 'w', encoding='utf-8') as f:
    f.write('# ==========================================\n')
    f.write('# BASE DE DATOS DEFINITIVA (FC 26 - STATS Y SUB-STATS COMPLETAS)\n')
    f.write('# ==========================================\n\n')
    f.write('jugadores = [\n')
    for j in jugadores:
        f.write(f'    {json.dumps(j, ensure_ascii=False)},\n')
    f.write(']\n')

print("¡Listo! Tu archivo datos.py ha sido inyectado con miles de sub-atributos nuevos.")