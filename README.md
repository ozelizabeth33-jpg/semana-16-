# RESTAURANTE APP - SEMANA 16

## Programación Orientada a Objetos

Aplicación gráfica desarrollada en Python con Tkinter/ttk para la gestión básica de un restaurante. La Semana 16 continúa el proyecto construido anteriormente y amplía la sección de **Usuarios** para demostrar el manejo de eventos en Tkinter.

La aplicación conserva las funcionalidades de inicio de sesión, productos y ventas, y añade una gestión administrativa de usuarios con roles, `Treeview`, `bind()`, callbacks y atajos de teclado.

## Objetivo de la Semana 16

Aplicar el manejo de eventos en una situación real del sistema:

```text
Interacción del usuario
        ↓
Evento
        ↓
bind() / command=
        ↓
Callback
        ↓
RestauranteServicio
        ↓
Persistencia JSON
        ↓
Respuesta visual
```

## Funcionalidades

### Inicio de sesión
- Acceso mediante identificación y nombre.
- El sistema identifica el rol del usuario autenticado.
- La gestión administrativa de usuarios está disponible únicamente para el rol **Administrador**.

### Gestión de usuarios
El Administrador puede:
- Registrar usuarios.
- Consultar usuarios mediante `Treeview`.
- Actualizar usuarios.
- Eliminar usuarios con confirmación.
- Seleccionar los roles **Administrador, Empleado y Cliente**.
- No eliminar accidentalmente la cuenta Administrador actualmente autenticada.
- Evitar que el sistema quede sin ningún Administrador.

### Eventos implementados

#### `<<TreeviewSelect>>`
Se asocia mediante `bind()` al `Treeview` de usuarios. Al seleccionar una fila:
1. Se obtiene el identificador del registro seleccionado.
2. Se consulta el objeto mediante `RestauranteServicio`.
3. Los datos se cargan automáticamente en el formulario.

El `Treeview` muestra únicamente identificación, nombre y rol; no contiene información sensible.

#### `<Return>`
Se utiliza como atajo de teclado para ejecutar el registro del usuario. El callback reutiliza `registrar_usuario()` y no duplica la lógica de negocio.

#### `<Escape>`
Limpia el formulario, cancela la selección actual y devuelve la interfaz a un estado inicial.

#### `<<ComboboxSelected>>`
Se aplica al selector de roles. Al cambiar el rol se actualiza la indicación visual de la interfaz.

#### `command=`
Los botones principales utilizan `command=` para ejecutar sus callbacks:
- Registrar
- Actualizar
- Eliminar
- Limpiar
- Registrar venta
- Navegación entre secciones

## Arquitectura modular

```text
restaurante_eli_app/
├── datos/
│   ├── productos.json
│   ├── usuarios.json
│   └── ventas.json
├── modelos/
│   ├── __init__.py
│   ├── producto.py
│   ├── usuario.py
│   └── venta.py
├── servicios/
│   ├── __init__.py
│   ├── archivo_servicio.py
│   └── restaurante_servicio.py
├── ui/
│   ├── __init__.py
│   ├── login_view.py
│   └── main_view.py
├── assets/
│   ├── logo.png
│   └── venta.png
└── main.py
```

## Separación de responsabilidades

- **Modelos:** representan `Usuario`, `Producto` y `Venta`.
- **ArchivoServicio:** centraliza la lectura y escritura de archivos JSON.
- **RestauranteServicio:** contiene validaciones, reglas de negocio, CRUD y persistencia.
- **LoginView:** captura los datos de acceso y responde al evento de ingreso.
- **MainView:** presenta la interfaz, captura eventos y coordina callbacks.
- **main.py:** inicia el sistema y controla el flujo de sesión.

La interfaz no lee ni escribe directamente los archivos JSON.

## Persistencia

Los datos se almacenan en:

- `datos/usuarios.json`
- `datos/productos.json`
- `datos/ventas.json`

Los usuarios incluyen:

```json
{
    "identificacion": "0102030405",
    "nombre": "Elizabeth",
    "rol": "Administrador"
}
```

## Ejecución

Se requiere Python 3.x.

Abrir una terminal en la carpeta:

```bash
cd restaurante_eli_app
python main.py
```

No se requieren librerías externas.

## Pruebas funcionales recomendadas

1. Ejecutar `main.py`.
2. Iniciar sesión con un usuario registrado.
3. Comprobar que el Administrador vea la sección **Usuarios**.
4. Comprobar que un Empleado o Cliente no tenga acceso a la gestión administrativa.
5. Registrar un usuario Empleado o Cliente.
6. Confirmar que aparezca en el `Treeview`.
7. Seleccionar una fila y verificar `<<TreeviewSelect>>`.
8. Cambiar el rol y verificar `<<ComboboxSelected>>`.
9. Actualizar un usuario.
10. Eliminar un usuario y confirmar la operación.
11. Intentar eliminar la cuenta Administrador actualmente autenticada y comprobar que el sistema lo impida.
12. Usar **Enter** para registrar.
13. Usar **Escape** para limpiar el formulario.
14. Cerrar y volver a ejecutar la aplicación.
15. Verificar que los usuarios se recuperen desde `usuarios.json`.
16. Probar Productos y Ventas para confirmar que las funciones anteriores continúan funcionando.

## Tecnologías

- Python 3
- Tkinter / ttk
- Programación Orientada a Objetos
- Archivos JSON
- Visual Studio Code
- GitHub

## Semana 16

La evolución principal de esta semana es la gestión de usuarios basada en eventos, manteniendo la reutilización de código y la separación entre interfaz, modelos, servicios y persistencia.


## Semana 16 — Manejo de eventos en Tkinter

La aplicación evolucionó para gestionar usuarios mediante un formulario y un `Treeview`, manteniendo la arquitectura modular y la persistencia en JSON.

### Mejoras implementadas
- CRUD de usuarios: registrar, consultar, actualizar y eliminar.
- Roles: Administrador, Empleado y Cliente.
- Acceso administrativo exclusivo para Administradores.
- Inicio de sesión mediante **usuario o correo electrónico + contraseña**. La identificación ya no funciona como contraseña.
- Contraseñas de 6 a 12 caracteres.
- Eventos `<<TreeviewSelect>>`, `<Return>`, `<Escape>` y `<<ComboboxSelected>>` mediante `bind()`.
- Botones de acciones principales mediante `command=`.
- Persistencia de usuarios en `datos/usuarios.json`.
- Interfaz renovada con colores, tarjetas, tabla estilizada y logotipo propio en `assets/`.

### Acceso inicial de prueba
- Usuario: `admin`
- Correo: `admin@sazonmesa.com`
- Contraseña: `admin12`

### Ejecución
Desde la carpeta `restaurante_eli_app` ejecutar:

```bash
python main.py
```
