import unittest
import os
import sys
import sqlite3

# Agregar la carpeta src al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import autenticacion
import database
from autenticacion import usuario_registrado, login_usuario, logout_usuario

# 🔧 Usar la base de datos de prueba en lugar de la real
def get_test_connection():
    return sqlite3.connect("test_gestor_academico.db")

database.get_connection = get_test_connection
autenticacion.get_connection = get_test_connection


class TestAutenticacion(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Crear base de datos de prueba
        cls.test_db = "test_gestor_academico.db"
        conn = sqlite3.connect(cls.test_db)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE usuario (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                nombre TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

    def setUp(self):
        # Limpiar tabla usuario antes de cada prueba
        conn = sqlite3.connect(self.test_db)
        conn.execute("DELETE FROM usuario")
        conn.commit()
        conn.close()

    def test_registro_usuario_exitoso(self):
        resultado = usuario_registrado("test@example.com", "1234", "Usuario Test")
        self.assertTrue(resultado)

    def test_registro_usuario_duplicado(self):
        usuario_registrado("test@example.com", "1234", "Usuario Test")
        resultado = usuario_registrado("test@example.com", "abcd", "Otro Usuario")
        self.assertFalse(resultado)

    def test_login_correcto(self):
        usuario_registrado("test@example.com", "1234", "Usuario Test")
        usuario = login_usuario("test@example.com", "1234")
        self.assertIsNotNone(usuario)

    def test_login_incorrecto(self):
        usuario_registrado("test@example.com", "1234", "Usuario Test")
        usuario = login_usuario("test@example.com", "incorrecto")
        self.assertIsNone(usuario)

    def test_logout(self):
        salida = logout_usuario()
        self.assertIsNone(salida)

    @classmethod
    def tearDownClass(cls):
        # Eliminar base de datos de prueba
        if os.path.exists(cls.test_db):
            os.remove(cls.test_db)


if __name__ == "__main__":
    unittest.main()
