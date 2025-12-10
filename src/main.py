from database import init_db
from autenticacion import usuario_registrado, login_usuario, logout_usuario
from gestor_tareas import (crear_tarea, crear_examen, crear_proyecto, 
                          obtener_tarea_usuario, actualizar_tarea, 
                          borrar_tarea, actualizar_estado_tarea,
                          obtener_examenes_usuario, obtener_proyectos_usuario)
from recordatorios import (mostrar_recordatorios, obtener_recordatorios_inmediatos,
                          mostrar_proximas_tareas, configurar_recordatorio,
                          verificar_tareas_vencidas)

def mostrar_colores():
    print("\nCOLORES DISPONIBLES:")
    print("🔵 - Azul (Por defecto)")
    print("🔴 - Rojo (Importante/Urgente)")
    print("🟢 - Verde (Completado/Fácil)")
    print("🟡 - Amarillo (Advertencia)")
    print("🟣 - Morado (Creativo/Personal)")
    print("⚫ - Negro (Secreto/Confidencial)")
    print("🟤 - Marrón (Investigación)")
    print("⚪ - Blanco (General)")
    return {
        'azul': '🔵',
        'rojo': '🔴',
        'verde': '🟢',
        'amarillo': '🟡',
        'morado': '🟣',
        'negro': '⚫',
        'marrón': '🟤',
        'marron': '🟤',
        'blanco': '⚪'
    }

def mostrar_tareas(tareas):
    if not tareas:
        print("No hay tareas registradas")
        return
    
    print("\nTUS TAREAS:")
    for tarea in tareas:
        tipo_indicador = "[EXAMEN]" if tarea[7] == 'examen' else "[TAREA]" if tarea[7] == 'tarea' else "[PROYECTO]"
        estado = "[COMPLETADA]" if tarea[6] == 'completada' else "[PENDIENTE]"
        fecha = f" - Vence: {tarea[4]}" if tarea[4] else ""
        materia_info = f" - Materia: {tarea[10]}" if len(tarea) > 10 and tarea[10] else ""
        recordatorio_info = f" - Recordatorio: {tarea[9]} días antes" if len(tarea) > 9 and tarea[9] else ""
        color_emoji = tarea[10] if len(tarea) > 10 else '🔵'
        
        print(f"{tarea[0]}. {color_emoji} {tipo_indicador} {estado} {tarea[2]}{materia_info} - Prioridad: {tarea[5]}{fecha}{recordatorio_info}")

