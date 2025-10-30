# Cómo Lanzar la Aplicación de Finanzas

Sigue estos pasos para poner en marcha la aplicación en tu ordenador local.

## Requisitos Previos

-   Tener Python 3.8 o superior instalado en tu sistema.
-   Tener todos los archivos del proyecto en un directorio (`mi_app_finanzas`).

## Pasos para la Ejecución

### 1. Crear y Activar el Entorno Virtual

Un entorno virtual es una buena práctica para aislar las dependencias del proyecto.

-   Abre una terminal (o Símbolo del sistema en Windows).
-   Navega hasta el directorio raíz del proyecto.

-   **Crea el entorno virtual** (solo necesitas hacerlo la primera vez):
    ```bash
    python3 -m venv venv
    ```

-   **Activa el entorno virtual** (debes hacerlo cada vez que abras una nueva terminal para trabajar en el proyecto):
    -   En **macOS / Linux**:
        ```bash
        source venv/bin/activate
        ```
    -   En **Windows**:
        ```bash
        venv\Scripts\activate
        ```
    *Deberías ver `(venv)` al principio de la línea de comandos, indicando que el entorno está activo.*

### 2. Instalar las Dependencias

Con el entorno virtual activo, instala todas las librerías que la aplicación necesita.

```bash
pip install -r requirements.txt
```

### 3. Ejecutar la Aplicación

Una vez instaladas las dependencias, ya puedes lanzar la aplicación con Streamlit.

```bash
streamlit run app.py
```

La aplicación se abrirá automáticamente en una nueva pestaña de tu navegador web. Si no lo hace, la terminal te mostrará una URL local (normalmente `http://localhost:8501`) que puedes abrir manualmente.

---

**¡Y eso es todo! Ya puedes empezar a gestionar tus finanzas.**