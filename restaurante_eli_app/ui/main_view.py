import tkinter as tk
from pathlib import Path
from tkinter import ttk, messagebox


class MainView:
    def __init__(self, root, servicio, cerrar_sesion, usuario_actual):
        self.root = root
        self.servicio = servicio
        self.cerrar_sesion = cerrar_sesion
        self.usuario_actual = usuario_actual

        self.root.title("Sazón & Mesa | Gestión de Restaurante")
        self.root.geometry("1180x760")
        self.root.minsize(1050, 680)
        self.root.configure(bg="#F7F3EE")

        self.logo = None
        self.icon_venta = None
        self.crear_estilos()
        self.crear_interfaz()
        self.mostrar_productos()

    def crear_estilos(self):
        estilo = ttk.Style()
        try:
            estilo.theme_use("clam")
        except tk.TclError:
            pass
        estilo.configure("TFrame", background="#F7F3EE")
        estilo.configure("Card.TFrame", background="#FFFFFF")
        estilo.configure("Title.TLabel", background="#5A1E22", foreground="#FFF8F0", font=("Segoe UI", 22, "bold"))
        estilo.configure("Subtitle.TLabel", background="#5A1E22", foreground="#F5D7B2", font=("Segoe UI", 10))
        estilo.configure("Section.TLabel", background="#F7F3EE", foreground="#5A1E22", font=("Segoe UI", 19, "bold"))
        estilo.configure("Info.TLabel", background="#F7F3EE", foreground="#6E625C", font=("Segoe UI", 10))
        estilo.configure("Card.TLabelframe", background="#FFFFFF", foreground="#5A1E22", bordercolor="#E4D6C8")
        estilo.configure("Card.TLabelframe.Label", background="#FFFFFF", foreground="#5A1E22", font=("Segoe UI", 11, "bold"))
        estilo.configure("Action.TButton", font=("Segoe UI", 10, "bold"), padding=(14, 9), background="#A8462D", foreground="#FFFFFF", borderwidth=0)
        estilo.map("Action.TButton", background=[("active", "#873521")])
        estilo.configure("Secondary.TButton", font=("Segoe UI", 10, "bold"), padding=(14, 9), background="#E8D6C5", foreground="#5A1E22", borderwidth=0)
        estilo.map("Secondary.TButton", background=[("active", "#D9C0AA")])
        estilo.configure("Danger.TButton", font=("Segoe UI", 10, "bold"), padding=(14, 9), background="#8B3030", foreground="#FFFFFF", borderwidth=0)
        estilo.map("Danger.TButton", background=[("active", "#702323")])
        estilo.configure("Treeview", rowheight=34, font=("Segoe UI", 10), background="#FFFFFF", fieldbackground="#FFFFFF", foreground="#352E2A")
        estilo.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), background="#5A1E22", foreground="#FFFFFF", padding=8)
        estilo.map("Treeview", background=[("selected", "#EBC9A8")], foreground=[("selected", "#3D211C")])
        estilo.configure("TEntry", padding=8, fieldbackground="#FFFFFF")
        estilo.configure("TCombobox", padding=7, fieldbackground="#FFFFFF")

    def crear_interfaz(self):
        contenedor = ttk.Frame(self.root, padding=0)
        contenedor.pack(fill="both", expand=True)

        encabezado = tk.Frame(contenedor, bg="#5A1E22", height=112)
        encabezado.pack(fill="x")
        encabezado.pack_propagate(False)

        ruta_logo = Path(__file__).resolve().parent.parent / "assets" / "logo.png"
        if ruta_logo.exists():
            try:
                self.logo = tk.PhotoImage(file=str(ruta_logo))
                tk.Label(encabezado, image=self.logo, bg="#5A1E22").pack(side="left", padx=(24, 16), pady=16)
            except tk.TclError:
                pass

        bloque = tk.Frame(encabezado, bg="#5A1E22")
        bloque.pack(side="left", fill="both", expand=True, pady=16)
        ttk.Label(bloque, text="SAZÓN & MESA", style="Title.TLabel").pack(anchor="w")
        ttk.Label(bloque, text="Sistema de gestión del restaurante", style="Subtitle.TLabel").pack(anchor="w", pady=(3, 0))
        ttk.Label(bloque, text=f"Sesión activa: {self.usuario_actual.nombre}  •  {self.usuario_actual.rol}", style="Subtitle.TLabel").pack(anchor="w", pady=(7, 0))

        ttk.Button(encabezado, text="Cerrar sesión", command=self.cerrar_sesion, style="Secondary.TButton").pack(side="right", padx=24, pady=34)

        navegacion = tk.Frame(contenedor, bg="#FFFDF9", height=64)
        navegacion.pack(fill="x")
        navegacion.pack_propagate(False)

        tk.Label(navegacion, text="MENÚ", bg="#FFFDF9", fg="#A8462D", font=("Segoe UI", 9, "bold")).pack(side="left", padx=(24, 10))
        if self.usuario_actual.rol == "Administrador":
            ttk.Button(navegacion, text="👤  Usuarios", command=self.mostrar_usuarios, style="Secondary.TButton").pack(side="left", padx=4, pady=10)
        ttk.Button(navegacion, text="🍽  Productos", command=self.mostrar_productos, style="Secondary.TButton").pack(side="left", padx=4, pady=10)
        ttk.Button(navegacion, text="💰  Ventas", command=self.mostrar_ventas, style="Secondary.TButton").pack(side="left", padx=4, pady=10)

        self.contenido = ttk.Frame(contenedor, padding=(24, 20))
        self.contenido.pack(fill="both", expand=True)
        self.estado = tk.Label(contenedor, text="Listo.", bg="#EFE4D8", fg="#5A1E22", anchor="w", font=("Segoe UI", 9), padx=24, pady=7)
        self.estado.pack(fill="x", side="bottom")

    def limpiar_contenido(self):
        for widget in self.contenido.winfo_children():
            widget.destroy()

    def establecer_estado(self, texto):
        self.estado.config(text=texto)

    # ==================== USUARIOS - SEMANA 16 ====================
    def mostrar_usuarios(self):
        if self.usuario_actual.rol != "Administrador":
            messagebox.showwarning("Acceso restringido", "Solo un usuario con rol Administrador puede gestionar usuarios.")
            return
        self.limpiar_contenido()
        ttk.Label(self.contenido, text="Gestión de usuarios", style="Section.TLabel").pack(anchor="w")
        ttk.Label(self.contenido, text="Administre cuentas, roles y datos de acceso de forma segura y sencilla.", style="Info.TLabel").pack(anchor="w", pady=(3, 14))

        formulario = ttk.LabelFrame(self.contenido, text="  Datos de la cuenta  ", padding=16, style="Card.TLabelframe")
        formulario.pack(fill="x", pady=(0, 12))

        campos = [
            ("Identificación", "entry_identificacion", 0, 0),
            ("Nombre completo", "entry_nombre_usuario", 0, 2),
            ("Correo electrónico", "entry_correo", 1, 0),
            ("Usuario de acceso", "entry_usuario_login", 1, 2),
            ("Clave (6-12)", "entry_clave", 2, 0),
        ]
        for texto, atributo, fila, columna in campos:
            ttk.Label(formulario, text=texto).grid(row=fila, column=columna, sticky="w", padx=7, pady=7)
            entrada = ttk.Entry(formulario, width=30, show="*" if atributo == "entry_clave" else "")
            entrada.grid(row=fila, column=columna + 1, sticky="ew", padx=7, pady=7)
            setattr(self, atributo, entrada)

        ttk.Label(formulario, text="Rol").grid(row=2, column=2, sticky="w", padx=7, pady=7)
        self.combo_rol = ttk.Combobox(formulario, values=("Administrador", "Empleado", "Cliente"), state="readonly", width=27)
        self.combo_rol.grid(row=2, column=3, sticky="ew", padx=7, pady=7)
        self.combo_rol.set("Cliente")
        self.lbl_rol = ttk.Label(formulario, text="Rol seleccionado: Cliente", style="Info.TLabel")
        self.lbl_rol.grid(row=3, column=0, columnspan=4, sticky="w", padx=7, pady=(2, 4))
        for col in (1, 3):
            formulario.columnconfigure(col, weight=1)

        botones = ttk.Frame(self.contenido)
        botones.pack(fill="x", pady=(0, 12))
        ttk.Button(botones, text="＋ Registrar", command=self.registrar_usuario, style="Action.TButton").pack(side="left", padx=(0, 6))
        ttk.Button(botones, text="✎ Actualizar", command=self.actualizar_usuario, style="Action.TButton").pack(side="left", padx=6)
        ttk.Button(botones, text="🗑 Eliminar", command=self.eliminar_usuario, style="Danger.TButton").pack(side="left", padx=6)
        ttk.Button(botones, text="↺ Limpiar", command=self.limpiar_formulario_usuario, style="Secondary.TButton").pack(side="left", padx=6)
        tk.Label(botones, text="Enter: registrar   •   Escape: limpiar", bg="#F7F3EE", fg="#8A7A70", font=("Segoe UI", 9)).pack(side="right", padx=6)

        tabla_contenedor = ttk.LabelFrame(self.contenido, text="  Usuarios registrados  ", padding=10, style="Card.TLabelframe")
        tabla_contenedor.pack(fill="both", expand=True)
        columnas = ("identificacion", "nombre", "correo", "usuario", "rol")
        self.tabla_usuarios = ttk.Treeview(tabla_contenedor, columns=columnas, show="headings", selectmode="browse")
        for col, titulo, ancho in [
            ("identificacion", "Identificación", 145), ("nombre", "Nombre", 220), ("correo", "Correo", 245),
            ("usuario", "Usuario", 150), ("rol", "Rol", 125)]:
            self.tabla_usuarios.heading(col, text=titulo)
            self.tabla_usuarios.column(col, width=ancho, anchor="center")
        scrollbar = ttk.Scrollbar(tabla_contenedor, orient="vertical", command=self.tabla_usuarios.yview)
        self.tabla_usuarios.configure(yscrollcommand=scrollbar.set)
        self.tabla_usuarios.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.tabla_usuarios.bind("<<TreeviewSelect>>", self.al_seleccionar_usuario)
        for widget in (self.entry_identificacion, self.entry_nombre_usuario, self.entry_correo, self.entry_usuario_login, self.entry_clave, self.combo_rol):
            widget.bind("<Return>", self.al_presionar_enter)
        self.root.bind("<Escape>", self.al_presionar_escape)
        self.combo_rol.bind("<<ComboboxSelected>>", self.al_cambiar_rol)
        self.actualizar_tabla_usuarios()
        self.entry_identificacion.focus()
        self.establecer_estado("Gestión administrativa de usuarios activa.")

    def actualizar_tabla_usuarios(self):
        if not hasattr(self, "tabla_usuarios"):
            return
        for elemento in self.tabla_usuarios.get_children():
            self.tabla_usuarios.delete(elemento)
        for usuario in self.servicio.listar_usuarios():
            self.tabla_usuarios.insert("", "end", iid=usuario.identificacion, values=(usuario.identificacion, usuario.nombre, usuario.correo, usuario.usuario, usuario.rol))

    def al_seleccionar_usuario(self, event):
        seleccion = self.tabla_usuarios.selection()
        if not seleccion:
            return
        usuario = self.servicio.buscar_usuario(seleccion[0])
        if usuario is None:
            return
        self._set_entry(self.entry_identificacion, usuario.identificacion)
        self._set_entry(self.entry_nombre_usuario, usuario.nombre)
        self._set_entry(self.entry_correo, usuario.correo)
        self._set_entry(self.entry_usuario_login, usuario.usuario)
        self._set_entry(self.entry_clave, usuario.clave)
        self.combo_rol.set(usuario.rol)
        self.lbl_rol.config(text=f"Rol seleccionado: {usuario.rol}")
        self.establecer_estado(f"Usuario seleccionado: {usuario.nombre}.")

    @staticmethod
    def _set_entry(entry, value):
        entry.delete(0, tk.END)
        entry.insert(0, value)

    def al_presionar_enter(self, event):
        self.registrar_usuario()
        return "break"

    def al_presionar_escape(self, event):
        self.limpiar_formulario_usuario()
        return "break"

    def al_cambiar_rol(self, event):
        rol = self.combo_rol.get()
        self.lbl_rol.config(text=f"Rol seleccionado: {rol}")
        self.establecer_estado(f"Se seleccionó el rol {rol}.")

    def registrar_usuario(self):
        correcto, mensaje = self.servicio.registrar_usuario(self.entry_identificacion.get(), self.entry_nombre_usuario.get(), self.entry_correo.get(), self.entry_usuario_login.get(), self.entry_clave.get(), self.combo_rol.get())
        if correcto:
            messagebox.showinfo("Registro exitoso", mensaje)
            self.actualizar_tabla_usuarios(); self.limpiar_formulario_usuario(); self.establecer_estado(mensaje)
        else:
            messagebox.showerror("No se pudo registrar", mensaje)

    def actualizar_usuario(self):
        identificacion = self.entry_identificacion.get().strip()
        if not identificacion:
            messagebox.showwarning("Actualización", "Seleccione un usuario de la tabla."); return
        rol = self.combo_rol.get()
        if identificacion.casefold() == self.usuario_actual.identificacion.casefold() and rol != "Administrador":
            messagebox.showwarning("Cuenta actual", "La cuenta Administrador actualmente autenticada debe conservar ese rol.")
            self.combo_rol.set("Administrador"); self.lbl_rol.config(text="Rol seleccionado: Administrador"); return
        correcto, mensaje = self.servicio.actualizar_usuario(identificacion, self.entry_nombre_usuario.get(), self.entry_correo.get(), self.entry_usuario_login.get(), self.entry_clave.get(), rol)
        if correcto:
            messagebox.showinfo("Actualización", mensaje); self.actualizar_tabla_usuarios(); self.limpiar_formulario_usuario(); self.establecer_estado(mensaje)
        else:
            messagebox.showerror("No se pudo actualizar", mensaje)

    def eliminar_usuario(self):
        identificacion = self.entry_identificacion.get().strip()
        if not identificacion:
            messagebox.showwarning("Eliminación", "Seleccione un usuario de la tabla."); return
        usuario = self.servicio.buscar_usuario(identificacion)
        if usuario is None:
            messagebox.showerror("Eliminación", "No se encontró el usuario seleccionado."); return
        if not messagebox.askyesno("Confirmar eliminación", f"¿Eliminar la cuenta de '{usuario.nombre}'?\n\nEsta acción no se puede deshacer."):
            return
        correcto, mensaje = self.servicio.eliminar_usuario(identificacion, self.usuario_actual.identificacion)
        if correcto:
            messagebox.showinfo("Eliminación", mensaje); self.actualizar_tabla_usuarios(); self.limpiar_formulario_usuario(); self.establecer_estado(mensaje)
        else:
            messagebox.showerror("No se pudo eliminar", mensaje)

    def limpiar_formulario_usuario(self):
        if not hasattr(self, "entry_identificacion"):
            return
        for entry in (self.entry_identificacion, self.entry_nombre_usuario, self.entry_correo, self.entry_usuario_login, self.entry_clave):
            entry.delete(0, tk.END)
        self.combo_rol.set("Cliente")
        self.lbl_rol.config(text="Rol seleccionado: Cliente")
        if hasattr(self, "tabla_usuarios"):
            for elemento in self.tabla_usuarios.selection():
                self.tabla_usuarios.selection_remove(elemento)
        self.entry_identificacion.focus()
        self.establecer_estado("Formulario de usuario limpio.")

    # ==================== PRODUCTOS ====================
    def mostrar_productos(self):
        self.limpiar_contenido()

        ttk.Label(
            self.contenido,
            text="Gestión de productos",
            style="Section.TLabel"
        ).pack(anchor="w", pady=(0, 10))

        formulario = ttk.LabelFrame(
            self.contenido,
            text="Información del producto",
            padding=15
        )
        formulario.pack(fill="x", pady=(0, 10))

        campos = [
            ("Código:", "entry_codigo", 0, 0),
            ("Nombre:", "entry_nombre", 0, 2),
            ("Precio:", "entry_precio", 1, 0),
            ("Stock:", "entry_stock", 1, 2)
        ]

        for texto, atributo, fila, columna in campos:
            ttk.Label(formulario, text=texto).grid(
                row=fila, column=columna,
                sticky="w", padx=5, pady=5
            )
            entrada = ttk.Entry(formulario, width=25)
            entrada.grid(
                row=fila, column=columna + 1,
                padx=5, pady=5
            )
            setattr(self, atributo, entrada)

        botones = ttk.Frame(self.contenido)
        botones.pack(fill="x", pady=(0, 10))

        for texto, comando in [
            ("Registrar", self.registrar_producto),
            ("Cargar / Consultar", self.cargar_producto),
            ("Actualizar", self.actualizar_producto),
            ("Eliminar", self.eliminar_producto),
            ("Limpiar", self.limpiar_formulario),
        ]:
            ttk.Button(
                botones, text=texto, command=comando,
                style="Action.TButton"
            ).pack(side="left", padx=3)

        tabla_contenedor = ttk.LabelFrame(
            self.contenido,
            text="Productos registrados",
            padding=10
        )
        tabla_contenedor.pack(fill="both", expand=True)

        columnas = ("codigo", "nombre", "precio", "stock")
        self.tabla_productos = ttk.Treeview(
            tabla_contenedor,
            columns=columnas,
            show="headings",
            selectmode="browse"
        )

        for col, titulo, ancho in [
            ("codigo", "Código", 140),
            ("nombre", "Nombre", 300),
            ("precio", "Precio", 140),
            ("stock", "Stock", 120)
        ]:
            self.tabla_productos.heading(col, text=titulo)
            self.tabla_productos.column(col, width=ancho, anchor="center")

        scrollbar = ttk.Scrollbar(
            tabla_contenedor,
            orient="vertical",
            command=self.tabla_productos.yview
        )
        self.tabla_productos.configure(yscrollcommand=scrollbar.set)
        self.tabla_productos.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.actualizar_tabla()
        self.establecer_estado("Gestión de productos activa.")

    def actualizar_tabla(self):
        if not hasattr(self, "tabla_productos"):
            return

        for elemento in self.tabla_productos.get_children():
            self.tabla_productos.delete(elemento)

        for producto in self.servicio.listar_productos():
            self.tabla_productos.insert(
                "",
                "end",
                values=(
                    producto.codigo,
                    producto.nombre,
                    f"${producto.precio:.2f}",
                    producto.stock
                )
            )

    def registrar_producto(self):
        correcto, mensaje = self.servicio.registrar_producto(
            self.entry_codigo.get(),
            self.entry_nombre.get(),
            self.entry_precio.get(),
            self.entry_stock.get()
        )

        if correcto:
            messagebox.showinfo("Registro", mensaje)
            self.actualizar_tabla()
            self.limpiar_formulario()
        else:
            messagebox.showerror("Error", mensaje)

    def cargar_producto(self):
        codigo = self.entry_codigo.get().strip()
        if not codigo:
            messagebox.showwarning(
                "Consulta",
                "Ingrese el código del producto."
            )
            return

        producto = self.servicio.buscar_producto(codigo)
        if producto is None:
            messagebox.showerror(
                "Consulta",
                "No se encontró el producto."
            )
            return

        self.entry_nombre.delete(0, tk.END)
        self.entry_nombre.insert(0, producto.nombre)
        self.entry_precio.delete(0, tk.END)
        self.entry_precio.insert(0, producto.precio)
        self.entry_stock.delete(0, tk.END)
        self.entry_stock.insert(0, producto.stock)

    def actualizar_producto(self):
        correcto, mensaje = self.servicio.actualizar_producto(
            self.entry_codigo.get(),
            self.entry_nombre.get(),
            self.entry_precio.get(),
            self.entry_stock.get()
        )

        if correcto:
            messagebox.showinfo("Actualización", mensaje)
            self.actualizar_tabla()
            self.limpiar_formulario()
        else:
            messagebox.showerror("Error", mensaje)

    def eliminar_producto(self):
        codigo = self.entry_codigo.get().strip()
        if not codigo:
            messagebox.showwarning(
                "Eliminación",
                "Ingrese el código del producto."
            )
            return

        producto = self.servicio.buscar_producto(codigo)
        if producto is None:
            messagebox.showerror(
                "Eliminación",
                "No se encontró el producto."
            )
            return

        if not messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Desea eliminar '{producto.nombre}'?"
        ):
            return

        correcto, mensaje = self.servicio.eliminar_producto(codigo)

        if correcto:
            messagebox.showinfo("Eliminación", mensaje)
            self.actualizar_tabla()
            self.limpiar_formulario()
        else:
            messagebox.showerror("Error", mensaje)

    def limpiar_formulario(self):
        for entrada in (
            self.entry_codigo,
            self.entry_nombre,
            self.entry_precio,
            self.entry_stock
        ):
            entrada.delete(0, tk.END)

        self.entry_codigo.focus()

    # ==================== VENTAS ====================
    def mostrar_ventas(self):
        self.limpiar_contenido()

        ttk.Label(
            self.contenido,
            text="Registro de ventas",
            style="Section.TLabel"
        ).pack(anchor="w", pady=(0, 10))

        formulario = ttk.LabelFrame(
            self.contenido, text="Nueva venta", padding=15
        )
        formulario.pack(fill="x", pady=(0, 10))

        ttk.Label(formulario, text="Usuario:").grid(
            row=0, column=0, sticky="w", padx=5, pady=6
        )
        usuarios = [
            f"{u.identificacion} - {u.nombre}"
            for u in self.servicio.listar_usuarios()
        ]
        self.combo_usuario = ttk.Combobox(
            formulario, values=usuarios,
            state="readonly", width=42
        )
        self.combo_usuario.grid(
            row=0, column=1, padx=5, pady=6
        )

        ttk.Label(formulario, text="Producto:").grid(
            row=1, column=0, sticky="w", padx=5, pady=6
        )
        productos = [
            f"{p.codigo} - {p.nombre}"
            for p in self.servicio.listar_productos()
        ]
        self.combo_producto = ttk.Combobox(
            formulario, values=productos,
            state="readonly", width=42
        )
        self.combo_producto.grid(
            row=1, column=1, padx=5, pady=6
        )

        ttk.Label(formulario, text="Cantidad:").grid(
            row=2, column=0, sticky="w", padx=5, pady=6
        )
        self.entry_cantidad = ttk.Entry(formulario, width=45)
        self.entry_cantidad.insert(0, "1")
        self.entry_cantidad.grid(
            row=2, column=1, padx=5, pady=6
        )

        ttk.Button(
            formulario,
            text="Registrar venta",
            command=self.registrar_venta,
            style="Action.TButton"
        ).grid(
            row=3, column=1, sticky="w",
            padx=5, pady=10
        )

        tabla_contenedor = ttk.LabelFrame(
            self.contenido, text="Ventas registradas", padding=10
        )
        tabla_contenedor.pack(fill="both", expand=True)

        columnas = ("usuario", "producto", "cantidad", "fecha")
        self.tabla_ventas = ttk.Treeview(
            tabla_contenedor,
            columns=columnas,
            show="headings"
        )

        for col, titulo, ancho in [
            ("usuario", "Usuario", 230),
            ("producto", "Producto", 250),
            ("cantidad", "Cantidad", 100),
            ("fecha", "Fecha", 190)
        ]:
            self.tabla_ventas.heading(col, text=titulo)
            self.tabla_ventas.column(col, width=ancho, anchor="center")

        scrollbar = ttk.Scrollbar(
            tabla_contenedor,
            orient="vertical",
            command=self.tabla_ventas.yview
        )
        self.tabla_ventas.configure(yscrollcommand=scrollbar.set)
        self.tabla_ventas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.actualizar_tabla_ventas()
        self.establecer_estado("Registro de ventas activo.")

    def registrar_venta(self):
        usuario_seleccionado = self.combo_usuario.get().strip()
        producto_seleccionado = self.combo_producto.get().strip()
        cantidad = self.entry_cantidad.get().strip()

        if not usuario_seleccionado or not producto_seleccionado:
            messagebox.showwarning(
                "Venta",
                "Seleccione un usuario y un producto."
            )
            return

        identificacion = usuario_seleccionado.split(" - ", 1)[0]
        codigo_producto = producto_seleccionado.split(" - ", 1)[0]

        correcto, mensaje = self.servicio.registrar_venta(
            identificacion, codigo_producto, cantidad
        )

        if correcto:
            messagebox.showinfo("Venta registrada", mensaje)
            self.actualizar_tabla_ventas()

            # Refresca productos porque la venta descuenta stock.
            self.actualizar_combos_venta()

            self.entry_cantidad.delete(0, tk.END)
            self.entry_cantidad.insert(0, "1")
        else:
            messagebox.showerror("Error en la venta", mensaje)

    def actualizar_combos_venta(self):
        if hasattr(self, "combo_usuario"):
            self.combo_usuario["values"] = [
                f"{u.identificacion} - {u.nombre}"
                for u in self.servicio.listar_usuarios()
            ]

        if hasattr(self, "combo_producto"):
            self.combo_producto["values"] = [
                f"{p.codigo} - {p.nombre}"
                for p in self.servicio.listar_productos()
            ]

    def actualizar_tabla_ventas(self):
        if not hasattr(self, "tabla_ventas"):
            return

        for elemento in self.tabla_ventas.get_children():
            self.tabla_ventas.delete(elemento)

        for venta in self.servicio.listar_ventas():
            usuario = self.servicio.buscar_usuario(
                venta.identificacion_usuario
            )
            producto = self.servicio.buscar_producto(
                venta.codigo_producto
            )

            nombre_usuario = (
                usuario.nombre if usuario else venta.identificacion_usuario
            )
            nombre_producto = (
                producto.nombre if producto else venta.codigo_producto
            )

            self.tabla_ventas.insert(
                "",
                "end",
                values=(
                    nombre_usuario,
                    nombre_producto,
                    venta.cantidad,
                    venta.fecha or "—"
                )
            )
