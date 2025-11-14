from database import init_db
from autenticacion import usuario_registrado, login_usuario, logout_usuario
from gestor_tareas import crear_tarea, obtener_tarea_usuario, actualizar_tarea, borrar_tarea, actualizar_estado_tarea

def mostrar_tareas(tareas):
    if not tareas:
        print(" No hay tareas registradas")
        return
    
    print("\n TUS TAREAS:")
    for tarea in tareas:
        
        print(f"{tarea[0]}. - Estado: {tarea[6]} {tarea[2]} - Vence: {tarea[4]} - Prioridad: {tarea[5]}")

def main():
    init_db()
    usuario_actual = None

    while True:
        print("\n" + "="*50)
        print(" SISTEMA DE GESTIÓN ACADÉMICA")
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
        if usuario_actual != None:
            
            print(f"Usuario: {usuario_actual[3]} ({usuario_actual[1]})")
            print("\n1.  Crear nueva tarea")
            print("2.  Ver mis tareas")
            print("3.  Editar tarea")
            print("4.  Eliminar tarea")
            print("5.  Marcar tarea como completada")
            print("6.  Marcar tarea como pendiente")
            """print("7.  Ver recordatorios")"""
            print("8.  Cerrar sesión")
            
            opcion = input("Selecciona una opción: ")
            
            if opcion == "1":
                print("\n--- CREAR NUEVA TAREA ---")
                titulo = input("Título de la tarea: ")
                descripcion = input("Descripción: ")
                
                prioridad = input("Prioridad (alta/media/baja): ")
                
                if crear_tarea(usuario_actual[0], titulo, descripcion, prioridad):
                    print(" Tarea creada exitosamente")
                else:
                    print(" Error al crear la tarea")
                    
            elif opcion == "2":
                tarea = obtener_tarea_usuario(usuario_actual[0])
                mostrar_tareas(tarea)
                
            elif opcion == "3":
                tarea = obtener_tarea_usuario(usuario_actual[0])
                if tarea:
                    mostrar_tareas(tarea)
                    tarea_id = input("\nID de la tarea a editar: ")
                    titulo = input("Nuevo título: ")
                    descripcion = input("Nueva descripción: ")
                    prioridad = input("Nueva prioridad: ")
                    
                    if actualizar_tarea(tarea_id, titulo, descripcion, prioridad):
                        print(" Tarea actualizada")
                    else:
                        print(" Error al actualizar")
                else:
                    print(" No hay tareas para editar")
                    
            elif opcion == "4":
                tarea = obtener_tarea_usuario(usuario_actual[0])
                if tarea:
                    mostrar_tareas(tarea)
                    tarea_id = input("\nID de la tarea a eliminar: ")
                    confirm = input("¿Estás seguro? (s/n): ")
                    if confirm.lower() == 's':
                        if borrar_tarea(tarea_id):
                            print(" Tarea eliminada")
                        else:
                            print(" Error al eliminar")
                else:
                    print(" No hay tareas para eliminar")
                    
            elif opcion == "5":
                tarea = obtener_tarea_usuario(usuario_actual[0])
                if tarea:
                    mostrar_tareas(tarea)
                    tarea_id = input("\nID de la tarea a marcar como COMPLETADA: ")
                    if actualizar_estado_tarea(tarea_id, "completada"):
                        print(" Tarea marcada como completada")
                    else:
                        print(" Error al actualizar")
                else:
                    print(" No hay tareas")
                    
            elif opcion == "6":
                tarea = obtener_tarea_usuario(usuario_actual[0])
                if tarea:
                    mostrar_tareas(tarea)
                    tarea_id = input("\nID de la tarea a marcar como PENDIENTE: ")
                    if actualizar_estado_tarea(tarea_id, "pendiente"):
                        print(" Tarea marcada como pendiente")
                    else:
                        print(" Error al actualizar")
                else:
                    print(" No hay tareas")
                    
                
            elif opcion == "8":
                usuario_actual = logout_usuario()
                
            else:
                print(" Opción inválida")

if __name__ == "__main__":
    main()    