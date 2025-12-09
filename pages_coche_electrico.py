# pages_coche_electrico.py
# Páginas y funciones para el módulo de Coche Eléctrico

import streamlit as st
import datetime
import pandas as pd
import plotly.graph_objects as go
from database import db_manager
from utils import coche_electrico
from utils.plotly_theme import apply_theme_to_fig, create_themed_pie_chart, create_themed_bar_chart, CHART_COLORS_FINANCE
from utils.feature_flags import is_enabled
from utils.components.page_layout import render_dashboard_layout, page_section, page_divider
from utils.components.chart_container import render_chart_container, render_chart_half
from utils.components.grid_system import render_metric_grid
from utils.components.data_table import render_data_table
from utils.design_tokens import Colors, Spacing, Typography


def mostrar_coche_electrico():
    """Página principal del Coche Eléctrico con sub-pestañas."""
    st.title("🔌 Coche Eléctrico - VW ID.3 Pro S")

    # Sub-pestañas
    tab1, tab2, tab3 = st.tabs(["⚡ Registrar Recarga", "💡 Registrar Factura Luz", "📊 Estadísticas"])

    with tab1:
        mostrar_registrar_recarga()

    with tab2:
        mostrar_registrar_factura_luz()

    with tab3:
        mostrar_estadisticas_coche()


