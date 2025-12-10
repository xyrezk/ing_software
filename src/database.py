import sqlite3
import os

def get_db_path():
   
    dir_actual = os.path.dirname(os.path.abspath(__file__))
    ruta_proyecto = os.path.dirname(dir_actual)
    return os.path.join(ruta_proyecto, "gestor_academico.db")

def init_db():
    db_path = get_db_path()  
    conn = sqlite3.connect(db_path) 
    cursor = conn.cursor()

    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuario (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            nombre TEXT NOT NULL
        )
    ''')

    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tarea (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER,
            titulo TEXT NOT NULL,
            descripcion TEXT,
            entrega DATE,
            prioridad TEXT,
            estado TEXT DEFAULT 'pendiente',
            tipo TEXT DEFAULT 'tarea',  -- 'tarea', 'examen', 'proyecto', etc.
            recordatorio_dias INTEGER DEFAULT 1,
            materia TEXT DEFAULT '',
            color TEXT DEFAULT '🔵',
            FOREIGN KEY(usuario_id) REFERENCES usuario(id)
        )
    ''')

    conn.commit()
    conn.close()
    print("Base de datos inicializada correctamente")

def get_connection():
    try:
        db_path = get_db_path()
        conn = sqlite3.connect(db_path)
        print("Conexión a la base de datos establecida correctamente.")
        return conn
    except sqlite3.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None