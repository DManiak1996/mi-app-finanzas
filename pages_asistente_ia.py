import streamlit as st
from utils.llm_service import LLMService
import time
from utils.feature_flags import is_enabled
from utils.components.page_layout import render_page_layout, page_header, page_section
from utils.design_tokens import Colors, Spacing, Typography, BorderRadius
from utils.environment import check_ollama_availability


def mostrar_asistente_ia_v2():
    """Asistente Financiero IA - Versión V2 con nuevo diseño."""

    def render_chat_content():
        # Verificar disponibilidad de Ollama
        ollama_available = check_ollama_availability()

        if not ollama_available:
            st.error("""
            ⚠️ **Ollama no está disponible**

            El Asistente IA requiere Ollama corriendo localmente.

            **Instrucciones:**
            1. Instala Ollama desde [ollama.ai](https://ollama.ai)
            2. Ejecuta `ollama pull llama3` para descargar el modelo
            3. Asegúrate de que Ollama esté corriendo en el puerto 11434
            """)
            return

        # Inicializar el servicio LLM
        if "llm_service" not in st.session_state:
            st.session_state.llm_service = LLMService(model_name="llama3")

        # Inicializar historial de chat
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Mensaje de bienvenida
        if not st.session_state.messages:
            with page_section(
                title="Bienvenido al Asistente Financiero IA",
                icon="👋",
                background=Colors.PREMIUM_BG_GRADIENT
            ):
                st.markdown(f"""
                Soy tu asistente financiero inteligente. Puedo ayudarte a:

                - 📊 Analizar tus gastos e ingresos
                - 💰 Consultar transacciones por categoría
                - 📈 Generar resúmenes mensuales
                - 🔍 Buscar patrones en tus finanzas

                **Ejemplo:** ¿Cuánto gasté en comida el mes pasado?
                """)

        # Mostrar mensajes previos
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                # Mensaje del usuario
                if message["role"] == "user":
                    st.markdown(message["content"])
                # Respuesta del asistente con estilo mejorado
                else:
                    st.markdown(f"""
                    <div style="
                        background: {Colors.PREMIUM_CARD_GRADIENT};
                        padding: {Spacing.LG};
                        border-radius: {BorderRadius.BASE};
                        border-left: 4px solid {Colors.PREMIUM_PRIMARY_START};
                    ">
                        {message["content"]}
                    </div>
                    """, unsafe_allow_html=True)

        # Input del usuario
        if prompt := st.chat_input("Pregunta sobre tus finanzas (ej: ¿Cuánto gasté en comida el mes pasado?)"):
            # Mostrar mensaje del usuario
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # Respuesta del asistente
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                message_placeholder.markdown("Pensando... 🧠")

                try:
                    llm = st.session_state.llm_service

                    # 1. Generar SQL
                    with st.status("Analizando tu pregunta...", expanded=False) as status:
                        st.write("Generando consulta SQL...")
                        sql_query = llm.get_sql_from_question(prompt)

                        if not sql_query:
                            status.update(label="Error generando SQL", state="error")
                            response_text = "Lo siento, no pude entender cómo traducir tu pregunta a una consulta de base de datos."
                        else:
                            st.write(f"SQL Generado: `{sql_query}`")

                            # 2. Ejecutar SQL
                            st.write("Consultando base de datos...")
                            df, error = llm.execute_sql(sql_query)

                            if error:
                                status.update(label="Error en consulta", state="error")
                                response_text = f"Hubo un error al ejecutar la consulta: {error}"
                            else:
                                # 3. Generar respuesta natural
                                st.write("Generando respuesta...")
                                response_text = llm.generate_natural_response(prompt, sql_query, df)
                                status.update(label="¡Listo!", state="complete")

                    # Mostrar respuesta con estilo
                    message_placeholder.markdown(f"""
                    <div style="
                        background: {Colors.PREMIUM_CARD_GRADIENT};
                        padding: {Spacing.LG};
                        border-radius: {BorderRadius.BASE};
                        border-left: 4px solid {Colors.PREMIUM_PRIMARY_START};
                    ">
                        {response_text}
                    </div>
                    """, unsafe_allow_html=True)

                    st.session_state.messages.append({"role": "assistant", "content": response_text})

                except Exception as e:
                    error_msg = f"Ocurrió un error inesperado: {e}"
                    message_placeholder.markdown(f"""
                    <div style="
                        background: {Colors.ERROR_ULTRA_LIGHT};
                        padding: {Spacing.LG};
                        border-radius: {BorderRadius.BASE};
                        border-left: 4px solid {Colors.ERROR};
                    ">
                        ⚠️ {error_msg}
                    </div>
                    """, unsafe_allow_html=True)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})

        # Botón para limpiar historial
        if st.session_state.messages:
            st.markdown(f"<div style='height: {Spacing.LG};'></div>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns([1, 1, 2])
            with col1:
                if st.button("🗑️ Limpiar Chat", use_container_width=True):
                    st.session_state.messages = []
                    st.rerun()

    # Renderizar con el layout
    render_page_layout(
        content_fn=render_chat_content,
        header={
            "title": "Asistente Financiero IA",
            "description": "Pregunta sobre tus finanzas y obtén respuestas inteligentes",
            "icon": "🤖"
        },
        max_width="1000px",
        background=Colors.PREMIUM_BG_GRADIENT
    )


def mostrar_asistente_ia():
    """Asistente Financiero IA."""

    # Feature flag para usar la versión v2
    if is_enabled('USE_NEW_ASISTENTE_IA'):
        return mostrar_asistente_ia_v2()

    # === VERSIÓN LEGACY (V1) ===
    st.title("🤖 Asistente Financiero IA")

    # Inicializar el servicio LLM
    if "llm_service" not in st.session_state:
        # Por defecto usamos llama3, pero podría ser configurable
        st.session_state.llm_service = LLMService(model_name="llama3")

    # Inicializar historial de chat
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Mostrar mensajes previos
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Input del usuario
    if prompt := st.chat_input("Pregunta sobre tus finanzas (ej: ¿Cuánto gasté en comida el mes pasado?)"):
        # Mostrar mensaje del usuario
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Respuesta del asistente
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            message_placeholder.markdown("Pensando... 🧠")
            
            try:
                llm = st.session_state.llm_service
                
                # 1. Generar SQL
                with st.status("Analizando tu pregunta...", expanded=False) as status:
                    st.write("Generando consulta SQL...")
                    sql_query = llm.get_sql_from_question(prompt)
                    
                    if not sql_query:
                        status.update(label="Error generando SQL", state="error")
                        response_text = "Lo siento, no pude entender cómo traducir tu pregunta a una consulta de base de datos."
                    else:
                        st.write(f"SQL Generado: `{sql_query}`")
                        
                        # 2. Ejecutar SQL
                        st.write("Consultando base de datos...")
                        df, error = llm.execute_sql(sql_query)
                        
                        if error:
                            status.update(label="Error en consulta", state="error")
                            response_text = f"Hubo un error al ejecutar la consulta: {error}"
                        else:
                            # 3. Generar respuesta natural
                            st.write("Generando respuesta...")
                            response_text = llm.generate_natural_response(prompt, sql_query, df)
                            status.update(label="¡Listo!", state="complete")
                
                message_placeholder.markdown(response_text)
                st.session_state.messages.append({"role": "assistant", "content": response_text})
                
            except Exception as e:
                error_msg = f"Ocurrió un error inesperado: {e}"
                message_placeholder.markdown(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
