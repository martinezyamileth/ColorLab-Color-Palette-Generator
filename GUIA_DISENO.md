# Guía rápida para personalizar ColorLab

Abre **styles/style.css** en VS Code. Los algoritmos siguen en `algoritmos/color.py` y la interfaz funcional en `app.py`.

## Cambios más comunes

- **Fondo principal:** `.stApp` → `background`
- **Color del texto:** `.stApp` y reglas `.block-container` → `color`
- **Encabezado grande:** `.hero` → `background`, `padding`, `border-radius`
- **Título ColorLab:** `.hero h1` → `font-size`, `color`
- **Texto del encabezado:** `.hero .subtitle` → `color`, `font-size`
- **Barra lateral:** `[data-testid="stSidebar"]` → `background`
- **Botón principal:** `.block-container .stButton > button[kind="primary"]`
- **Tarjetas de colores:** `.color-card`, `.color-chip`, `.color-code`, `.color-meta`
- **Recuadro de instrucciones:** `.section-intro`

Ejemplo: cambia `background:#142D43;` en `.hero` por `background:#49366D;` para un encabezado morado.

## Ver cambios

1. Abre la carpeta del proyecto en VS Code.
2. Ejecuta `python -m pip install -r requirements.txt` (solo la primera vez).
3. Ejecuta `python -m streamlit run app.py`.
4. Modifica `styles/style.css`, guarda con **Ctrl+S** y recarga la página si hace falta.

**Nota:** El HTML de los bloques visuales sigue dentro de `app.py` porque Streamlit genera la interfaz. Se ha separado el CSS completo para que sea fácil de editar. No borres las reglas de contraste sin comprobar que los textos siguen siendo legibles.

## Tema claro forzado

El archivo `.streamlit/config.toml` fuerza el tema claro. Sin él, Streamlit hereda el modo oscuro de Windows/navegador y la barra superior, el cargador de archivos y los avisos quedan con texto ilegible. Ejecuta siempre `streamlit run app.py` desde la carpeta del proyecto para que lo lea.
