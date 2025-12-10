import sqlite3
from datetime import datetime
from database import get_connection

def crear_tarea(usuario_id, titulo, descripcion, prioridad, tipo='tarea', entrega=None, materia=''):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO tarea (usuario_id, titulo, descripcion, prioridad, tipo, entrega, materia)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (usuario_id, titulo, descripcion, prioridad, tipo, entrega, materia))
    conn.commit()
    conn.close()
    return True

def crear_examen(usuario_id, titulo, descripcion, prioridad, entrega, materia=''):
    return crear_tarea(usuario_id, titulo, descripcion, prioridad, 'examen', entrega, materia)

def crear_proyecto(usuario_id, titulo, descripcion, prioridad, entrega, materia=''):
    return crear_tarea(usuario_id, titulo, descripcion, prioridad, 'proyecto', entrega, materia)

def actualizar_tarea(tarea_id, titulo, descripcion, prioridad, tipo=None, entrega=None, materia=None):
    conn = get_connection()
    cursor = conn.cursor()
    
    campos = []
    valores = []
    
    campos.append("titulo = ?")
    valores.append(titulo)
    
    campos.append("descripcion = ?")
    valores.append(descripcion)
    
    campos.append("prioridad = ?")
    valores.append(prioridad)
    
    if tipo:
        campos.append("tipo = ?")
        valores.append(tipo)
    
    if entrega is not None:
        campos.append("entrega = ?")
        valores.append(entrega)
    
    if materia is not None:
        campos.append("materia = ?")
        valores.append(materia)
    
    valores.append(tarea_id)
    
    query = f"UPDATE tarea SET {', '.join(campos)} WHERE id = ?"
    cursor.execute(query, valores)
    
    conn.commit()
    conn.close()
    return cursor.rowcount > 0

def borrar_tarea(tarea_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tarea WHERE id = ?', (tarea_id,))
    conn.commit()
    conn.close()
    return cursor.rowcount > 0

def actualizar_estado_tarea(tarea_id, estado):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE tarea SET estado = ? WHERE id = ?', (estado, tarea_id))
    conn.commit()
    conn.close()
    return cursor.rowcount > 0

def obtener_tarea_usuario(usuario_id, tipo=None):
    conn = get_connection()
    cursor = conn.cursor()
    
    if tipo:
        cursor.execute('SELECT * FROM tarea WHERE usuario_id = ? AND tipo = ?', 
                      (usuario_id, tipo))
    else:
        cursor.execute('SELECT * FROM tarea WHERE usuario_id = ?', (usuario_id,))
    
    tareas = cursor.fetchall()
    conn.close()
    return tareas

def obtener_examenes_usuario(usuario_id):
    return obtener_tarea_usuario(usuario_id, 'examen')

def obtener_proyectos_usuario(usuario_id):
    return obtener_tarea_usuario(usuario_id, 'proyecto')