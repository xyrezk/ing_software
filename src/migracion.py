import sqlite3
import os
from database import get_db_path

def migrar_base_datos():
    db_path = get_db_path()
    
    if not os.path.exists(db_path):
        print("La base de datos no existe. Ejecuta init_db primero.")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        cursor.execute("PRAGMA table_info(tarea)")
        columnas = [col[1] for col in cursor.fetchall()]
        
        if 'materia' not in columnas:
            print("Agregando columna 'materia'...")
            cursor.execute("ALTER TABLE tarea ADD COLUMN materia TEXT DEFAULT ''")
            print("✓ Columna 'materia' agregada")
        
        conn.commit()
        print("\nMigración completada exitosamente")
        
    except sqlite3.Error as e:
        print(f"Error en migración: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    migrar_base_datos()