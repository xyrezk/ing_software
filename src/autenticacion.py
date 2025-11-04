import sqlite3
import hashlib
from database import get_connection

def usuario_registrado(email, password, nombre):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO usuario (email, password, nombre)
            VALUES (?, ?, ?)
        ''', (email, hashed_password, nombre))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False  
    finally:
        conn.close()

def login_usuario(email, password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM usuario WHERE email = ? AND password = ?', (email, hashed_password))
    usuario = cursor.fetchone()
    conn.close()
    return usuario

def logout_usuario():
    print("Sesión cerrada correctamente")
    return None
