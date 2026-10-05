class Usuario:
    ROLES = ("Administrador", "Empleado", "Cliente")

    def __init__(self, identificacion, nombre, correo="", usuario="", clave="", rol="Cliente"):
        self.identificacion = str(identificacion).strip()
        self.nombre = str(nombre).strip()
        self.correo = str(correo).strip().lower()
        self.usuario = str(usuario).strip()
        self.clave = str(clave).strip()
        self.rol = rol if rol in self.ROLES else "Cliente"

    def to_dict(self):
        return {
            "identificacion": self.identificacion,
            "nombre": self.nombre,
            "correo": self.correo,
            "usuario": self.usuario,
            "clave": self.clave,
            "rol": self.rol,
        }

    def __str__(self):
        return f"{self.nombre} | {self.usuario} | {self.rol}"
