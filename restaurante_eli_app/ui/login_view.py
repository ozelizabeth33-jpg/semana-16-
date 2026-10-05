import tkinter as tk
from pathlib import Path
from tkinter import ttk, messagebox


class LoginView:
    def __init__(self, root, servicio, abrir_principal):
        self.root = root
        self.servicio = servicio
        self.abrir_principal = abrir_principal
        self.root.title("Sazón & Mesa | Acceso")
        self.root.geometry("620x760")
        self.root.minsize(620, 720)
        self.root.resizable(False, False)
        self.root.configure(bg="#F7F3EE")
        self.logo = None
        self.crear_interfaz()

    def crear_interfaz(self):
        estilo = ttk.Style()
        try:
            estilo.theme_use("clam")
        except tk.TclError:
            pass
        estilo.configure("TFrame", background="#F7F3EE")
        estilo.configure("Title.TLabel", background="#F7F3EE", foreground="#5A1E22", font=("Segoe UI", 26, "bold"))
        estilo.configure("Sub.TLabel", background="#F7F3EE", foreground="#7D6E65", font=("Segoe UI", 10))
        estilo.configure("Login.TLabelframe", background="#FFFFFF", foreground="#5A1E22", bordercolor="#E4D6C8")
        estilo.configure("Login.TLabelframe.Label", background="#FFFFFF", foreground="#5A1E22", font=("Segoe UI", 11, "bold"))
        estilo.configure("Login.TButton", background="#A8462D", foreground="#FFFFFF", font=("Segoe UI", 11, "bold"), padding=(12, 11), borderwidth=0)
        estilo.map("Login.TButton", background=[("active", "#873521"), ("pressed", "#6F291B")])
        estilo.configure("TEntry", padding=9)

        contenedor = tk.Frame(self.root, bg="#F7F3EE")
        contenedor.pack(fill="both", expand=True, padx=42, pady=24)

        # Logo reducido para que el botón siempre quede visible en la ventana.
        ruta_logo = Path(__file__).resolve().parent.parent / "assets" / "logo.png"
        if ruta_logo.exists():
            try:
                imagen = tk.PhotoImage(file=str(ruta_logo))
                # El logo original es 420x180; se reduce a 210x90.
                self.logo = imagen.subsample(2, 2)
                tk.Label(contenedor, image=self.logo, bg="#F7F3EE").pack(pady=(0, 8))
            except tk.TclError:
                pass

        ttk.Label(contenedor, text="SAZÓN & MESA", style="Title.TLabel").pack()
        ttk.Label(contenedor, text="Sistema de gestión del restaurante", style="Sub.TLabel").pack(pady=(2, 14))

        formulario = ttk.LabelFrame(contenedor, text="  Iniciar sesión  ", padding=22, style="Login.TLabelframe")
        formulario.pack(fill="x")

        ttk.Label(formulario, text="Usuario, nombre o correo electrónico").grid(row=0, column=0, sticky="w", pady=(0, 6))
        self.acceso = ttk.Entry(formulario, width=40)
        self.acceso.grid(row=1, column=0, sticky="ew", pady=(0, 14))

        ttk.Label(formulario, text="Contraseña").grid(row=2, column=0, sticky="w", pady=(0, 6))
        self.clave = ttk.Entry(formulario, width=40, show="•")
        self.clave.grid(row=3, column=0, sticky="ew", pady=(0, 5))
        formulario.columnconfigure(0, weight=1)

        ttk.Label(formulario, text="Entre 6 y 12 caracteres.", style="Sub.TLabel").grid(row=4, column=0, sticky="w", pady=(0, 2))

        # Botón en un bloque independiente y visible.
        self.boton_ingresar = ttk.Button(
            contenedor, text="🔐  INGRESAR AL SISTEMA",
            command=self.iniciar_sesion, style="Login.TButton"
        )
        self.boton_ingresar.pack(fill="x", pady=(18, 10), ipady=2)

        ttk.Label(contenedor, text="Puedes ingresar con tu usuario, nombre o correo electrónico.", style="Sub.TLabel").pack()
        ttk.Label(contenedor, text="Sazón & Mesa • Gestión de Restaurante", style="Sub.TLabel").pack(pady=(8, 0))

        self.acceso.focus_set()
        self.root.bind("<Return>", self._enter)

    def _enter(self, event=None):
        self.iniciar_sesion()
        return "break"

    def iniciar_sesion(self):
        acceso = self.acceso.get().strip()
        clave = self.clave.get().strip()
        if not acceso or not clave:
            messagebox.showwarning("Datos incompletos", "Ingrese su usuario o correo y su contraseña.", parent=self.root)
            return
        if not 6 <= len(clave) <= 12:
            messagebox.showwarning("Contraseña no válida", "La contraseña debe tener entre 6 y 12 caracteres.", parent=self.root)
            return
        usuario = self.servicio.validar_acceso(acceso, clave)
        if usuario:
            self.root.destroy()
            self.abrir_principal(usuario)
        else:
            messagebox.showerror("Acceso denegado", "Usuario/correo o contraseña incorrectos.", parent=self.root)
            self.clave.select_range(0, tk.END)
            self.clave.focus_set()