def mostrar_registrar_recarga():
    """Formulario para registrar una nueva recarga del coche."""
    st.subheader("⚡ Nueva Recarga")

    # Obtener última recarga para pre-rellenar campos (Smart Defaults)
    ultima_recarga = db_manager.obtener_ultima_recarga()

    # Valores por defecto basados en la última recarga
    default_bateria_final = 80.0
    default_potencia = 4.6
    default_franja = "valle"
    default_consumo = 16.0

    if ultima_recarga:
        default_bateria_final = ultima_recarga.get('bateria_final', 80.0)
        default_potencia = 4.6  # La potencia no se guarda, usar default
        default_franja = ultima_recarga.get('franja_horaria', 'valle')
        default_consumo = ultima_recarga.get('consumo_medio', 16.0)

    with st.form("form_recarga", clear_on_submit=False):
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### 🔋 Batería")
            bateria_inicial = st.number_input(
                "% Batería inicial",
                min_value=0.0,
                max_value=100.0,
                value=20.0,
                step=1.0,
                help="Porcentaje de batería al iniciar la recarga"
            )

            bateria_final = st.number_input(
                "% Batería final",
                min_value=0.0,
                max_value=100.0,
                value=default_bateria_final,
                step=1.0,
                help="Porcentaje de batería al finalizar la recarga"
            )

            # Cálculo automático de kWh
            kwh_cargados = coche_electrico.calcular_kwh_cargados(bateria_inicial, bateria_final)
            st.metric("kWh cargados", f"{kwh_cargados:.2f} kWh", help="Calculado automáticamente")

        with col2:
            st.markdown("#### ⚡ Recarga")

            potencia_recarga = st.number_input(
                "Potencia de recarga (kW)",
                min_value=1.0,
                max_value=350.0,
                value=default_potencia,
                step=0.1,
                help="Potencia del cargador (4.6 kW casa, 7.4 kW wallbox, 11+ kW público)"
            )

            # Cálculo automático de tiempo
            horas_recarga = coche_electrico.calcular_tiempo_recarga(kwh_cargados, potencia_recarga)
            st.metric("Tiempo estimado", f"{horas_recarga:.1f} horas", help="Calculado automáticamente")

            # Índice por defecto según última franja
            franjas_opciones = ["valle", "llano", "punta"]
            indice_franja = franjas_opciones.index(default_franja) if default_franja in franjas_opciones else 0

            franja_horaria = st.selectbox(
                "Franja horaria",
                options=franjas_opciones,
                index=indice_franja,
                help="Valle: noche/madrugada (más barata)"
            )

        st.markdown("---")

        col3, col4 = st.columns(2)

        with col3:
            st.markdown("#### 🚗 Conducción")
            fecha_recarga = st.date_input(
                "Fecha de recarga",
                value=datetime.date.today()
            )

            km_recorridos = st.number_input(
                "Km recorridos con la batería anterior",
                min_value=0.0,
                value=0.0,
                step=1.0,
                help="Km que has conducido desde la última recarga hasta esta. Se asignarán a la recarga ANTERIOR (la batería que acabas de gastar)."
            )

            consumo_medio = st.number_input(
                "Consumo medio (kWh/100km)",
                min_value=0.0,
                value=default_consumo,
                step=0.1,
                help="Consumo mostrado en el ordenador de a bordo"
            )

        with col4:
            st.markdown("#### 💰 Coste Calculado")

            # Calcular coste completo
            costes = coche_electrico.calcular_coste_recarga(
                kwh_cargados,
                franja_horaria,
                horas_recarga
            )

            st.metric("Energía", f"{costes['coste_energia']:.2f} €")
            st.metric("Costes fijos", f"{costes['coste_potencia'] + costes['coste_alquiler'] + costes['coste_bono'] + costes['coste_servicios']:.2f} €")
            st.metric("Impuestos", f"{costes['impuesto_electricidad'] + costes['iva']:.2f} €")
            st.metric("💵 TOTAL", f"{costes['coste_total']:.2f} €",
                     delta=None,
                     help="Coste total de esta recarga")

        st.markdown("---")

        notas = st.text_input(
            "Notas (opcional)",
            placeholder="Ej: Recarga en casa, Recarga rápida en autopista...",
            help="Información adicional sobre esta recarga"
        )

        # Validación previa visual
        validacion_ok = True
        if bateria_final <= bateria_inicial:
            st.warning("⚠️ La batería final debe ser mayor que la inicial")
            validacion_ok = False
        elif kwh_cargados <= 0:
            st.warning("⚠️ Los kWh deben ser positivos")
            validacion_ok = False

        # Botón de submit
        submitted = st.form_submit_button("💾 Guardar Recarga", type="primary", use_container_width=True, disabled=not validacion_ok)

        if submitted:
            # Validaciones (por si acaso)
            if bateria_final <= bateria_inicial:
                st.error("❌ La batería final debe ser mayor que la inicial")
            elif kwh_cargados <= 0:
                st.error("❌ Los kWh cargados deben ser positivos")
            else:
                # Si hay km recorridos, asignarlos a la recarga ANTERIOR
                if km_recorridos > 0 and ultima_recarga:
                    # Actualizar la última recarga con los km recorridos
                    db_manager.actualizar_recarga_coche(
                        ultima_recarga['id'],
                        km_recorridos=km_recorridos
                    )
                
                # Guardar la nueva recarga en BD (siempre con km = 0)
                mes = fecha_recarga.month
                año = fecha_recarga.year

                resultado = db_manager.insertar_recarga_coche(
                    fecha_recarga=fecha_recarga,
                    bateria_inicial=bateria_inicial,
                    bateria_final=bateria_final,
                    kwh_cargados=kwh_cargados,
                    km_recorridos=0,  # La nueva recarga empieza sin km
                    consumo_medio=consumo_medio,
                    franja_horaria=franja_horaria,
                    tarifa_kwh=costes['tarifa_kwh'],
                    coste_energia=costes['coste_energia'],
                    coste_potencia=costes['coste_potencia'],
                    coste_alquiler=costes['coste_alquiler'],
                    coste_bono=costes['coste_bono'],
                    coste_servicios=costes['coste_servicios'],
                    impuesto_electricidad=costes['impuesto_electricidad'],
                    iva=costes['iva'],
                    coste_total=costes['coste_total'],
                    mes=mes,
                    año=año,
                    notas=notas
                )

                if resultado:
                    if km_recorridos > 0 and ultima_recarga:
                        st.success(f"✅ Recarga guardada - Total: {costes['coste_total']:.2f} € | {km_recorridos:.0f} km asignados a la recarga anterior")
                    else:
                        st.success(f"✅ Recarga guardada correctamente - Total: {costes['coste_total']:.2f} €")
                    st.balloons()

                    # Mostrar análisis de la recarga
                    if ultima_recarga:
                        dias_desde_ultima = coche_electrico.calcular_dias_desde_ultima_recarga(
                            fecha_recarga,
                            datetime.datetime.fromisoformat(ultima_recarga['fecha_recarga']).date()
                        )
                        st.info(f"📅 Días desde última recarga: {dias_desde_ultima}")

                        if km_recorridos > 0 and dias_desde_ultima > 0:
                            km_diarios = coche_electrico.calcular_km_diarios(km_recorridos, dias_desde_ultima)
                            st.info(f"🚗 Promedio: {km_diarios:.1f} km/día")
                else:
                    st.error("❌ Error al guardar la recarga. Inténtalo de nuevo.")

    # Mostrar últimas 10 recargas con opción de editar/eliminar
    st.markdown("---")
    st.subheader("📝 Últimas Recargas")

    recargas_recientes = db_manager.obtener_recargas(limit=10)

    if recargas_recientes:
        # Preparar DataFrame con todos los campos necesarios
        df_recargas = pd.DataFrame(recargas_recientes)

        # Mostrar tabla editable
        columnas_display = ['id', 'fecha_recarga', 'bateria_inicial', 'bateria_final', 'kwh_cargados',
                           'km_recorridos', 'consumo_medio', 'franja_horaria', 'coste_total']

        df_editable = df_recargas[columnas_display].copy()
        # Convertir fecha a datetime para poder usar DateColumn (formato ISO8601)
        df_editable['fecha_recarga'] = pd.to_datetime(df_editable['fecha_recarga'], format='ISO8601')

        # Renombrar columnas para mejor visualización
        df_editable = df_editable.rename(columns={
            'id': 'ID',
            'fecha_recarga': 'Fecha',
            'bateria_inicial': 'Bat. Inicial %',
            'bateria_final': 'Bat. Final %',
            'kwh_cargados': 'kWh',
            'km_recorridos': 'Km',
            'consumo_medio': 'kWh/100km',
            'franja_horaria': 'Franja',
            'coste_total': 'Coste €'
        })

        # Editor de datos con configuración de columnas
        edited_df = st.data_editor(
            df_editable,
            use_container_width=True,
            hide_index=True,
            num_rows="fixed",
            disabled=['ID', 'kWh', 'Coste €'],  # Campos calculados no editables
            column_config={
                "ID": st.column_config.TextColumn("ID", width="small", disabled=True),
                "Fecha": st.column_config.DateColumn("Fecha", format="DD/MM/YYYY"),
                "Bat. Inicial %": st.column_config.NumberColumn("Bat. Inicial %", min_value=0, max_value=100, step=1),
                "Bat. Final %": st.column_config.NumberColumn("Bat. Final %", min_value=0, max_value=100, step=1),
                "kWh": st.column_config.NumberColumn("kWh", format="%.2f", disabled=True),
                "Km": st.column_config.NumberColumn("Km", min_value=0, step=1),
                "kWh/100km": st.column_config.NumberColumn("kWh/100km", min_value=0, step=0.1, format="%.1f"),
                "Franja": st.column_config.SelectboxColumn("Franja", options=["valle", "llano", "punta"]),
                "Coste €": st.column_config.NumberColumn("Coste €", format="%.2f €", disabled=True)
            }
        )

        # Botones de acción
        col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 4])

        with col_btn1:
            if st.button("💾 Guardar Cambios", type="primary", use_container_width=True):
                # Comparar DataFrames para detectar cambios
                cambios_detectados = False

                for idx in range(len(df_editable)):
                    id_recarga = edited_df.iloc[idx]['ID']

                    # Verificar si hay cambios en esta fila
                    for col_orig, col_edit in [
                        ('Fecha', 'Fecha'),
                        ('Bat. Inicial %', 'Bat. Inicial %'),
                        ('Bat. Final %', 'Bat. Final %'),
                        ('Km', 'Km'),
                        ('kWh/100km', 'kWh/100km'),
                        ('Franja', 'Franja')
                    ]:
                        if df_editable.iloc[idx][col_orig] != edited_df.iloc[idx][col_edit]:
                            cambios_detectados = True

                            # Recalcular kWh y costes si cambió batería o franja
                            bat_inicial = edited_df.iloc[idx]['Bat. Inicial %']
                            bat_final = edited_df.iloc[idx]['Bat. Final %']
                            kwh = coche_electrico.calcular_kwh_cargados(bat_inicial, bat_final)

                            # Obtener potencia de recarga de la BD (o usar default 4.6)
                            recarga_original = db_manager.obtener_recarga_por_id(id_recarga)
                            potencia = 4.6  # Default
                            horas = coche_electrico.calcular_tiempo_recarga(kwh, potencia)

                            franja = edited_df.iloc[idx]['Franja']
                            costes = coche_electrico.calcular_coste_recarga(kwh, franja, horas)

                            # Actualizar en BD
                            campos_actualizar = {
                                'fecha_recarga': edited_df.iloc[idx]['Fecha'],
                                'bateria_inicial': bat_inicial,
                                'bateria_final': bat_final,
                                'kwh_cargados': kwh,
                                'km_recorridos': edited_df.iloc[idx]['Km'],
                                'consumo_medio': edited_df.iloc[idx]['kWh/100km'],
                                'franja_horaria': franja,
                                'tarifa_kwh': costes['tarifa_kwh'],
                                'coste_energia': costes['coste_energia'],
                                'coste_potencia': costes['coste_potencia'],
                                'coste_alquiler': costes['coste_alquiler'],
                                'coste_bono': costes['coste_bono'],
                                'coste_servicios': costes['coste_servicios'],
                                'impuesto_electricidad': costes['impuesto_electricidad'],
                                'iva': costes['iva'],
                                'coste_total': costes['coste_total']
                            }

                            if db_manager.actualizar_recarga_coche(id_recarga, **campos_actualizar):
                                st.success(f"✅ Recarga {id_recarga[:8]}... actualizada")
                            else:
                                st.error(f"❌ Error al actualizar recarga {id_recarga[:8]}...")
                            break

                if cambios_detectados:
                    st.rerun()
                else:
                    st.info("ℹ️ No se detectaron cambios")

        with col_btn2:
            # Selector de recarga a eliminar
            opciones_eliminar = [f"{r['fecha_recarga'][:10]} - {r['kwh_cargados']:.1f} kWh" for r in recargas_recientes]
            recarga_a_eliminar = st.selectbox(
                "Eliminar recarga:",
                options=range(len(recargas_recientes)),
                format_func=lambda x: opciones_eliminar[x],
                label_visibility="collapsed"
            )

        with col_btn3:
            # Sistema de confirmación con session_state
            if 'confirmar_eliminacion' not in st.session_state:
                st.session_state.confirmar_eliminacion = False

            if not st.session_state.confirmar_eliminacion:
                if st.button("🗑️ Eliminar", type="secondary", use_container_width=False, key="btn_eliminar_inicial"):
                    st.session_state.confirmar_eliminacion = True
                    st.rerun()
            else:
                # Mostrar confirmación
                recarga_seleccionada = recargas_recientes[recarga_a_eliminar]
                st.warning(f"⚠️ ¿Eliminar recarga del {recarga_seleccionada['fecha_recarga'][:10]}? ({recarga_seleccionada['kwh_cargados']:.1f} kWh - {recarga_seleccionada['coste_total']:.2f}€)")

                col_conf1, col_conf2 = st.columns(2)
                with col_conf1:
                    if st.button("❌ Cancelar", use_container_width=True, key="btn_cancelar_elim"):
                        st.session_state.confirmar_eliminacion = False
                        st.rerun()

                with col_conf2:
                    if st.button("✅ Sí, eliminar", type="primary", use_container_width=True, key="btn_confirmar_elim"):
                        id_eliminar = recarga_seleccionada['id']
                        if db_manager.eliminar_recarga_coche(id_eliminar):
                            st.success("✅ Recarga eliminada correctamente")
                            st.session_state.confirmar_eliminacion = False
                            st.rerun()
                        else:
                            st.error("❌ Error al eliminar la recarga")
                            st.session_state.confirmar_eliminacion = False

        # Sección para PAGAR recargas pendientes del mes
        st.markdown("---")
        st.subheader("💰 Pagar Recargas del Mes")

        col_pago1, col_pago2 = st.columns(2)

        with col_pago1:
            # Selector de mes y año
            mes_pagar = st.selectbox(
                "Mes a pagar",
                options=list(range(1, 13)),
                format_func=lambda x: datetime.date(2000, x, 1).strftime("%B"),
                index=datetime.date.today().month - 1
            )
            año_pagar = st.number_input(
                "Año",
                min_value=2020,
                max_value=2030,
                value=datetime.date.today().year,
                step=1
            )

        with col_pago2:
            # Obtener recargas pendientes del mes seleccionado
            recargas_pendientes = db_manager.obtener_recargas_pendientes(mes=mes_pagar, año=año_pagar)

            if recargas_pendientes:
                total_pendiente = sum(r['coste_total'] for r in recargas_pendientes)
                st.metric("Recargas pendientes", len(recargas_pendientes))
                st.metric("Total a pagar", f"{total_pendiente:.2f} €")

                # Fecha de pago
                fecha_pago = st.date_input(
                    "Fecha del pago (ej: fecha del bizum)",
                    value=datetime.date.today()
                )

                # Botón para pagar
                if st.button("✅ Marcar como Pagadas y Crear Transacción", type="primary", use_container_width=True):
                    resultado = db_manager.pagar_recargas_mes(
                        mes=mes_pagar,
                        año=año_pagar,
                        fecha_pago=fecha_pago
                    )

                    if resultado:
                        id_transaccion, total, num_recargas = resultado
                        st.success(f"✅ {num_recargas} recargas pagadas por {total:.2f}€")
                        st.info(f"💳 Transacción creada con concepto 'Recarga coche'")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error("❌ Error al procesar el pago")
            else:
                st.info(f"ℹ️ No hay recargas pendientes para {datetime.date(2000, mes_pagar, 1).strftime('%B')} {año_pagar}")
    else:
        st.info("No hay recargas registradas aún.")


