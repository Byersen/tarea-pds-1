# tarea-pds-1

Proyecto de ejemplo: CRUD de usuarios en memoria con pruebas basadas en propiedades (Hypothesis).

## Descripción

Este repositorio implementa un ejemplo sencillo de un CRUD (Create, Read, Update, Delete) para entidades `User` almacenadas en memoria. Incluye:

- Un modelo de usuario y un repositorio en `user_model.py`.
- Un script demostrativo `demo_crud.py` que muestra el uso del CRUD.
- Pruebas basadas en propiedades usando `hypothesis` y `pytest` en `test_user_properties.py`.

El objetivo es servir como ejercicio educativo sobre diseño de modelos, validación de datos y testing basado en propiedades.

## Características

- Crear, leer, actualizar, eliminar y listar usuarios en memoria.
- Validaciones básicas de datos (nombre no vacío, email con `@`, edad entre 0 y 150).
- Pruebas de propiedades que verifican invariantes del sistema (p. ej. crear -> leer conserva los datos).

## Requisitos

- Python 3.8+
- Dependencias (ver `requirements.txt`):
	- hypothesis
	- pytest

## Instalación (Windows PowerShell)

Abre PowerShell y ejecuta:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Nota: en otras shells (bash, WSL) activa el virtualenv con `source .venv/bin/activate`.

## Uso rápido

Ejecuta la demostración para ver cómo funciona el CRUD:

```powershell
python demo_crud.py
```

El script imprimirá ejemplos de creación, lectura, actualización, listado, eliminación y ejemplos de validación.

## Ejecutar pruebas

Las pruebas usan `pytest` y `hypothesis`. Para ejecutarlas:

```powershell
pytest test_user_properties.py -v
```

Recomendación: ejecuta las pruebas dentro del virtualenv creado en la sección de instalación.

## Estructura de archivos

- `user_model.py` - Contiene la clase `User` (con validaciones) y la clase `UserRepository` (CRUD en memoria).
- `demo_crud.py` - Script que demuestra las operaciones del repositorio y muestra ejemplos de validación.
- `test_user_properties.py` - Pruebas basadas en propiedades con Hypothesis para las operaciones y validaciones.
- `requirements.txt` - Dependencias necesarias para ejecutar las pruebas.

## Contrato (resumen técnico)

- Entradas principales: name (str), email (str), age (int), active (bool opcional).
- Salidas: objetos `User` con `id` (UUID string) y métodos del repositorio que retornan `User`, `bool` o `None` según la operación.
- Modos de error: las validaciones del modelo lanzan `ValueError` si los datos no cumplen reglas; las operaciones sobre IDs inexistentes retornan `None` o `False` según corresponda.

## Casos borde considerados

- Nombres vacíos o solo espacios -> ValueError.
- Emails sin `@` -> ValueError.
- Edades fuera del rango [0, 150] -> ValueError.
- Intentar leer/actualizar/eliminar un ID inexistente -> comportamiento seguro (`None` o `False`).

## Desarrollo y contribuciones

1. Haz un fork o clona el repositorio.
2. Crea un entorno virtual y activa (ver arriba).
3. Instala dependencias y añade tests para cambios nuevos.
4. Asegúrate de que las pruebas pasen antes de abrir un pull request.

## Licencia

Este repositorio no incluye un archivo de licencia por defecto. Añade una licencia apropiada si planeas compartir o distribuir el código.

## Contacto

Si tienes preguntas o sugerencias, abre un issue en el repositorio.

---

Pequeña nota: si quieres puedo añadir badges, un archivo CONTRIBUTING.md, o examples/ con salidas de ejemplo del `demo_crud.py`.