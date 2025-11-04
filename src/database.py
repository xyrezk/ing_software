import sqlite3

def init_db():
    conn = sqlite3.connect("gestor_academico.db")
    cursor = conn.cursor()

    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuario (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            nombre TEXT NOT NULL,
        )
    ''')

    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER,
            titulo TEXT NOT NULL,
            descripcion TEXT,
            entrega DATE,
            prioridad TEXT,
            estado TEXT DEFAULT 'pendiente',
            FOREIGN KEY(usuario_id) REFERENCES usuario(id)
        )
    ''')

    conn.commit()
    conn.close()
    print("Base de datos inicializada correctamente")

def get_connection():
    try:
        conn = sqlite3.connect("gestor_academico.db")
        print("Conexión a la base de datos establecida correctamente.")
        return conn
    except sqlite3.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None