def mostrar_registrar_factura_luz():
    """Formulario para registrar la factura mensual de electricidad."""
    st.subheader("💡 Nueva Factura de Electricidad")

    with st.form("form_factura", clear_on_submit=False):
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### 📅 Período")

            mes = st.selectbox(
                "Mes",
                options=list(range(1, 13)),
                format_func=lambda x: datetime.date(2000, x, 1).strftime('%B'),
                index=datetime.date.today().month - 1
            )

            año = st.number_input(
                "Año",
                min_value=2020,
                max_value=2030,
                value=datetime.date.today().year,
                step=1
            )

            fecha_factura = st.date_input(
                "Fecha de la factura",
                value=datetime.date.today()
            )

        with col2:
            st.markdown("#### ⚡ Consumos de la RED (kWh)")
            st.caption("Solo lo que se factura de la red (sin autoconsumo)")

            consumo_punta = st.number_input(
                "Punta (de la red)",
                min_value=0.0,
                value=106.02,
                step=0.01,
                help="kWh consumidos de la RED en franja punta (facturados)"
            )

            consumo_llano = st.number_input(
                "Llano (de la red)",
                min_value=0.0,
                value=126.82,
                step=0.01,
                help="kWh consumidos de la RED en franja llano (facturados)"
            )

            consumo_valle = st.number_input(
                "Valle (de la red)",
                min_value=0.0,
                value=368.58,
                step=0.01,
                help="kWh consumidos de la RED en franja valle (facturados)"
            )

        st.markdown("---")
        st.markdown("#### 💰 Costes Fijos Mensuales (€)")

        col3, col4, col5 = st.columns(3)

        with col3:
            potencia = st.number_input(
                "Potencia",
                min_value=0.0,
                value=13.71,
                step=0.01
            )

            alquiler = st.number_input(
                "Alquiler contador",
                min_value=0.0,
                value=0.80,
                step=0.01
            )

        with col4:
            bono_social = st.number_input(
                "Bono social",
                min_value=0.0,
                value=0.40,
                step=0.01,
                help="Financiación bono social fijo (cargos normativos)"
            )

            alquiler = st.number_input(
                "Alquiler contador",
                min_value=0.0,
                value=0.83,
                step=0.01,
                help="Alquiler de equipos de medida (servicios y otros)"
            )

        with col5:
            st.markdown("#### ☀️ Paneles Solares (Smart Solar)")

            energia_generada = st.number_input(
                "Energía generada (kWh)",
                value=0.0,
                step=0.01,
                help="kWh generados por los paneles solares durante el periodo"
            )

            energia_exportada = st.number_input(
                "Energía exportada (kWh)",
                value=0.0,
                step=0.01,
                help="kWh exportados a la red (excedentes no consumidos)"
            )

            precio_compensacion = st.number_input(
                "Precio compensación (€/kWh)",
                value=0.07,
                step=0.001,
                help="Precio que paga Iberdrola por excedentes exportados",
                format="%.3f"
            )

        notas_factura = st.text_area(
            "Notas (opcional)",
            placeholder="Información adicional sobre esta factura..."
        )

        submitted = st.form_submit_button("💾 Guardar Factura", type="primary", use_container_width=True)

        if submitted:
            # Tarifas fijas
            tarifa_punta = 0.184576
            tarifa_llano = 0.131892
            tarifa_valle = 0.099904

            resultado = db_manager.insertar_factura_electricidad(
                mes=mes,
                año=año,
                fecha_factura=fecha_factura,
                consumo_punta_kwh=consumo_punta,
                consumo_llano_kwh=consumo_llano,
                consumo_valle_kwh=consumo_valle,
                tarifa_punta=tarifa_punta,
                tarifa_llano=tarifa_llano,
                tarifa_valle=tarifa_valle,
                potencia=potencia,
                alquiler_contador=alquiler,
                bono_social=bono_social,
                servicios=0.0,  # Ya no se usa, solo alquiler_contador
                energia_generada=energia_generada,
                energia_exportada=energia_exportada,
                precio_compensacion=precio_compensacion,
                excedentes_kwh=0,
                excedentes_compensacion=0,
                notas=notas_factura
            )

            if resultado:
                # Obtener la factura recién insertada para mostrar resultados
                factura = db_manager.obtener_factura_por_mes(mes, año)

                st.success(f"✅ Factura guardada correctamente")
                st.balloons()

                # Mostrar resumen
                col_r1, col_r2, col_r3 = st.columns(3)

                with col_r1:
                    st.metric("Total Factura", f"{factura['total_factura']:.2f} €")

                with col_r2:
                    st.metric("Consumo Total", f"{factura['consumo_total_kwh']:.1f} kWh")

                with col_r3:
                    if factura['porcentaje_coche'] > 0:
                        st.metric("Participación Coche", f"{factura['porcentaje_coche']:.1f} %",
                                 delta=f"{factura['coste_coche_mes']:.2f} €")

                # Mostrar desglose
                with st.expander("📋 Ver Desglose Completo"):
                    st.write("**Energía por franja:**")
                    st.write(f"- Punta: {consumo_punta} kWh × {tarifa_punta} €/kWh = {consumo_punta * tarifa_punta:.2f} €")
                    st.write(f"- Llano: {consumo_llano} kWh × {tarifa_llano} €/kWh = {consumo_llano * tarifa_llano:.2f} €")
                    st.write(f"- Valle: {consumo_valle} kWh × {tarifa_valle} €/kWh = {consumo_valle * tarifa_valle:.2f} €")
                    st.write(f"**Coste energía total: {factura['coste_energia']:.2f} €**")
                    st.write("")
                    st.write(f"**Costes fijos:** {potencia + alquiler + bono_social + servicios:.2f} €")
                    st.write(f"**Impuesto electricidad:** {factura['impuesto_electricidad']:.2f} €")
                    st.write(f"**IVA:** {factura['iva']:.2f} €")
                    st.write("")
                    st.write(f"### TOTAL: {factura['total_factura']:.2f} €")
            else:
                st.error("❌ Error al guardar la factura. Puede que ya exista una factura para este mes/año.")

    # Mostrar últimas facturas
    st.markdown("---")
    st.subheader("📝 Últimas Facturas")

    facturas_recientes = db_manager.obtener_facturas_electricidad(limit=6)

    if facturas_recientes:
        df_facturas = pd.DataFrame(facturas_recientes)

        # Crear columna de periodo
        df_facturas['periodo'] = df_facturas.apply(
            lambda row: f"{datetime.date(2000, row['mes'], 1).strftime('%B')} {row['año']}",
            axis=1
        )

        columnas_mostrar = {
            'periodo': 'Período',
            'consumo_total_kwh': 'kWh Total',
            'kwh_coche_mes': 'kWh Coche',
            'porcentaje_coche': '% Coche',
            'total_factura': 'Total €'
        }

        df_display = df_facturas[list(columnas_mostrar.keys())].rename(columns=columnas_mostrar)
        df_display['Total €'] = df_display['Total €'].apply(lambda x: f"{x:.2f} €")
        df_display['% Coche'] = df_display['% Coche'].apply(lambda x: f"{x:.1f}%")

        st.dataframe(df_display, use_container_width=True, hide_index=True)
    else:
        st.info("No hay facturas registradas aún.")


