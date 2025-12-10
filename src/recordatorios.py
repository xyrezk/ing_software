import sqlite3
from datetime import datetime, timedelta
from database import get_connection

def convertir_formato_fecha(fecha_str):
    if not fecha_str:
        return None
    fecha_str = str(fecha_str).strip()
    try:
        if '-' in fecha_str:
            partes = fecha_str.split('-')
            if len(partes) == 3:
                if len(partes[2]) == 4:
                    fecha = datetime(int(partes[2]), int(partes[1]), int(partes[0]))
                    return fecha.date()
                elif len(partes[0]) == 4:
                    fecha = datetime(int(partes[0]), int(partes[1]), int(partes[2]))
                    return fecha.date()
        return datetime.now().date()
    except:
        return None

def obtener_recordatorios_inmediatos(usuario_id):
    conn = get_connection()
    cursor = conn.cursor()
    hoy = datetime.now().date()
    
    cursor.execute('SELECT * FROM tarea WHERE usuario_id = ? AND estado = "pendiente" AND entrega IS NOT NULL', (usuario_id,))
    todas = cursor.fetchall()
    conn.close()
    
    tareas_hoy = []
    examenes_hoy = []
    
    for tarea in todas:
        fecha_tarea = convertir_formato_fecha(tarea[4])
        if fecha_tarea:
            # Índices ajustados: tarea[9] es recordatorio_dias, tarea[10] es materia
            try:
                if len(tarea) > 9 and tarea[9] is not None:
                    recordatorio_dias = int(tarea[9])
                else:
                    recordatorio_dias = 1
            except (ValueError, TypeError):
                recordatorio_dias = 1
                
            fecha_recordatorio = fecha_tarea - timedelta(days=recordatorio_dias)
            
            if hoy >= fecha_recordatorio:
                if fecha_tarea == hoy:
                    if len(tarea) > 7 and tarea[7] == 'examen':
                        examenes_hoy.append(tarea)
                    else:
                        tareas_hoy.append(tarea)
                elif hoy < fecha_tarea:
                    tareas_hoy.append(tarea)
    
    return {
        'tareas_hoy': tareas_hoy,
        'examenes_hoy': examenes_hoy,
        'total': len(tareas_hoy) + len(examenes_hoy),
        'examenes': len(examenes_hoy)
    }

    
def mostrar_recordatorios(recordatorios):
    if not recordatorios['tareas_hoy']:
        print("No hay recordatorios para hoy")
        return
    print("RECORDATORIOS PARA HOY")
    print("--"*25)
    if recordatorios['examenes_hoy']:
        print("EXÁMENES HOY:")
        for tarea in recordatorios['examenes_hoy']:
            print(f"- {tarea[2]}")
    otras = [t for t in recordatorios['tareas_hoy'] if t not in recordatorios['examenes_hoy']]
    if otras:
        print("OTRAS TAREAS:")
        for tarea in otras:
            tipo = tarea[7] if len(tarea) > 7 else 'tarea'
            print(f"- {tarea[2]} [{tipo.upper()}]")
    print(f"Total: {recordatorios['total']} tareas")
    print("--"*25)

def mostrar_proximas_tareas(usuario_id, dias=7):
    conn = get_connection()
    cursor = conn.cursor()
    hoy = datetime.now().date()
    cursor.execute('SELECT * FROM tarea WHERE usuario_id = ? AND estado = "pendiente" AND entrega IS NOT NULL', (usuario_id,))
    todas = cursor.fetchall()
    conn.close()
    
    proximas = []
    for tarea in todas:
        fecha_tarea = convertir_formato_fecha(tarea[4])
        if fecha_tarea:
            try:
                if len(tarea) > 9 and tarea[9] is not None:
                    recordatorio_dias = int(tarea[9])
                else:
                    recordatorio_dias = 1
            except (ValueError, TypeError):
                recordatorio_dias = 1
                
            fecha_recordatorio = fecha_tarea - timedelta(days=recordatorio_dias)
            
            if hoy <= fecha_recordatorio <= hoy + timedelta(days=dias):
                proximas.append((tarea, fecha_tarea, fecha_recordatorio))
    
    if not proximas:
        print(f"No hay tareas en los próximos {dias} días")
        return
    
    proximas.sort(key=lambda x: x[1])
    print(f"TAREAS PRÓXIMAS ({dias} días):")
    for tarea, fecha, fecha_recordatorio in proximas:
        dias_restantes = (fecha - hoy).days
        tipo = tarea[7] if len(tarea) > 7 else 'tarea'
        materia_info = f" [{tarea[10]}]" if len(tarea) > 10 and tarea[10] else ""
        
        if fecha_recordatorio == hoy:
            cuando = "RECORDATORIO HOY"
        elif fecha_recordatorio == hoy + timedelta(days=1):
            cuando = "RECORDATORIO MAÑANA"
        else:
            dias_recordatorio = (fecha_recordatorio - hoy).days
            cuando = f"RECORDATORIO EN {dias_recordatorio} DÍAS"
        
        print(f"- {tarea[2]}{materia_info} [{tipo.upper()}] - Entrega en {dias_restantes} días ({cuando})")

def configurar_recordatorio(tarea_id, dias):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE tarea SET recordatorio_dias = ? WHERE id = ?', (dias, tarea_id))
    conn.commit()
    conn.close()
    return True

def verificar_tareas_vencidas(usuario_id):
    conn = get_connection()
    cursor = conn.cursor()
    hoy = datetime.now().date()
    cursor.execute('SELECT * FROM tarea WHERE usuario_id = ? AND estado = "pendiente" AND entrega IS NOT NULL', (usuario_id,))
    todas = cursor.fetchall()
    conn.close()
    vencidas = []
    for tarea in todas:
        fecha_tarea = convertir_formato_fecha(tarea[4])
        if fecha_tarea and fecha_tarea < hoy:
            vencidas.append(tarea)
    return vencidas