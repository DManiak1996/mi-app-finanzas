"""
Sistema de Feature Flags para el Overhaul de Diseño

Este módulo proporciona un sistema de feature flags para habilitar gradualmente
el nuevo diseño sin afectar la funcionalidad existente.

Estrategia:
- Todos los flags inician en False (diseño viejo activo)
- Se activan gradualmente según fase de desarrollo
- Permite rollback instantáneo en caso de problemas
- Soporta testing A/B y migración por componente

Uso básico:
    from utils.feature_flags import FeatureFlags, is_enabled

    if is_enabled('USE_NEW_DASHBOARD'):
        render_dashboard_v2()
    else:
        render_dashboard_v1()

Autor: Claude Code
Fecha: 2025-12-04
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional


class FeatureFlags:
    """
    Control centralizado de características en desarrollo.

    Organizado por fases según la estrategia de migración:
    - FASE 0: Master flag y preparación
    - FASE 1: Design system y fundamentos
    - FASE 2: Componentes individuales
    - FASE 3: Layouts y sistemas
    - FASE 4: Páginas completas
    - FASE 5: Features avanzados
    """

    # ==========================================
    # FASE 0: MASTER FLAG
    # ==========================================
    USE_NEW_DESIGN = True  # ✅ ACTIVADO - Bugs corregidos: gap parameter + HTML rendering
    """
    Master flag: Si es True, activa automáticamente todos los flags.
    Útil para activar el diseño completo de una vez en producción.
    """

    # ==========================================
    # FASE 1: DESIGN SYSTEM (Fundamentos)
    # ==========================================
    USE_NEW_COMPONENTS = False  # ⚠️ DESACTIVADO temporalmente
    """
    Activa los componentes wrapper del nuevo design system.
    No afecta la UI visualmente, solo reorganiza el código.
    """

    USE_NEW_CSS_MODULE = False  # ⚠️ DESACTIVADO temporalmente
    """
    Usa el CSS extraído del app.py al módulo separado.
    Permite mantener estilos centralizados y consistentes.
    """

    USE_NEW_PLOTLY_THEME = False  # ⚠️ DESACTIVADO temporalmente
    """
    Activa el tema unificado de Plotly para todos los gráficos.
    Incluye colores, tipografía y estilos consistentes.
    """

    # ==========================================
    # FASE 2: COMPONENTES (UI Aislada)
    # ==========================================
    USE_METRIC_CARDS = False  # ⚠️ DESACTIVADO temporalmente
    """
    Usa el componente MetricCard para métricas del dashboard.
    Reemplaza st.metric() con versión estilizada.
    """

    USE_CHART_TEMPLATES = False  # ⚠️ DESACTIVADO temporalmente
    """
    Activa plantillas de gráficos predefinidas.
    Estandariza la creación de gráficos en toda la app.
    """

    USE_LAYOUT_SYSTEM = False  # ⚠️ DESACTIVADO temporalmente
    """
    Usa el sistema de layouts (Grid, Container, etc).
    Mejora la organización espacial de la UI.
    """

    USE_FORM_CARDS = False  # ⚠️ DESACTIVADO temporalmente
    """
    Activa el componente FormCard para formularios.
    Estandariza la apariencia de formularios.
    """

    USE_DATA_TABLES = False  # ⚠️ DESACTIVADO temporalmente
    """
    Usa el componente DataTable para tablas de datos.
    Mejora la presentación de datos tabulares.
    """

    # ==========================================
    # FASE 3: PAGES (Rediseño por página)
    # ==========================================
    USE_NEW_DASHBOARD = False  # ⚠️ DESACTIVADO - render_metric_grid no funciona correctamente
    """
    Activa el dashboard rediseñado (v2).
    Incluye nuevo layout, métricas y gráficos.
    ESTADO: ACTIVO - Dashboard migrado al nuevo sistema de diseño
    """

    USE_NEW_TRANSACCIONES = False  # ⚠️ DESACTIVADO temporalmente
    """
    Activa la página de transacciones rediseñada (v2).
    Mejora filtros, tabla y visualización.
    """

    USE_NEW_IMPORTAR = False  # ⚠️ DESACTIVADO temporalmente
    """
    Activa la página de importación rediseñada (v2).
    Mejora el flujo de importación de archivos.
    """

    USE_NEW_CATEGORIAS = False  # ⚠️ DESACTIVADO temporalmente
    """
    Activa la página de categorías rediseñada (v2).
    Mejora la gestión de categorías.
    """

    USE_NEW_CONFIGURACION = False  # ⚠️ DESACTIVADO temporalmente
    """
    Activa la página de configuración rediseñada (v2).
    Mejora la organización de ajustes.
    """

    USE_NEW_COCHE_ELECTRICO = False  # ⚠️ DESACTIVADO temporalmente
    """
    Activa la página de coche eléctrico rediseñada (v2).
    Mejora tracking de cargas y estadísticas.
    """

    USE_NEW_ASISTENTE_IA = False  # ⚠️ DESACTIVADO temporalmente
    """
    Activa la página de asistente IA rediseñada (v2).
    Mejora la interfaz de chat y sugerencias.
    """

    # ==========================================
    # FASE 4: FEATURES AVANZADOS
    # ==========================================
    DARK_MODE = False
    """
    Activa el modo oscuro en toda la aplicación.
    Incluye paleta de colores alternativa.
    """

    RESPONSIVE_MOBILE = False
    """
    Activa optimizaciones para dispositivos móviles.
    Ajusta layouts y componentes para pantallas pequeñas.
    """

    ANIMATIONS = False
    """
    Activa animaciones y transiciones suaves.
    Mejora la experiencia de usuario con feedback visual.
    """

    ACCESSIBILITY_FEATURES = False
    """
    Activa características de accesibilidad.
    Incluye ARIA labels, contraste mejorado, etc.
    """

    # ==========================================
    # FASE 5: DEBUGGING Y DESARROLLO
    # ==========================================
    DEBUG_MODE = False
    """
    Activa modo debug que muestra información adicional.
    Útil para desarrollo y troubleshooting.
    """

    SHOW_FLAG_STATUS = False
    """
    Muestra el estado de los feature flags en la UI.
    Útil para verificar qué flags están activos.
    """


# ==========================================
# FUNCIONES HELPER
# ==========================================

def is_enabled(flag_name: str) -> bool:
    """
    Verifica si un feature flag específico está activo.

    Si USE_NEW_DESIGN (master flag) está activo, todos los flags
    de diseño se consideran activos automáticamente.

    Args:
        flag_name: Nombre del flag a verificar (ej: 'USE_NEW_DASHBOARD')

    Returns:
        bool: True si el flag está activo, False si no

    Ejemplo:
        >>> if is_enabled('USE_NEW_DASHBOARD'):
        ...     render_dashboard_v2()
        ... else:
        ...     render_dashboard_v1()
    """
    # Verificar que el flag existe
    if not hasattr(FeatureFlags, flag_name):
        if FeatureFlags.DEBUG_MODE:
            print(f"⚠️  Warning: Flag '{flag_name}' no existe")
        return False

    # Si el master flag está activo, todos los flags de diseño están activos
    # (excepto DEBUG_MODE y SHOW_FLAG_STATUS que son independientes)
    if FeatureFlags.USE_NEW_DESIGN and flag_name not in ['DEBUG_MODE', 'SHOW_FLAG_STATUS']:
        return True

    # Retornar el valor del flag
    return getattr(FeatureFlags, flag_name)


def get_all_flags() -> Dict[str, bool]:
    """
    Obtiene el estado de todos los feature flags.

    Útil para debugging y para mostrar el estado actual del sistema.

    Returns:
        Dict[str, bool]: Diccionario con nombre y estado de cada flag

    Ejemplo:
        >>> flags = get_all_flags()
        >>> print(f"Flags activos: {sum(flags.values())}/{len(flags)}")
    """
    flags = {}
    for attr in dir(FeatureFlags):
        # Filtrar solo los flags (mayúsculas y sin guiones bajos al inicio)
        if attr.isupper() and not attr.startswith('_'):
            flags[attr] = is_enabled(attr)
    return flags


def get_active_flags() -> List[str]:
    """
    Obtiene una lista de todos los flags activos.

    Returns:
        List[str]: Lista con los nombres de los flags activos

    Ejemplo:
        >>> active = get_active_flags()
        >>> print(f"Flags activos: {', '.join(active)}")
    """
    return [name for name, value in get_all_flags().items() if value]


def get_flags_by_phase() -> Dict[str, Dict[str, bool]]:
    """
    Organiza los flags por fase de desarrollo.

    Returns:
        Dict[str, Dict[str, bool]]: Flags organizados por fase

    Ejemplo:
        >>> phases = get_flags_by_phase()
        >>> for phase, flags in phases.items():
        ...     print(f"{phase}: {len([f for f in flags.values() if f])} activos")
    """
    all_flags = get_all_flags()

    phases = {
        "FASE 0: Master Flag": {
            'USE_NEW_DESIGN': all_flags.get('USE_NEW_DESIGN', False),
        },
        "FASE 1: Design System": {
            'USE_NEW_COMPONENTS': all_flags.get('USE_NEW_COMPONENTS', False),
            'USE_NEW_CSS_MODULE': all_flags.get('USE_NEW_CSS_MODULE', False),
            'USE_NEW_PLOTLY_THEME': all_flags.get('USE_NEW_PLOTLY_THEME', False),
        },
        "FASE 2: Componentes": {
            'USE_METRIC_CARDS': all_flags.get('USE_METRIC_CARDS', False),
            'USE_CHART_TEMPLATES': all_flags.get('USE_CHART_TEMPLATES', False),
            'USE_LAYOUT_SYSTEM': all_flags.get('USE_LAYOUT_SYSTEM', False),
            'USE_FORM_CARDS': all_flags.get('USE_FORM_CARDS', False),
            'USE_DATA_TABLES': all_flags.get('USE_DATA_TABLES', False),
        },
        "FASE 3: Pages": {
            'USE_NEW_DASHBOARD': all_flags.get('USE_NEW_DASHBOARD', False),
            'USE_NEW_TRANSACCIONES': all_flags.get('USE_NEW_TRANSACCIONES', False),
            'USE_NEW_IMPORTAR': all_flags.get('USE_NEW_IMPORTAR', False),
            'USE_NEW_CATEGORIAS': all_flags.get('USE_NEW_CATEGORIAS', False),
            'USE_NEW_CONFIGURACION': all_flags.get('USE_NEW_CONFIGURACION', False),
            'USE_NEW_COCHE_ELECTRICO': all_flags.get('USE_NEW_COCHE_ELECTRICO', False),
            'USE_NEW_ASISTENTE_IA': all_flags.get('USE_NEW_ASISTENTE_IA', False),
        },
        "FASE 4: Features Avanzados": {
            'DARK_MODE': all_flags.get('DARK_MODE', False),
            'RESPONSIVE_MOBILE': all_flags.get('RESPONSIVE_MOBILE', False),
            'ANIMATIONS': all_flags.get('ANIMATIONS', False),
            'ACCESSIBILITY_FEATURES': all_flags.get('ACCESSIBILITY_FEATURES', False),
        },
        "DEBUG": {
            'DEBUG_MODE': all_flags.get('DEBUG_MODE', False),
            'SHOW_FLAG_STATUS': all_flags.get('SHOW_FLAG_STATUS', False),
        }
    }

    return phases


def enable_flag(flag_name: str) -> bool:
    """
    Activa un feature flag específico.

    NOTA: Solo modifica en memoria, no persiste.
    Para persistir, usar save_flags_to_file().

    Args:
        flag_name: Nombre del flag a activar

    Returns:
        bool: True si se activó correctamente, False si no existe

    Ejemplo:
        >>> enable_flag('USE_NEW_DASHBOARD')
        >>> save_flags_to_file()  # Para persistir
    """
    if not hasattr(FeatureFlags, flag_name):
        if FeatureFlags.DEBUG_MODE:
            print(f"⚠️  Warning: Flag '{flag_name}' no existe")
        return False

    setattr(FeatureFlags, flag_name, True)
    return True


def disable_flag(flag_name: str) -> bool:
    """
    Desactiva un feature flag específico.

    NOTA: Solo modifica en memoria, no persiste.
    Para persistir, usar save_flags_to_file().

    Args:
        flag_name: Nombre del flag a desactivar

    Returns:
        bool: True si se desactivó correctamente, False si no existe

    Ejemplo:
        >>> disable_flag('USE_NEW_DASHBOARD')
        >>> save_flags_to_file()  # Para persistir
    """
    if not hasattr(FeatureFlags, flag_name):
        if FeatureFlags.DEBUG_MODE:
            print(f"⚠️  Warning: Flag '{flag_name}' no existe")
        return False

    setattr(FeatureFlags, flag_name, False)
    return True


# ==========================================
# PERSISTENCIA (OPCIONAL)
# ==========================================

def get_flags_file_path() -> Path:
    """
    Obtiene la ruta del archivo de configuración de flags.

    Returns:
        Path: Ruta al archivo feature_flags.json
    """
    # Buscar el directorio raíz del proyecto
    current_dir = Path(__file__).parent.parent
    return current_dir / 'config' / 'feature_flags.json'


def save_flags_to_file(file_path: Optional[str] = None) -> bool:
    """
    Guarda el estado actual de los flags en un archivo JSON.

    Útil para persistir la configuración entre reinicios de la app.

    Args:
        file_path: Ruta del archivo (opcional, usa default si no se provee)

    Returns:
        bool: True si se guardó correctamente, False si hubo error

    Ejemplo:
        >>> enable_flag('USE_NEW_DASHBOARD')
        >>> save_flags_to_file()
    """
    try:
        path = Path(file_path) if file_path else get_flags_file_path()

        # Crear directorio si no existe
        path.parent.mkdir(parents=True, exist_ok=True)

        # Obtener todos los flags
        flags = get_all_flags()

        # Guardar con formato legible
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(flags, f, indent=2, ensure_ascii=False)

        if FeatureFlags.DEBUG_MODE:
            print(f"✅ Flags guardados en: {path}")

        return True

    except Exception as e:
        if FeatureFlags.DEBUG_MODE:
            print(f"❌ Error guardando flags: {e}")
        return False


def load_flags_from_file(file_path: Optional[str] = None) -> bool:
    """
    Carga el estado de los flags desde un archivo JSON.

    Si el archivo no existe, mantiene los valores por defecto.

    Args:
        file_path: Ruta del archivo (opcional, usa default si no se provee)

    Returns:
        bool: True si se cargó correctamente, False si hubo error o no existe

    Ejemplo:
        >>> load_flags_from_file()
        >>> if is_enabled('USE_NEW_DASHBOARD'):
        ...     print("Dashboard v2 activo")
    """
    try:
        path = Path(file_path) if file_path else get_flags_file_path()

        # Si no existe el archivo, no hacer nada (usar defaults)
        if not path.exists():
            if FeatureFlags.DEBUG_MODE:
                print(f"ℹ️  Archivo de flags no existe: {path}")
            return False

        # Cargar flags del archivo
        with open(path, 'r', encoding='utf-8') as f:
            saved_flags = json.load(f)

        # Aplicar cada flag
        for flag_name, value in saved_flags.items():
            if hasattr(FeatureFlags, flag_name):
                setattr(FeatureFlags, flag_name, value)

        if FeatureFlags.DEBUG_MODE:
            print(f"✅ Flags cargados desde: {path}")
            print(f"   Flags activos: {len(get_active_flags())}/{len(saved_flags)}")

        return True

    except Exception as e:
        if FeatureFlags.DEBUG_MODE:
            print(f"❌ Error cargando flags: {e}")
        return False


def reset_all_flags() -> None:
    """
    Reinicia todos los flags a False (estado por defecto).

    Útil para rollback completo en caso de problemas.

    Ejemplo:
        >>> reset_all_flags()
        >>> save_flags_to_file()  # Para persistir el reset
    """
    for attr in dir(FeatureFlags):
        if attr.isupper() and not attr.startswith('_'):
            setattr(FeatureFlags, attr, False)

    if FeatureFlags.DEBUG_MODE:
        print("🔄 Todos los flags reseteados a False")


# ==========================================
# HELPERS PARA STREAMLIT
# ==========================================

def render_flag_status_widget():
    """
    Renderiza un widget en Streamlit mostrando el estado de los flags.

    Solo se muestra si SHOW_FLAG_STATUS está activo.

    Ejemplo:
        >>> import streamlit as st
        >>> from utils.feature_flags import render_flag_status_widget
        >>> render_flag_status_widget()
    """
    if not is_enabled('SHOW_FLAG_STATUS'):
        return

    try:
        import streamlit as st

        with st.expander("🚩 Feature Flags Status", expanded=False):
            phases = get_flags_by_phase()

            for phase_name, flags in phases.items():
                st.markdown(f"**{phase_name}**")

                for flag_name, is_active in flags.items():
                    icon = "✅" if is_active else "⬜"
                    st.markdown(f"{icon} `{flag_name}`")

                st.markdown("---")

            # Resumen
            all_flags = get_all_flags()
            active_count = sum(all_flags.values())
            total_count = len(all_flags)

            st.info(f"**Total:** {active_count}/{total_count} flags activos")

    except ImportError:
        # Streamlit no disponible (testing, etc)
        pass


# ==========================================
# INICIALIZACIÓN
# ==========================================

# Intentar cargar flags desde archivo al importar el módulo
# Si no existe el archivo, se usan los valores por defecto
load_flags_from_file()


# ==========================================
# EXPORT
# ==========================================

__all__ = [
    'FeatureFlags',
    'is_enabled',
    'get_all_flags',
    'get_active_flags',
    'get_flags_by_phase',
    'enable_flag',
    'disable_flag',
    'save_flags_to_file',
    'load_flags_from_file',
    'reset_all_flags',
    'render_flag_status_widget',
]