def mostrar_estadisticas_coche_v2():
    """Dashboard con estadísticas y gráficos del coche eléctrico - Versión V2 con nuevo diseño."""

    def render_dashboard_content():
        # Selector de período
        col_sel1, col_sel2 = st.columns(2)

        with col_sel1:
            año_seleccionado = st.selectbox(
                "Año",
                options=list(range(datetime.date.today().year, 2019, -1)),
                index=0
            )

        with col_sel2:
            mes_seleccionado = st.selectbox(
                "Mes (para detalles)",
                options=list(range(1, 13)),
                format_func=lambda x: datetime.date(2000, x, 1).strftime('%B'),
                index=datetime.date.today().month - 1
            )

        # Obtener datos
        recargas_mes = db_manager.obtener_recargas(mes=mes_seleccionado, año=año_seleccionado)
        recargas_año = db_manager.obtener_recargas(año=año_seleccionado)

        if not recargas_mes and not recargas_año:
            st.warning("No hay datos de recargas para mostrar. Registra tu primera recarga para ver estadísticas.")
            return

        # === MÉTRICAS DEL MES ===
        if recargas_mes:
            stats_mes = coche_electrico.calcular_estadisticas_mes(recargas_mes, incluir_proyeccion=True, detectar_anomalias=True)

            with page_section(
                title=f"{datetime.date(2000, mes_seleccionado, 1).strftime('%B')} {año_seleccionado}",
                icon="📅"
            ):
                # Métricas principales
                metrics = [
                    {
                        "label": "Recargas",
                        "value": stats_mes['total_recargas'],
                        "help": "Número total de recargas en el mes"
                    },
                    {
                        "label": "kWh Totales",
                        "value": f"{stats_mes['kwh_totales']:.1f}",
                        "delta": f"~{stats_mes.get('proyeccion', {}).get('kwh_proyectados', 0):.1f} proyectados" if stats_mes.get('proyeccion', {}).get('kwh_proyectados') else None,
                        "help": "Energía total cargada"
                    },
                    {
                        "label": "Coste Total",
                        "value": f"{stats_mes['coste_total']:.2f} €",
                        "delta": f"~{stats_mes.get('proyeccion', {}).get('coste_proyectado', 0):.2f} € proyectados" if stats_mes.get('proyeccion', {}).get('coste_proyectado') else None,
                        "help": "Coste total de recargas"
                    },
                    {
                        "label": "Coste/km" if stats_mes['km_totales'] > 0 else "Coste/km (N/A)",
                        "value": f"{stats_mes['coste_por_km']:.4f} €" if stats_mes['km_totales'] > 0 else "N/A",
                        "help": "Coste por kilómetro recorrido"
                    },
                ]

                render_metric_grid(metrics, cols=4)

                # Métricas secundarias (solo si hay km)
                if stats_mes['km_totales'] > 0:
                    st.markdown(f"<div style='height: {Spacing.LG};'></div>", unsafe_allow_html=True)

                    metrics_km = [
                        {
                            "label": "Km Recorridos",
                            "value": f"{stats_mes['km_totales']:.0f}",
                            "delta": f"~{stats_mes.get('proyeccion', {}).get('km_proyectados', 0):.0f} proyectados" if stats_mes.get('proyeccion', {}).get('km_proyectados') else None,
                        },
                        {
                            "label": "Km/recarga",
                            "value": f"{stats_mes['km_promedio_por_recarga']:.0f}",
                        },
                        {
                            "label": "Consumo Medio",
                            "value": f"{stats_mes['consumo_medio']:.1f} kWh/100km",
                        },
                        {
                            "label": "Días entre recargas",
                            "value": f"{stats_mes['dias_promedio_entre_recargas']:.1f}",
                        },
                    ]

                    render_metric_grid(metrics_km, cols=4)

                # Anomalías
                if stats_mes.get('anomalias'):
                    anoms = stats_mes['anomalias']
                    if anoms:
                        st.warning("⚠️ Se detectaron recargas atípicas:")
                        for a in anoms:
                            st.caption(f"Recarga ID {a['recarga_id']} ({a['fecha']}): km/día {a['km_dia']:.1f} (desviación {a['desviacion_pct']:.0f}%)")

            # Comparativa gasolina
            if stats_mes['km_totales'] > 0:
                ahorro_vs_gasolina = coche_electrico.calcular_ahorro_vs_gasolina(
                    stats_mes['km_totales'],
                    stats_mes['coste_total']
                )

                with page_section(title="Comparativa con Gasolina", icon="💰"):
                    metrics_gasolina = [
                        {
                            "label": "Coste Gasolina",
                            "value": f"{ahorro_vs_gasolina['coste_gasolina']:.2f} €",
                        },
                        {
                            "label": "Ahorro Mensual",
                            "value": f"{ahorro_vs_gasolina['ahorro']:.2f} €",
                            "delta": f"-{ahorro_vs_gasolina['porcentaje_ahorro']:.1f}%",
                        },
                        {
                            "label": "Ahorro Anual Estimado",
                            "value": f"{ahorro_vs_gasolina['ahorro'] * 12:.2f} €",
                        },
                    ]

                    render_metric_grid(metrics_gasolina, cols=3)

        else:
            st.info(f"No hay recargas en {datetime.date(2000, mes_seleccionado, 1).strftime('%B')} {año_seleccionado}")

        # === GRÁFICOS DEL AÑO ===
        if recargas_año:
            page_divider(margin=Spacing.XXL)

            with page_section(
                title=f"Evolución Anual {año_seleccionado}",
                icon="📈"
            ):
                # Preparar datos
                df_año = pd.DataFrame(recargas_año)
                df_año['fecha_recarga'] = pd.to_datetime(df_año['fecha_recarga'], format='ISO8601')
                df_año = df_año.sort_values('fecha_recarga')

                # Gráficos lado a lado
                fig_kwh = go.Figure()
                fig_kwh.add_trace(go.Bar(
                    x=df_año['fecha_recarga'].dt.strftime('%d/%m'),
                    y=df_año['kwh_cargados'],
                    name='kWh',
                    marker_color=CHART_COLORS_FINANCE['balance'],
                    marker_line=dict(width=0)
                ))
                apply_theme_to_fig(fig_kwh, title=None, height=350, showlegend=False)

                fig_coste = go.Figure()
                fig_coste.add_trace(go.Bar(
                    x=df_año['fecha_recarga'].dt.strftime('%d/%m'),
                    y=df_año['coste_total'],
                    name='Coste €',
                    marker_color=CHART_COLORS_FINANCE['income'],
                    marker_line=dict(width=0),
                    hovertemplate='<b>%{x}</b><br>Coste: %{y:.2f} €<extra></extra>'
                ))
                apply_theme_to_fig(fig_coste, title=None, height=350, showlegend=False)

                render_chart_half([
                    {"fig": fig_kwh, "title": "kWh por Recarga"},
                    {"fig": fig_coste, "title": "Coste por Recarga"}
                ])

                # Gráfico de distribución por franja
                st.markdown(f"<div style='height: {Spacing.LG};'></div>", unsafe_allow_html=True)

                distribucion_franjas = df_año['franja_horaria'].value_counts()
                df_franjas = pd.DataFrame({
                    'franja': distribucion_franjas.index,
                    'recargas': distribucion_franjas.values
                })

                fig_franjas = create_themed_pie_chart(
                    df_franjas,
                    names='franja',
                    values='recargas',
                    title='Distribución por Franja Horaria',
                    hole=0.4
                )

                render_chart_container(
                    fig_franjas,
                    title="Distribución por Franja Horaria",
                    height=450
                )

                # Tabla resumen por mes
                st.markdown(f"<div style='height: {Spacing.XL};'></div>", unsafe_allow_html=True)

                df_año['mes_nombre'] = df_año['fecha_recarga'].dt.strftime('%B')

                resumen_mes = df_año.groupby('mes_nombre').agg({
                    'kwh_cargados': 'sum',
                    'km_recorridos': 'sum',
                    'coste_total': 'sum'
                }).round(2)

                def calcular_consumo_mes(grupo):
                    km_total = grupo['km_recorridos'].sum()
                    kwh_total = grupo['kwh_cargados'].sum()
                    if km_total > 0:
                        return round((kwh_total / km_total) * 100, 1)
                    else:
                        consumos = grupo['consumo_medio'][grupo['consumo_medio'] > 0]
                        return round(consumos.mean(), 1) if len(consumos) > 0 else 0

                resumen_consumo = df_año.groupby('mes_nombre').apply(calcular_consumo_mes)
                resumen_mes['consumo_medio'] = resumen_consumo

                resumen_mes.columns = ['kWh Total', 'Km Total', 'Coste Total €', 'Consumo Medio (kWh/100km)']

                render_data_table(
                    resumen_mes.reset_index().rename(columns={'mes_nombre': 'Mes'}),
                    title="Resumen Mensual",
                    searchable=False,
                    exportable=True,
                    export_filename=f"resumen_coche_{año_seleccionado}",
                    currency_columns=['Coste Total €'],
                    number_columns=['kWh Total', 'Km Total', 'Consumo Medio (kWh/100km)']
                )

        else:
            st.info(f"No hay recargas en {año_seleccionado}")

    # Renderizar con el layout de dashboard
    render_dashboard_layout(
        content_fn=render_dashboard_content,
        title="Coche Eléctrico - VW ID.3 Pro S",
        description="Estadísticas y análisis de consumo y costes",
        icon="🔌",
        show_period_selector=False
    )


