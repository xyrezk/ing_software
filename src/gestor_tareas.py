import sqlite3
from database import get_connection


def crear_tarea(usuario_id, titulo, descripcion, prioridad):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO tarea (usuario_id, titulo, descripcion, prioridad)
        VALUES (?, ?, ?, ?)
    ''', (usuario_id, titulo, descripcion,prioridad))
    conn.commit()
    conn.close()
    return True

def obtener_tarea_usuario(usuario_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tarea WHERE usuario_id = ? ', (usuario_id,))
    tarea = cursor.fetchall()
    conn.close()
    return tarea

def actualizar_tarea(tarea_id, titulo, descripcion,prioridad):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE tarea 
        SET titulo = ?, descripcion = ?, priority = ?
        WHERE id = ?
    ''', (titulo, descripcion,prioridad, tarea_id))
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