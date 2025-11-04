class Usuario:
    def __init__(self, id, email, password, nombre):
        self.id = id
        self.email = email
        self.password = password
        self.nombre = nombre

class Tarea:
    def __init__(self, id, usuario_id, titulo, descripcion, entrega, prioridad, estado="pendiente"):
        self.id = id
        self.usuario_id = usuario_id
        self.titulo = titulo
        self.descripcion = descripcion
        self.entrega = entrega
        self.prioridad = prioridad
        self.estado = estado