def mostrar_estadisticas_coche():
    """Dashboard con estadísticas y gráficos del coche eléctrico."""

    # Feature flag para usar la versión v2
    if is_enabled('USE_NEW_COCHE_ELECTRICO'):
        return mostrar_estadisticas_coche_v2()

    # === VERSIÓN LEGACY (V1) ===
    st.subheader("📊 Estadísticas del Coche Eléctrico")

    # Selector de período
    col_sel1, col_sel2 = st.columns(2)

    with col_sel1:
        año_seleccionado = st.selectbox(
            "Año",
            options=list(range(datetime.date.today().year, 2019, -1)),
            index=0
        )

    with col_sel2:
        mes_seleccionado = st.selectbox(
            "Mes (para detalles)",
            options=list(range(1, 13)),
            format_func=lambda x: datetime.date(2000, x, 1).strftime('%B'),
            index=datetime.date.today().month - 1
        )

    # Obtener datos
    recargas_mes = db_manager.obtener_recargas(mes=mes_seleccionado, año=año_seleccionado)
    recargas_año = db_manager.obtener_recargas(año=año_seleccionado)

    if not recargas_mes and not recargas_año:
        st.warning("No hay datos de recargas para mostrar. Registra tu primera recarga para ver estadísticas.")
        return

    # Estadísticas del mes
    if recargas_mes:
        stats_mes = coche_electrico.calcular_estadisticas_mes(recargas_mes, incluir_proyeccion=True, detectar_anomalias=True)

        st.markdown(f"### 📅 {datetime.date(2000, mes_seleccionado, 1).strftime('%B')} {año_seleccionado}")

        # Layout responsive (2x2 con 2 métricas por columna)
        col1, col2 = st.columns(2)

        # Obtener proyección si existe
        proj = stats_mes.get('proyeccion', {})

        with col1:
            st.metric("Recargas", stats_mes['total_recargas'])
            
            # kWh con proyección
            if proj and proj.get('kwh_proyectados'):
                st.metric("kWh Totales", f"{stats_mes['kwh_totales']:.1f}",
                         delta=f"~{proj['kwh_proyectados']:.1f} proyectados",
                         help="Proyección para fin de mes")
            else:
                st.metric("kWh Totales", f"{stats_mes['kwh_totales']:.1f}")
            
            # Coste con proyección
            if proj and proj.get('coste_proyectado'):
                st.metric("Coste Total", f"{stats_mes['coste_total']:.2f} €",
                         delta=f"~{proj['coste_proyectado']:.2f} € proyectados",
                         help="Proyección para fin de mes")
            else:
                st.metric("Coste Total", f"{stats_mes['coste_total']:.2f} €")

            # Mostrar coste/km solo si hay km registrados
            if stats_mes['km_totales'] > 0:
                st.metric("Coste/km", f"{stats_mes['coste_por_km']:.4f} €")
            else:
                st.metric("Coste/km", "N/A", help="Registra km para calcular el coste por kilómetro")

        with col2:
            # Mostrar km solo si hay registros de km
            if stats_mes['km_totales'] > 0:
                # Km con proyección
                if proj and proj.get('km_proyectados'):
                    st.metric("Km Recorridos", f"{stats_mes['km_totales']:.0f}",
                             delta=f"~{proj['km_proyectados']:.0f} proyectados",
                             help="Proyección para fin de mes")
                else:
                    st.metric("Km Recorridos", f"{stats_mes['km_totales']:.0f}")
                st.metric("Km/recarga", f"{stats_mes['km_promedio_por_recarga']:.0f}")
            else:
                st.metric("Km Recorridos", "No registrados", help="Opcional: Registra km desde la carga anterior")
                st.metric("Km/recarga", "N/A")

            st.metric("Consumo Medio", f"{stats_mes['consumo_medio']:.1f} kWh/100km")
            st.metric("Días entre recargas", f"{stats_mes['dias_promedio_entre_recargas']:.1f}")

            # Anomalías
            if stats_mes.get('anomalias'):
                anoms = stats_mes['anomalias']
                if anoms:
                    st.warning("⚠️ Se detectaron recargas atípicas:")
                    for a in anoms:
                        st.caption(f"Recarga ID {a['recarga_id']} ({a['fecha']}): km/día {a['km_dia']:.1f} (desviación {a['desviacion_pct']:.0f}%)")

        # Comparativa gasolina
        if stats_mes['km_totales'] > 0:
            ahorro_vs_gasolina = coche_electrico.calcular_ahorro_vs_gasolina(
                stats_mes['km_totales'],
                stats_mes['coste_total']
            )

            st.markdown("---")
            st.markdown("### 💰 Comparativa con Gasolina")

            col_g1, col_g2, col_g3 = st.columns(3)

            with col_g1:
                st.metric("Coste Gasolina", f"{ahorro_vs_gasolina['coste_gasolina']:.2f} €")

            with col_g2:
                st.metric("Ahorro Mensual", f"{ahorro_vs_gasolina['ahorro']:.2f} €",
                         delta=f"-{ahorro_vs_gasolina['porcentaje_ahorro']:.1f}%")

            with col_g3:
                ahorro_anual = ahorro_vs_gasolina['ahorro'] * 12
                st.metric("Ahorro Anual Estimado", f"{ahorro_anual:.2f} €")

    else:
        st.info(f"No hay recargas en {datetime.date(2000, mes_seleccionado, 1).strftime('%B')} {año_seleccionado}")

    # Gráficos del año
    if recargas_año:
        st.markdown("---")
        st.markdown(f"### 📈 Evolución Anual {año_seleccionado}")

        # Preparar datos para gráficos
        df_año = pd.DataFrame(recargas_año)
        df_año['fecha_recarga'] = pd.to_datetime(df_año['fecha_recarga'], format='ISO8601')
        df_año = df_año.sort_values('fecha_recarga')

        # Gráfico 1: Evolución kWh y Coste
        col_g1, col_g2 = st.columns(2)

        with col_g1:
            st.markdown("#### kWh por Recarga")
            fig_kwh = go.Figure()
            fig_kwh.add_trace(go.Bar(
                x=df_año['fecha_recarga'].dt.strftime('%d/%m'),
                y=df_año['kwh_cargados'],
                name='kWh',
                marker_color=CHART_COLORS_FINANCE['balance'],
                marker_line=dict(width=0)
            ))
            apply_theme_to_fig(fig_kwh, title=None, height=300, showlegend=False)
            st.plotly_chart(fig_kwh, use_container_width=True)

        with col_g2:
            st.markdown("#### Coste por Recarga")
            fig_coste = go.Figure()
            fig_coste.add_trace(go.Bar(
                x=df_año['fecha_recarga'].dt.strftime('%d/%m'),
                y=df_año['coste_total'],
                name='Coste €',
                marker_color=CHART_COLORS_FINANCE['income'],
                marker_line=dict(width=0),
                hovertemplate='<b>%{x}</b><br>Coste: %{y:.2f} €<extra></extra>'
            ))
            apply_theme_to_fig(fig_coste, title=None, height=300, showlegend=False)
            st.plotly_chart(fig_coste, use_container_width=True)

        # Gráfico 2: Distribución por franja
        st.markdown("#### Distribución por Franja Horaria")
        distribucion_franjas = df_año['franja_horaria'].value_counts()

        # Crear DataFrame para el gráfico de pie
        df_franjas = pd.DataFrame({
            'franja': distribucion_franjas.index,
            'recargas': distribucion_franjas.values
        })

        fig_franjas = create_themed_pie_chart(
            df_franjas,
            names='franja',
            values='recargas',
            title='Distribución por Franja Horaria',
            hole=0.4
        )
        st.plotly_chart(fig_franjas, use_container_width=True)

        # Tabla resumen por mes
        st.markdown("#### Resumen Mensual")
        df_año['mes_nombre'] = df_año['fecha_recarga'].dt.strftime('%B')

        # Agrupar datos por mes
        resumen_mes = df_año.groupby('mes_nombre').agg({
            'kwh_cargados': 'sum',
            'km_recorridos': 'sum',
            'coste_total': 'sum'
        }).round(2)

        # Calcular consumo medio por mes (si hay km registrados)
        def calcular_consumo_mes(grupo):
            km_total = grupo['km_recorridos'].sum()
            kwh_total = grupo['kwh_cargados'].sum()
            if km_total > 0:
                return round((kwh_total / km_total) * 100, 1)
            else:
                # Si no hay km, usar promedio de los consumos_medio registrados
                consumos = grupo['consumo_medio'][grupo['consumo_medio'] > 0]
                return round(consumos.mean(), 1) if len(consumos) > 0 else 0

        resumen_consumo = df_año.groupby('mes_nombre').apply(calcular_consumo_mes)
        resumen_mes['consumo_medio'] = resumen_consumo

        resumen_mes.columns = ['kWh Total', 'Km Total', 'Coste Total €', 'Consumo Medio (kWh/100km)']
        st.dataframe(resumen_mes, use_container_width=True)

    else:
        st.info(f"No hay recargas en {año_seleccionado}")