def main():
    init_db()
    usuario_actual = None

    while True:
        print("\n" + "="*50)
        print("SISTEMA DE GESTION ACADEMICA")
        print("="*50)
        
        if usuario_actual:
            recordatorios = obtener_recordatorios_inmediatos(usuario_actual[0])
            mostrar_recordatorios(recordatorios)
            
            tareas_vencidas = verificar_tareas_vencidas(usuario_actual[0])
            if tareas_vencidas:
                print("\n" + "!"*60)
                print("¡TIENES TAREAS VENCIDAS!")
                print("!"*60)
                for tarea in tareas_vencidas[:3]:  
                    print(f"- {tarea[2]} - Vencida el {tarea[4]}")
        
        if not usuario_actual:
            print("1. Registrarse")
            print("2. Iniciar sesión")
            print("3. Salir")
            
            opcion = input("Selecciona una opcion: ")
            
            if opcion == "1":
                print("\n--- REGISTRO DE USUARIO ---")
                email = input("Email: ")
                password = input("Contraseña: ")
                name = input("Nombre completo: ")
                
                if usuario_registrado(email, password, name):
                    print("Usuario registrado exitosamente")
                else:
                    print("Error: El email ya está registrado")
                    
            elif opcion == "2":
                print("\n--- INICIO DE SESION ---")
                email = input("Email: ")
                password = input("Contraseña: ")
                
                user = login_usuario(email, password)
                if user:
                    usuario_actual = user
                    print(f"Bienvenido/a {user[3]}!")
                    
                else:
                    print("Credenciales incorrectas")
                    
            elif opcion == "3":
                print("Hasta luego")
                break
            else:
                print("Opcion invalida")
        else:
            print(f"\nUsuario: {usuario_actual[3]} ({usuario_actual[1]})")
            print("\n1.  Crear nueva tarea")
            print("2.  Crear examen")
            print("3.  Crear proyecto")
            print("4.  Ver todas mis tareas")
            print("5.  Ver solo examenes")
            print("6.  Ver solo proyectos")
            print("7.  Editar tarea")
            print("8.  Eliminar tarea")
            print("9.  Marcar tarea como completada")
            print("10. Marcar tarea como pendiente")
            print("11. Ver proximas tareas (7 dias)")
            print("12. Configurar recordatorio")
            print("13. Cambiar color de una tarea")
            print("14. Ver recordatorios de hoy")
            print("15. Cerrar sesion")
            
            opcion = input("\nSelecciona una opcion: ")
            
            if opcion == "1":
                print("\n--- CREAR NUEVA TAREA ---")
                titulo = input("Título de la tarea: ")
                descripcion = input("Descripción: ")
                prioridad = input("Prioridad (alta/media/baja): ")
                materia = input("Materia (opcional): ")
                fecha = input("Fecha de entrega (YYYY-MM-DD, opcional): ") or None
                colores = mostrar_colores()
                color_input = input("Color (escribe el nombre o presiona Enter para azul): ").lower()
                color = colores.get(color_input, '🔵')  
                
                if crear_tarea(usuario_actual[0], titulo, descripcion, prioridad, 'tarea', fecha, materia, color):
                    print("Tarea creada exitosamente")

            elif opcion == "2":
                print("\n--- CREAR EXAMEN ---")
                titulo = input("Materia del examen: ")
                descripcion = input("Temas a evaluar: ")
                materia = input("Materia (opcional): ")
                prioridad = "alta"
                fecha = input("Fecha del examen (YYYY-MM-DD): ")
                colores = mostrar_colores()
                color_input = input("Color (escribe el nombre o presiona Enter para azul): ").lower()
                color = colores.get(color_input, '🔵')  # Default azul

                if crear_examen(usuario_actual[0], titulo, descripcion, prioridad, fecha, materia, color):
                    print("Examen registrado exitosamente")

            elif opcion == "3":
                print("\n--- CREAR PROYECTO ---")
                titulo = input("Nombre del proyecto: ")
                descripcion = input("Descripción del proyecto: ")
                prioridad = input("Prioridad (alta/media/baja): ")
                materia = input("Materia (opcional): ")
                fecha = input("Fecha de entrega (YYYY-MM-DD): ")
                colores = mostrar_colores()
                color_input = input("Color (escribe el nombre o presiona Enter para azul): ").lower()
                color = colores.get(color_input, '🔵')  # Default azul

                if crear_proyecto(usuario_actual[0], titulo, descripcion, prioridad, fecha, materia, color):
                    print("Proyecto creado exitosamente")
            elif opcion == "4":
                tareas = obtener_tarea_usuario(usuario_actual[0])
                mostrar_tareas(tareas)
                
            elif opcion == "5":
                examenes = obtener_examenes_usuario(usuario_actual[0])
                mostrar_tareas(examenes)
                
            elif opcion == "6":
                proyectos = obtener_proyectos_usuario(usuario_actual[0])
                mostrar_tareas(proyectos)
                
            elif opcion == "7":
                tareas = obtener_tarea_usuario(usuario_actual[0])
                if tareas:
                    mostrar_tareas(tareas)
                    tarea_id = input("\nID de la tarea a editar: ")
                    titulo = input("Nuevo título (dejar vacío para no cambiar): ")
                    descripcion = input("Nueva descripción (dejar vacío para no cambiar): ")
                    prioridad = input("Nueva prioridad (dejar vacío para no cambiar): ")
                    materia = input("Nueva materia (dejar vacío para no cambiar, '-' para borrar): ")
                    fecha = input("Nueva fecha (YYYY-MM-DD, dejar vacío para no cambiar): ")
                    color_input = input("Nuevo color (dejar vacío para no cambiar): ").lower()

                    tarea_actual = next((t for t in tareas if str(t[0]) == tarea_id), None)
                    if tarea_actual:
                        titulo = titulo or tarea_actual[2]
                        descripcion = descripcion or tarea_actual[3]
                        prioridad = prioridad or tarea_actual[5]
                        fecha = fecha if fecha != '' else tarea_actual[4]

                        if materia == '':
                            materia_valor = tarea_actual[9] if len(tarea_actual) > 9 else ''
                        elif materia == '-':
                            materia_valor = ''
                        else:
                            materia_valor = materia
                        if color_input:
                            colores = mostrar_colores()
                            color_valor = colores.get(color_input, tarea_actual[11] if len(tarea_actual) > 11 else '🔵')
                        else:
                            color_valor = tarea_actual[10] if len(tarea_actual) > 10 else '🔵'

                        if actualizar_tarea(tarea_id, titulo, descripcion, prioridad, tarea_actual[7], fecha, materia_valor, color_valor):
                            print("Tarea actualizada")

            elif opcion == "8":
                tareas = obtener_tarea_usuario(usuario_actual[0])
                if tareas:
                    mostrar_tareas(tareas)
                    tarea_id = input("\nID de la tarea a eliminar: ")
                    confirm = input("¿Estás seguro? (s/n): ")
                    if confirm.lower() == 's':
                        if borrar_tarea(tarea_id):
                            print("Tarea eliminada")
                        else:
                            print("Error al eliminar")
                else:
                    print("No hay tareas para eliminar")
                    
            elif opcion == "9":
                tareas = obtener_tarea_usuario(usuario_actual[0])
                if tareas:
                    mostrar_tareas(tareas)
                    tarea_id = input("\nID de la tarea a marcar como COMPLETADA: ")
                    if actualizar_estado_tarea(tarea_id, "completada"):
                        print("Tarea marcada como completada")
                    else:
                        print("Error al actualizar")
                else:
                    print("No hay tareas")
                    
            elif opcion == "10":
                tareas = obtener_tarea_usuario(usuario_actual[0])
                if tareas:
                    mostrar_tareas(tareas)
                    tarea_id = input("\nID de la tarea a marcar como PENDIENTE: ")
                    if actualizar_estado_tarea(tarea_id, "pendiente"):
                        print("Tarea marcada como pendiente")
                    else:
                        print("Error al actualizar")
                else:
                    print("No hay tareas")
                    
            elif opcion == "11":
                mostrar_proximas_tareas(usuario_actual[0], 7)
                
            elif opcion == "12":
                tareas = obtener_tarea_usuario(usuario_actual[0])
                if tareas:
                    mostrar_tareas(tareas)
                    tarea_id = input("\nID de la tarea para configurar recordatorio: ")
                    
                    tarea_actual = next((t for t in tareas if str(t[0]) == tarea_id), None)
                    if tarea_actual:
                        dias_actual = tarea_actual[8] if len(tarea_actual) > 8 and tarea_actual[8] is not None else 1
                        print(f"Recordatorio actual: {dias_actual} día(s) antes")
                        
                        dias = input("Nuevos días de anticipación (1-7): ")
                        try:
                            dias_int = int(dias)
                            if 1 <= dias_int <= 7:
                                if configurar_recordatorio(tarea_id, dias_int):
                                    print(f"Recordatorio configurado para {dias_int} días antes")
                                else:
                                    print("Error al configurar recordatorio")
                            else:
                                print("Los días deben estar entre 1 y 7")
                        except ValueError:
                            print("Ingresa un número válido")
                else:
                    print("No hay tareas para configurar")
            elif opcion == "13":
                tareas = obtener_tarea_usuario(usuario_actual[0])
                if tareas:
                    mostrar_tareas(tareas)
                    tarea_id = input("\nID de la tarea para cambiar color: ")

                    tarea_actual = next((t for t in tareas if str(t[0]) == tarea_id), None)
                    if tarea_actual:
                        colores = mostrar_colores()
                        print(f"\nColor actual: {tarea_actual[10] if len(tarea_actual) > 10 else '🔵'}")
                        color_input = input("Nuevo color (escribe el nombre): ").lower()

                        if color_input in colores:
                            if actualizar_tarea(tarea_id, 
                                               tarea_actual[2], 
                                               tarea_actual[3], 
                                               tarea_actual[5], 
                                               tarea_actual[7], 
                                               tarea_actual[4], 
                                               tarea_actual[10] if len(tarea_actual) > 10 else '',
                                               colores[color_input]):
                                print(f"Color cambiado a {colores[color_input]}")
                            else:
                                print("Error al cambiar el color")
                        else:
                            print("Color no válido")
                else:
                    print("No hay tareas para cambiar color")
            elif opcion == "14":
                recordatorios = obtener_recordatorios_inmediatos(usuario_actual[0])
                mostrar_recordatorios(recordatorios)
                
            elif opcion == "15":
                usuario_actual = logout_usuario()
                
            else:
                print("Opcion invalida")

if __name__ == "__main__":
    main()