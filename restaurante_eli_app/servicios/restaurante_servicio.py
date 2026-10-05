from datetime import datetime

from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta
from servicios.archivo_servicio import ArchivoServicio


class RestauranteServicio:
    def __init__(self):
        self.usuarios = []
        self.productos = []
        self.ventas = []
        self.cargar_datos()

    def cargar_datos(self):
        datos_usuarios = ArchivoServicio.leer_json("usuarios.json")
        self.usuarios = []
        for indice, datos in enumerate(datos_usuarios):
            rol = datos.get("rol") or ("Administrador" if indice == 0 else "Cliente")
            identificacion = datos.get("identificacion", "")
            nombre = datos.get("nombre", "")
            usuario_login = datos.get("usuario") or self._generar_usuario(nombre, indice)
            correo = datos.get("correo") or f"{usuario_login.lower()}@restaurante.com"
            clave = datos.get("clave") or ("123456" if indice == 0 else "123456")
            self.usuarios.append(Usuario(identificacion, nombre, correo, usuario_login, clave, rol))

        self.productos = []
        for datos in ArchivoServicio.leer_json("productos.json"):
            try:
                self.productos.append(
                    Producto(
                        datos.get("codigo", ""),
                        datos.get("nombre", ""),
                        datos.get("precio", 0),
                        datos.get("stock", 0),
                    )
                )
            except (TypeError, ValueError):
                continue

        self.ventas = []
        for datos in ArchivoServicio.leer_json("ventas.json"):
            try:
                self.ventas.append(
                    Venta(
                        datos.get("identificacion_usuario", ""),
                        datos.get("codigo_producto", ""),
                        datos.get("cantidad", 1),
                        datos.get("fecha", ""),
                    )
                )
            except (TypeError, ValueError):
                continue

    def _generar_usuario(self, nombre, indice):
        base = "".join(ch for ch in str(nombre).lower() if ch.isalnum()) or "usuario"
        return f"{base}{indice + 1}"

    # ==================== LOGIN ====================
    def validar_acceso(self, acceso, clave):
        acceso = str(acceso).strip().casefold()
        clave = str(clave).strip()
        for usuario in self.usuarios:
            if (
                (
                    usuario.usuario.casefold() == acceso
                    or usuario.correo.casefold() == acceso
                    or usuario.nombre.casefold() == acceso
                )
                and usuario.clave == clave
            ):
                return usuario
        return None

    # ==================== USUARIOS ====================
    def listar_usuarios(self):
        return list(self.usuarios)

    def buscar_usuario(self, identificacion):
        identificacion = str(identificacion).strip().casefold()
        for usuario in self.usuarios:
            if usuario.identificacion.casefold() == identificacion:
                return usuario
        return None

    def buscar_por_usuario_o_correo(self, acceso):
        acceso = str(acceso).strip().casefold()
        for usuario in self.usuarios:
            if usuario.usuario.casefold() == acceso or usuario.correo.casefold() == acceso:
                return usuario
        return None

    def registrar_usuario(self, identificacion, nombre, correo, usuario_login, clave, rol):
        identificacion = str(identificacion).strip()
        nombre = str(nombre).strip()
        correo = str(correo).strip().lower()
        usuario_login = str(usuario_login).strip()
        clave = str(clave).strip()
        rol = str(rol).strip()

        if not identificacion or not nombre or not correo or not usuario_login or not clave:
            return False, "Complete todos los campos obligatorios."
        if "@" not in correo or "." not in correo.split("@")[-1]:
            return False, "Ingrese un correo electrónico válido."
        if len(clave) < 6 or len(clave) > 12:
            return False, "La clave debe tener entre 6 y 12 caracteres."
        if rol not in Usuario.ROLES:
            return False, "Seleccione un rol válido."
        if self.buscar_usuario(identificacion):
            return False, "Ya existe un usuario con esa identificación."
        if self.buscar_por_usuario_o_correo(usuario_login):
            return False, "El nombre de usuario ya está registrado."
        if self.buscar_por_usuario_o_correo(correo):
            return False, "El correo electrónico ya está registrado."

        self.usuarios.append(Usuario(identificacion, nombre, correo, usuario_login, clave, rol))
        self.guardar_usuarios()
        return True, "Usuario registrado correctamente."

    def actualizar_usuario(self, identificacion, nombre, correo, usuario_login, clave, rol):
        usuario = self.buscar_usuario(identificacion)
        if usuario is None:
            return False, "No se encontró el usuario."

        nombre = str(nombre).strip()
        correo = str(correo).strip().lower()
        usuario_login = str(usuario_login).strip()
        clave = str(clave).strip()
        rol = str(rol).strip()

        if not nombre or not correo or not usuario_login or not clave:
            return False, "Complete todos los campos obligatorios."
        if "@" not in correo or "." not in correo.split("@")[-1]:
            return False, "Ingrese un correo electrónico válido."
        if len(clave) < 6 or len(clave) > 12:
            return False, "La clave debe tener entre 6 y 12 caracteres."
        if rol not in Usuario.ROLES:
            return False, "Seleccione un rol válido."

        for otro in self.usuarios:
            if otro is usuario:
                continue
            if otro.usuario.casefold() == usuario_login.casefold():
                return False, "El nombre de usuario ya está registrado."
            if otro.correo.casefold() == correo.casefold():
                return False, "El correo electrónico ya está registrado."

        usuario.nombre = nombre
        usuario.correo = correo
        usuario.usuario = usuario_login
        usuario.clave = clave
        usuario.rol = rol
        self.guardar_usuarios()
        return True, "Usuario actualizado correctamente."

    def eliminar_usuario(self, identificacion, identificacion_admin):
        usuario = self.buscar_usuario(identificacion)
        if usuario is None:
            return False, "No se encontró el usuario."

        if usuario.identificacion.casefold() == str(identificacion_admin).strip().casefold():
            return False, "No puede eliminar la cuenta Administrador actualmente autenticada."

        if usuario.rol == "Administrador":
            administradores = [u for u in self.usuarios if u.rol == "Administrador" and u.identificacion.casefold() != usuario.identificacion.casefold()]
            if not administradores:
                return False, "No puede eliminar al único Administrador del sistema."

        self.usuarios.remove(usuario)
        self.guardar_usuarios()
        return True, "Usuario eliminado correctamente."

    def guardar_usuarios(self):
        ArchivoServicio.guardar_json("usuarios.json", [usuario.to_dict() for usuario in self.usuarios])

    # ==================== PRODUCTOS ====================
    def listar_productos(self):
        return list(self.productos)

    def buscar_producto(self, codigo):
        codigo = str(codigo).strip().casefold()
        for producto in self.productos:
            if producto.codigo.strip().casefold() == codigo:
                return producto
        return None

    def registrar_producto(self, codigo, nombre, precio, stock):
        codigo = str(codigo).strip()
        nombre = str(nombre).strip()

        if not codigo:
            return False, "El código es obligatorio."
        if not nombre:
            return False, "El nombre es obligatorio."

        try:
            precio = float(precio)
            stock = int(stock)
        except (TypeError, ValueError):
            return False, "Precio y stock deben ser valores numéricos."

        if precio < 0 or stock < 0:
            return False, "Precio y stock no pueden ser negativos."
        if self.buscar_producto(codigo):
            return False, "Ya existe un producto con ese código."

        self.productos.append(Producto(codigo, nombre, precio, stock))
        self.guardar_productos()
        return True, "Producto registrado correctamente."

    def actualizar_producto(self, codigo, nombre, precio, stock):
        producto = self.buscar_producto(codigo)
        if producto is None:
            return False, "No se encontró el producto."

        nombre = str(nombre).strip()
        if not nombre:
            return False, "El nombre es obligatorio."

        try:
            precio = float(precio)
            stock = int(stock)
        except (TypeError, ValueError):
            return False, "Precio y stock deben ser valores numéricos."

        if precio < 0 or stock < 0:
            return False, "Precio y stock no pueden ser negativos."

        producto.nombre = nombre
        producto.precio = precio
        producto.stock = stock
        self.guardar_productos()
        return True, "Producto actualizado correctamente."

    def eliminar_producto(self, codigo):
        producto = self.buscar_producto(codigo)
        if producto is None:
            return False, "No se encontró el producto."

        self.productos.remove(producto)
        self.guardar_productos()
        return True, "Producto eliminado correctamente."

    def guardar_productos(self):
        ArchivoServicio.guardar_json(
            "productos.json", [producto.to_dict() for producto in self.productos]
        )

    # ==================== VENTAS ====================
    def listar_ventas(self):
        return list(self.ventas)

    def registrar_venta(self, identificacion_usuario, codigo_producto, cantidad=1):
        usuario = self.buscar_usuario(identificacion_usuario)
        if usuario is None:
            return False, "El usuario seleccionado no existe."

        producto = self.buscar_producto(codigo_producto)
        if producto is None:
            return False, "El producto seleccionado no existe."

        try:
            cantidad = int(cantidad)
        except (TypeError, ValueError):
            return False, "La cantidad debe ser un número entero."

        if cantidad <= 0:
            return False, "La cantidad debe ser mayor que cero."
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        venta = Venta(identificacion_usuario, codigo_producto, cantidad, fecha)
        self.ventas.append(venta)

        # Se conserva la lógica de ventas de la Semana 15:
        # registrar la venta no modifica el inventario.
        self.guardar_ventas()
        return True, "Venta registrada correctamente."

    def guardar_ventas(self):
        ArchivoServicio.guardar_json(
            "ventas.json", [venta.to_dict() for venta in self.ventas]
        )
