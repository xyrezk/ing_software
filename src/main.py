from database import init_db
from autenticacion import usuario_registrado, login_usuario, logout_usuario
from gestor_tareas import crear_tarea, obtener_tarea_usuario, actualizar_tarea, borrar_tarea, actualizar_estado_tarea

def mostrar_tareas(tareas):
    if not tareas:
        print(" No hay tareas registradas")
        return
    
    print("\n TUS TAREAS:")
    for tarea in tareas:
        """estado = "✅" if tarea[6] == "completada" else "⏳" """
        print(f"{tarea[0]}. - Estado: {tarea[6]} {tarea[2]} - Vence: {tarea[4]} - Prioridad: {tarea[5]}")

def main():
    init_db()
    usuario_actual = None

    while True:
        print("\n" + "="*50)
        print("📚 SISTEMA DE GESTIÓN ACADÉMICA")
        print("="*50)
        
        if not usuario_actual:
            print("1.  Registrarse")
            print("2.  Iniciar sesión")
            print("3.  Salir")
            
            opcion = input("Selecciona una opción: ")
            
            if opcion == "1":
                print("\n--- REGISTRO DE USUARIO ---")
                email = input("Email: ")
                password = input("Contraseña: ")
                name = input("Nombre completo: ")
                
                if usuario_registrado(email, password, name):
                    print(" Usuario registrado exitosamente")
                else:
                    print(" Error: El email ya está registrado")
                    
            elif opcion == "2":
                print("\n--- INICIO DE SESIÓN ---")
                email = input("Email: ")
                password = input("Contraseña: ")
                
                user = login_usuario(email, password)
                if user:
                    usuario_actual = user
                    print(f" Bienvenido/a {user[3]}!")
                    
                else:
                    print(" Credenciales incorrectas")
                    
            elif opcion == "3":
                print(" Hasta luego")
                break
            else:
                print(" Opción inválida")