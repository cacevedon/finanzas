import streamlit as st
import numpy as np
import pandas as pd
import numpy_financial as npf
import math
import io

# Configuración de página
st.set_page_config(
    page_title="Plataforma de Simulación & Ingeniería Financiera",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        color: #2F5496;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #555;
        margin-bottom: 1.5rem;
    }
    .val-badge {
        background-color: #E2EFDA;
        color: #276A3C;
        padding: 4px 10px;
        border-radius: 4px;
        font-weight: 600;
        font-size: 0.88rem;
        margin-top: -8px;
        margin-bottom: 12px;
        display: inline-block;
    }
    .stButton>button {
        background-color: #2F5496;
        color: white;
        border-radius: 5px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Helper para parsing de números ingresados por el usuario
def parse_num(val_str, default_val=0.0):
    if val_str is None:
        return float(default_val)
    s = str(val_str).strip().replace("$", "").replace(" ", "")
    if not s:
        return float(default_val)
    
    if "." in s and "," in s:
        s = s.replace(".", "").replace(",", ".")
    elif "." in s:
        parts = s.split(".")
        if len(parts) > 2:
            s = s.replace(".", "")
        elif len(parts) == 2:
            if len(parts[1]) == 3 and len(parts[0]) <= 3:
                s = s.replace(".", "")
            elif len(parts[1]) == 3:
                s = s.replace(".", "")
    elif "," in s:
        parts = s.split(",")
        if len(parts) > 2:
            s = s.replace(",", "")
        elif len(parts) == 2:
            if len(parts[1]) == 3 and len(parts[0]) <= 3:
                s = s.replace(",", "")
            else:
                s = s.replace(",", ".")
    
    try:
        return float(s)
    except:
        return float(default_val)

# Helper para formateo de miles en formato latino (punto para miles, coma para decimales)
def fmt_m(val, dec=2):
    try:
        val = float(val)
        formatted = f"{val:,.{dec}f}"
        return formatted.replace(",", "X").replace(".", ",").replace("X", ".")
    except:
        return str(val)

def fmt_n(val, dec=2):
    try:
        val = float(val)
        if dec == 0:
            formatted = f"{int(round(val)):,d}"
            return formatted.replace(",", ".")
        else:
            formatted = f"{val:,.{dec}f}"
            return formatted.replace(",", "X").replace(".", ",").replace("X", ".")
    except:
        return str(val)

# Callback para formatear la casilla al cambiar el valor
def format_input_cb(key, default_val):
    val_str = st.session_state.get(key, "")
    parsed = parse_num(val_str, default_val)
    if parsed.is_integer():
        st.session_state[key] = fmt_n(parsed, 0)
    else:
        st.session_state[key] = fmt_n(parsed, 2)

# Widget inteligente de casilla numérica con separador de miles en la misma casilla
def smart_num_input(label, default_val, key, help_text=None):
    if key not in st.session_state:
        st.session_state[key] = fmt_n(default_val, 0 if float(default_val).is_integer() else 2)
    
    st.text_input(
        label,
        key=key,
        on_change=format_input_cb,
        args=(key, default_val),
        help=help_text
    )
    
    val_str = st.session_state.get(key, "")
    return parse_num(val_str, default_val)

# Helper para exportación segura a Excel (.xlsx) o CSV (.csv)
def export_dataframe_button(df, filename_prefix="tabla_desarrollo"):
    try:
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name="Desarrollo")
        excel_data = output.getvalue()
        
        st.download_button(
            label="📥 Exportar Tabla de Desarrollo a Excel (.xlsx)",
            data=excel_data,
            file_name=f"{filename_prefix}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    except Exception:
        csv_data = df.to_csv(index=False, sep=";", decimal=",").encode('utf-8-sig')
        st.download_button(
            label="📥 Exportar Tabla de Desarrollo a CSV (Compatible con Excel)",
            data=csv_data,
            file_name=f"{filename_prefix}.csv",
            mime="text/csv"
        )

# Encabezado Principal
st.markdown('<div class="main-header">PLATAFORMA DE SIMULACIÓN Y CÁLCULO FINANCIERO</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Plataforma interactiva de simulación, análisis y modelos de ingeniería financiera.</div>', unsafe_allow_html=True)

# Barra lateral de navegación
st.sidebar.title("📌 Navegación del Sistema")
modulo = st.sidebar.radio(
    "Selecciona un Módulo:",
    [
        "1. Fundamentos y Decisiones",
        "2. Interés Simple y Compuesto",
        "3. Conversión de Tasas (TNA/TEA)",
        "4. Anualidades y Amortización",
        "5. Gradientes Financieros",
        "6. Presupuesto y Flujo de Caja",
        "7. Evaluación de Proyectos (VAN/TIR)",
        "8. Calculadoras Especializadas"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info("💡 **Tip:** Modifica los parámetros de los simuladores en tiempo real para evaluar diferentes escenarios.")

# ==========================================
# MÓDULO 1: FUNDAMENTOS
# ==========================================
if modulo == "1. Fundamentos y Decisiones":
    st.header("Módulo 1: Fundamentos y Decisiones Financieras")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📚 Marco Teórico Clave")
        st.markdown("""
        - **Valor del Dinero en el Tiempo (VDT):** Un capital hoy posee un valor superior a un capital futuro equivalente debido a su capacidad de generar rentabilidad, la inflación y la prima por riesgo.
        - **Costo de Oportunidad:** El rendimiento de la mejor alternativa sacrificada al asignar recursos a una opción de inversión.
        - **Relación Riesgo - Liquidez - Rentabilidad:** A mayor liquidez inmediata, menor suele ser la rentabilidad esperada del activo.
        - **Intermediación Financiera:** El sistema bancario canaliza excedentes de liquidez desde agentes superavitarios hacia agentes deficitarios.
        """)
        
    with col2:
        st.subheader("🎯 Matriz de Decisiones Prácticas")
        caso = st.selectbox("Selecciona un Escenario de Análisis:", [
            "Escenario 1: Asignación de Bono de $500.000",
            "Escenario 2: Decisión de Compra a Crédito ($600.000)",
            "Escenario 3: Presupuesto y Contingencia Médica (15%)",
            "Escenario 4: Gestión de Excedente de Caja ($5.000.000)"
        ])
        
        if "Bono" in caso:
            st.info("**Situación:** Asignación de un excedente de $500.000 entre consumo o depósito a plazo fijo al 0,60% mensual.")
            st.success(f"**Recomendación:** Invertir en un instrumento conservador. En 12 meses el monto asciende a **${fmt_m(500000*(1.006**12))}**. Prioriza la acumulación de capital y la preservación del VDT.")
        elif "Crédito" in caso:
            st.info("**Situación:** Compra de equipo al contado por $600.000 vs. 12 cuotas de $62.000 (Total $744.000).")
            st.warning("**Recomendación:** Comprar al contado de contar con liquidez. La opción a crédito implica un costo financiero total implícito superior al 40,00% anual.")
        elif "Contingencia" in caso:
            st.info("**Situación:** Fondo con ingresos de $1.200.000 enfrenta un gasto imprevisto del 15% ($180.000).")
            st.error("**Recomendación:** Utilizar la reserva de emergencia. Reestructurar gastos prescindibles del mes y evitar líneas de crédito rotativo de alta tasa.")
        else:
            st.info("**Situación:** Excedente operativo de $5.000.000 ocioso en la cuenta corriente.")
            st.success("**Recomendación:** Colocar el 60% ($3.000.000) en pactos diarios o fondos de liquidez inmediata para rentabilizar saldos sin perder operatividad.")

# ==========================================
# MÓDULO 2: INTERÉS SIMPLE Y COMPUESTO
# ==========================================
elif modulo == "2. Interés Simple y Compuesto":
    st.header("Módulo 2: Interés Simple e Interés Compuesto")
    
    st.subheader("⚙️ Calculadora Interactiva de Capitalización")
    
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        vp_input = smart_num_input("Capital Inicial (VP $):", 1000000.0, key="m2_vp")
        st.markdown(f'<div class="val-badge">💵 VP: ${fmt_m(vp_input)}</div>', unsafe_allow_html=True)
    with c2:
        tasa_input = smart_num_input("Tasa Periódica (%):", 1.50, key="m2_tasa") / 100.0
        st.markdown(f'<div class="val-badge">📈 Tasa: {fmt_n(tasa_input*100, 2)}%</div>', unsafe_allow_html=True)
    with c3:
        n_input = int(smart_num_input("Plazo (Periodos):", 12.0, key="m2_n"))
        st.markdown(f'<div class="val-badge">⏳ Plazo: {n_input} periodos</div>', unsafe_allow_html=True)
    with c4:
        regimen = st.selectbox("Régimen de Análisis:", ["Interés Compuesto", "Interés Simple", "Comparar Ambos"])
        
    vf_simple = vp_input * (1 + tasa_input * n_input)
    vf_compuesto = vp_input * ((1 + tasa_input) ** n_input)
    
    res_df = pd.DataFrame({
        "Periodo": list(range(0, n_input + 1)),
        "Interés Simple ($)": [vp_input * (1 + tasa_input * t) for t in range(0, n_input + 1)],
        "Interés Compuesto ($)": [vp_input * ((1 + tasa_input) ** t) for t in range(0, n_input + 1)]
    })
    
    st.markdown("#### Resultados Proyectados")
    mc1, mc2, mc3 = st.columns(3)
    mc1.metric("Valor Futuro (Simple)", f"${fmt_m(vf_simple)}")
    mc2.metric("Valor Futuro (Compuesto)", f"${fmt_m(vf_compuesto)}")
    mc3.metric("Diferencia por Capitalización", f"${fmt_m(vf_compuesto - vf_simple)}")
    
    st.line_chart(res_df.set_index("Periodo"))

# ==========================================
# MÓDULO 3: CONVERSIÓN DE TASAS
# ==========================================
elif modulo == "3. Conversión de Tasas (TNA/TEA)":
    st.header("Módulo 3: Conversión y Decodificación de Tasas de Interés")
    
    col_t1, col_t2 = st.columns(2)
    
    with col_t1:
        st.subheader("🔄 Conversor Universal de TNA a TEA")
        tna_val = smart_num_input("Tasa Nominal Anual (TNA %):", 24.0, key="m3_tna") / 100.0
        st.markdown(f'<div class="val-badge">📊 TNA: {fmt_n(tna_val*100, 2)}%</div>', unsafe_allow_html=True)
        freq_dict = {
            "Mensual (m=12)": 12,
            "Bimestral (m=6)": 6,
            "Trimestral (m=4)": 4,
            "Cuatrimestral (m=3)": 3,
            "Semestral (m=2)": 2,
            "Diaria (m=360)": 360
        }
        freq_sel = st.selectbox("Frecuencia de Capitalización (m):", list(freq_dict.keys()))
        m_val = freq_dict[freq_sel]
        
        i_per = tna_val / m_val
        tea_calc = ((1 + i_per) ** m_val) - 1.0
        
        st.write(f"• **Tasa Periódica ($i'$):** {fmt_n(i_per*100, 4)}%")
        st.metric("Tasa Efectiva Anual Equivalente (TEA)", f"{fmt_n(tea_calc*100, 4)}%")

    with col_t2:
        st.subheader("⚖️ Comparador Financiero: Banco X vs. Banco Y")
        st.markdown("""
        - **Banco X:** 9,00% TNA con capitalización trimestral ($m=4$).
        - **Banco Y:** 9,20% TEA directa.
        """)
        tea_x = ((1 + 0.09/4)**4) - 1.0
        tea_y = 0.092
        
        st.write(f"• **TEA Banco X:** $(1 + 0,09/4)^4 - 1 =$ **{fmt_n(tea_x*100, 4)}%**")
        st.write(f"• **TEA Banco Y:** **{fmt_n(tea_y*100, 4)}%**")
        
        if tea_x > tea_y:
            st.success(f"✅ **Para Inversión/Ahorro:** Conviene **Banco X** ({fmt_n(tea_x*100, 2)}% TEA).\n\n✅ **Para Crédito:** Conviene **Banco Y** (9,20% TEA).")

# ==========================================
# MÓDULO 4: ANUALIDADES
# ==========================================
elif modulo == "4. Anualidades y Amortización":
    st.header("Módulo 4: Anualidades y Tablas de Amortización")
    
    st.subheader("💳 Simulador de Préstamos y Amortización (Método Francés)")
    
    ac1, ac2, ac3 = st.columns(3)
    with ac1:
        monto_prestamo = smart_num_input("Monto del Préstamo ($):", 30000.0, key="m4_monto")
        st.markdown(f'<div class="val-badge">💵 Préstamo: ${fmt_m(monto_prestamo)}</div>', unsafe_allow_html=True)
    with ac2:
        tasa_mensual_anu = smart_num_input("Tasa Efectiva Mensual (%):", 1.20, key="m4_tasa") / 100.0
        st.markdown(f'<div class="val-badge">📈 Tasa: {fmt_n(tasa_mensual_anu*100, 2)}%</div>', unsafe_allow_html=True)
    with ac3:
        plazo_meses = int(smart_num_input("Plazo en Meses (n):", 36.0, key="m4_plazo"))
        st.markdown(f'<div class="val-badge">⏳ Plazo: {plazo_meses} meses</div>', unsafe_allow_html=True)
        
    cuota_fija = monto_prestamo * (tasa_mensual_anu / (1 - (1 + tasa_mensual_anu)**(-plazo_meses)))
    
    st.metric("Cuota Mensual Calculada (R)", f"${fmt_m(cuota_fija)}")
    
    saldo = monto_prestamo
    amort_data = []
    for mes in range(1, plazo_meses + 1):
        interes_mes = saldo * tasa_mensual_anu
        capital_mes = cuota_fija - interes_mes
        saldo_final = max(0.0, saldo - capital_mes)
        amort_data.append({
            "Mes": mes,
            "Saldo Inicial ($)": fmt_m(saldo),
            "Cuota ($)": fmt_m(cuota_fija),
            "Interés ($)": fmt_m(interes_mes),
            "Amortización ($)": fmt_m(capital_mes),
            "Saldo Final ($)": fmt_m(saldo_final)
        })
        saldo = saldo_final
        
    df_amort = pd.DataFrame(amort_data)
    
    st.markdown("#### Tabla de Amortización Dinámica")
    st.dataframe(df_amort, hide_index=True, height=280)
    export_dataframe_button(df_amort, "tabla_amortizacion_m4")

# ==========================================
# MÓDULO 5: GRADIENTES
# ==========================================
elif modulo == "5. Gradientes Financieros":
    st.header("Módulo 5: Gradientes Financieros (Series Variables)")
    
    st.subheader("📈 Comparativa de Series: Constante vs. Aritmética vs. Geométrica")
    
    gc1, gc2, gc3 = st.columns(3)
    with gc1:
        base_a = smart_num_input("Flujo Base Inicial (A $):", 1000.0, key="m5_base")
        st.markdown(f'<div class="val-badge">💵 Base A: ${fmt_m(base_a)}</div>', unsafe_allow_html=True)
    with gc2:
        grad_g = smart_num_input("Gradiente Aritmético (G $):", 200.0, key="m5_grad_g")
        st.markdown(f'<div class="val-badge">💵 Gradiente G: ${fmt_m(grad_g)}</div>', unsafe_allow_html=True)
    with gc3:
        grad_pct = smart_num_input("Gradiente Geométrico (g %):", 10.0, key="m5_grad_pct") / 100.0
        st.markdown(f'<div class="val-badge">📈 Gradiente g: {fmt_n(grad_pct*100, 2)}%</div>', unsafe_allow_html=True)
        
    periodos_g = 10
    grad_df = pd.DataFrame({
        "Año": list(range(1, periodos_g + 1)),
        "Serie Constante": [base_a] * periodos_g,
        "Gradiente Aritmético (+G)": [base_a + (t - 1) * grad_g for t in range(1, periodos_g + 1)],
        "Gradiente Geométrico (+g)": [base_a * ((1 + grad_pct)**(t - 1)) for t in range(1, periodos_g + 1)]
    })
    
    st.line_chart(grad_df.set_index("Año"))

# ==========================================
# MÓDULO 6: PRESUPUESTOS
# ==========================================
elif modulo == "6. Presupuesto y Flujo de Caja":
    st.header("Módulo 6: Presupuestos y Control de Caja Operacional")
    
    st.subheader("📊 Simulador de Presupuesto Mensual a 12 Meses con Inflación")
    
    pc1, pc2, pc3 = st.columns(3)
    with pc1:
        v_base = smart_num_input("Ventas Mes 1 ($):", 15000.0, key="m6_ventas")
        st.markdown(f'<div class="val-badge">💵 Ventas Mes 1: ${fmt_m(v_base)}</div>', unsafe_allow_html=True)
    with pc2:
        g_ventas = smart_num_input("Crecimiento Ventas Mensual (%):", 1.50, key="m6_g_ventas") / 100.0
        st.markdown(f'<div class="val-badge">📈 Crecimiento: {fmt_n(g_ventas*100, 2)}%</div>', unsafe_allow_html=True)
    with pc3:
        inf_mensual = smart_num_input("Inflación Costos Mensual (%):", 0.50, key="m6_inf") / 100.0
        st.markdown(f'<div class="val-badge">📉 Inflación: {fmt_n(inf_mensual*100, 2)}%</div>', unsafe_allow_html=True)
        
    meses_p = 12
    p_data = []
    caja_acum = 8000.0
    
    for m in range(1, meses_p + 1):
        ventas_m = v_base * ((1 + g_ventas)**(m - 1))
        costos_m = (ventas_m * 0.40) * ((1 + inf_mensual)**(m - 1))
        fijos_m = 7000.0 * ((1 + inf_mensual)**(m - 1))
        reserva_m = ventas_m * 0.05
        egresos_total = costos_m + fijos_m + reserva_m
        flujo_neto = ventas_m - egresos_total
        caja_acum += flujo_neto
        
        p_data.append({
            "Mes": f"Mes {m}",
            "Ventas ($)": fmt_m(ventas_m),
            "Total Egresos ($)": fmt_m(egresos_total),
            "Flujo Neto ($)": fmt_m(flujo_neto),
            "Caja Acumulada ($)": fmt_m(caja_acum)
        })
        
    df_pres = pd.DataFrame(p_data)
    st.dataframe(df_pres, hide_index=True)
    export_dataframe_button(df_pres, "presupuesto_m6")

# ==========================================
# MÓDULO 7: EVALUACIÓN DE PROYECTOS
# ==========================================
elif modulo == "7. Evaluación de Proyectos (VAN/TIR)":
    st.header("Módulo 7: Evaluación Financiera de Proyectos")
    
    st.subheader("🎯 Punto de Equilibrio Operacional")
    eq1, eq2, eq3 = st.columns(3)
    with eq1:
        cf_val = smart_num_input("Costos Fijos Totales ($):", 120000.0, key="m7_cf")
        st.markdown(f'<div class="val-badge">💵 Costos Fijos: ${fmt_m(cf_val)}</div>', unsafe_allow_html=True)
    with eq2:
        p_val = smart_num_input("Precio Unitario ($):", 50.0, key="m7_p")
        st.markdown(f'<div class="val-badge">💵 Precio: ${fmt_m(p_val)}</div>', unsafe_allow_html=True)
    with eq3:
        cv_val = smart_num_input("Costo Variable Unitario ($):", 30.0, key="m7_cv")
        st.markdown(f'<div class="val-badge">💵 Costo Var: ${fmt_m(cv_val)}</div>', unsafe_allow_html=True)
        
    mc_unit = p_val - cv_val
    if mc_unit > 0:
        q_eq = cf_val / mc_unit
        ing_eq = q_eq * p_val
        st.success(f"• **Punto de Equilibrio en Unidades:** **{fmt_n(q_eq, 0)} unidades**")
        st.success(f"• **Ingreso de Equilibrio:** **${fmt_m(ing_eq)}**")
    else:
        st.error("El precio unitario debe ser superior al costo variable.")

# ==========================================
# MÓDULO 8: CALCULADORAS ESPECIALIZADAS
# ==========================================
elif modulo == "8. Calculadoras Especializadas":
    st.header("Módulo 8: Calculadoras Especializadas")
    st.markdown("Suite avanzada de cálculo e ingeniería financiera. Todos los modelos se ejecutan automáticamente en tiempo real.")
    
    calc_option = st.selectbox(
        "Selecciona la Herramienta de Cálculo:",
        [
            "I. Desglose de Interés y Amortización para una Cuota Específica (k) con Convertidor de Tasas",
            "II. Valor Futuro con Interés Compuesto (Plazos Enteros y Fraccionados)",
            "III. Valor Futuro de Anualidades y Fondos de Ahorro (Ordinarias y Anticipadas)",
            "IV. Valuación de Flujos Múltiples e Irregulares (VP en t=0 y VF en t=N)",
            "V. Despeje de Plazo Requerido (n) y Tasa Implícita para Metas de Capital",
            "VI. Conversión Avanzada de Tasas Nominales/Efectivas y Spread Financiero",
            "VII. Valor Presente (VP) de Pagos Futuros Específicos Discretos en Meses",
            "VIII. Valor Futuro (VF) de Depósitos Proyectados Discretos en Meses Específicos (Tasas Variables)",
            "IX. Comparador de Ofertas Bancarias a Plazo Fijo / Depósitos (Múltiples Bancos y Tipos de Tasa)",
            "X. Crédito Comercial / Bienes de Capital (Pagos Anuales & Cuota Mensual)",
            "XI. Tasa Implícita Anual para Créditos o Inversiones de Pago Único",
            "XII. Valor Presente de Cero / Descuento con Alta Precisión Decimal (4 Decimales)"
        ]
    )
    
    st.markdown("---")
    
    # -------------------------------------------------------------
    # HERRAMIENTA I: DESGLOSE DE CUOTA k CON CONVERTIDOR AUTOMÁTICO
    # -------------------------------------------------------------
    if calc_option.startswith("I. "):
        st.subheader("🛠️ I. Desglose de Interés y Amortización (Cuota Especifica k)")
        st.caption("Configura el préstamo y la periodicidad de la tasa entregada. El sistema homogeneizará automáticamente la tasa y calculará la cuota y el desglose k.")
        
        k1, k2, k3 = st.columns(3)
        with k1:
            vp_loan = smart_num_input("Monto del Préstamo (VP $):", 1000000.0, key="calc1_vp")
            st.markdown(f'<div class="val-badge">💵 Préstamo: ${fmt_m(vp_loan)}</div>', unsafe_allow_html=True)
            
            pago_freq_name = st.selectbox("Periodicidad de Pago de las Cuotas:", [
                "Mensual (12/año)", "Bimestral (6/año)", "Trimestral (4/año)", 
                "Cuatrimestral (3/año)", "Semestral (2/año)", "Anual (1/año)"
            ], key="pago_freq")
            
        with k2:
            rate_val_in = smart_num_input("Tasa de Interés Ingresada (%):", 7.45, key="calc1_rate")
            st.markdown(f'<div class="val-badge">📈 Tasa Ingresada: {fmt_n(rate_val_in, 2)}%</div>', unsafe_allow_html=True)
            
            rate_freq_name = st.selectbox("Periodicidad de la Tasa Ingresada:", [
                "Cuatrimestral (3/año)", "Mensual (12/año)", "Bimestral (6/año)", 
                "Trimestral (4/año)", "Semestral (2/año)", "Anual / TEA (1/año)"
            ], key="rate_freq")
            
        with k3:
            plazo_num = smart_num_input("Duración / Plazo Total:", 5.0, key="calc1_plazo")
            plazo_unit = st.selectbox("Unidad del Plazo Total:", ["Años", "Meses", "Cuatrimestres", "Semestres"], key="plazo_unit")
            k_eval = int(smart_num_input("Número de Cuota a Evaluar (k):", 4.0, key="calc1_k"))

        freq_map = {"Mensual (12/año)": 12, "Bimestral (6/año)": 6, "Trimestral (4/año)": 4, "Cuatrimestral (3/año)": 3, "Semestral (2/año)": 2, "Anual (1/año)": 1, "Anual / TEA (1/año)": 1}
        m_pago = freq_map[pago_freq_name]
        m_tasa = freq_map[rate_freq_name]
        
        i_tasa_dec = rate_val_in / 100.0
        tea_base = ((1 + i_tasa_dec) ** m_tasa) - 1.0
        i_cuota = ((1 + tea_base) ** (1.0 / m_pago)) - 1.0
        
        if plazo_unit == "Años":
            n_cuotas = int(round(plazo_num * m_pago))
        elif plazo_unit == "Meses":
            n_cuotas = int(round(plazo_num * (m_pago / 12.0)))
        elif plazo_unit == "Cuatrimestres":
            n_cuotas = int(round(plazo_num * (m_pago / 3.0)))
        else:
            n_cuotas = int(round(plazo_num * (m_pago / 2.0)))
            
        if n_cuotas < 1: n_cuotas = 1
        if k_eval > n_cuotas: k_eval = n_cuotas

        cuota_r = vp_loan * (i_cuota / (1 - (1 + i_cuota)**(-n_cuotas)))
        
        saldo_curr = vp_loan
        k_interes = 0.0
        k_amort = 0.0
        k_saldo_prev = 0.0
        k_saldo_final = 0.0
        
        amort_full = []
        for period in range(1, n_cuotas + 1):
            int_p = saldo_curr * i_cuota
            amort_p = cuota_r - int_p
            saldo_next = max(0.0, saldo_curr - amort_p)
            
            if period == k_eval:
                k_saldo_prev = saldo_curr
                k_interes = int_p
                k_amort = amort_p
                k_saldo_final = saldo_next
                
            amort_full.append({
                "Cuota #": period,
                "Saldo Inicial ($)": fmt_m(saldo_curr),
                "Cuota ($)": fmt_m(cuota_r),
                "Interés ($)": fmt_m(int_p),
                "Amortización ($)": fmt_m(amort_p),
                "Saldo Final ($)": fmt_m(saldo_next)
            })
            saldo_curr = saldo_next

        st.markdown("#### 📊 Parámetros Homogeneizados Automáticamente:")
        st.write(f"• **Tasa Periódica Ajustada por Cuota ($i_{{pago}}$):** **{fmt_n(i_cuota*100, 4)}%** (TEA Equivalente: {fmt_n(tea_base*100, 2)}%)")
        st.write(f"• **Cantidad Total de Cuotas ($n$):** **{n_cuotas} cuotas**")
        st.write(f"• **Valor Cuota Fija ($R$):** **${fmt_m(cuota_r)}**")
        
        st.markdown(f"#### 🎯 Desglose Específico para la Cuota $k = {k_eval}$:")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Saldo Inicial Cuota k", f"${fmt_m(k_saldo_prev)}")
        m2.metric("Interés de la Cuota k", f"${fmt_m(k_interes)}")
        m3.metric("Amortización Cuota k", f"${fmt_m(k_amort)}")
        m4.metric("Saldo Insoluto Final", f"${fmt_m(k_saldo_final)}")
        
        df_k_full = pd.DataFrame(amort_full)
        st.dataframe(df_k_full, hide_index=True)
        export_dataframe_button(df_k_full, f"tabla_amortizacion_cuota_k_{k_eval}")

    # -------------------------------------------------------------
    # HERRAMIENTA II: VALOR FUTURO INTERÉS COMPUESTO
    # -------------------------------------------------------------
    elif calc_option.startswith("II. "):
        st.subheader("🛠️ II. Valor Futuro con Interés Compuesto (Plazos Fraccionados)")
        
        sf1, sf2, sf3 = st.columns(3)
        with sf1:
            s1_vp = smart_num_input("Capital Presente (VP $):", 1000.0, key="calc2_vp")
            st.markdown(f'<div class="val-badge">💵 VP: ${fmt_m(s1_vp)}</div>', unsafe_allow_html=True)
        with sf2:
            s1_tasa = smart_num_input("Tasa de Interés Anual (%):", 5.0, key="calc2_tasa") / 100.0
            st.markdown(f'<div class="val-badge">📈 Tasa Anual: {fmt_n(s1_tasa*100, 2)}%</div>', unsafe_allow_html=True)
        with sf3:
            s1_meses = smart_num_input("Plazo en Meses (n):", 16.0, key="calc2_meses")
            st.markdown(f'<div class="val-badge">⏳ Plazo: {s1_meses} meses ({fmt_n(s1_meses/12, 2)} años)</div>', unsafe_allow_html=True)
            
        s1_vf = s1_vp * ((1 + s1_tasa) ** (s1_meses / 12.0))
        st.metric("Valor Futuro Resultante (VF)", f"${fmt_m(s1_vf)}")
        st.info(f"Fórmula aplicada por el sistema: $VF = {fmt_m(s1_vp)} \\times (1 + {fmt_n(s1_tasa*100, 2)}\\%)^{{({fmt_n(s1_meses, 0)}/12)}} = {fmt_m(s1_vf)}$")

    # -------------------------------------------------------------
    # HERRAMIENTA III: VF ANUALIDADES Y FONDOS DE AHORRO
    # -------------------------------------------------------------
    elif calc_option.startswith("III. "):
        st.subheader("🛠️ III. Valor Futuro de Anualidades (Acumulación de Fondos)")
        
        af1, af2, af3, af4 = st.columns(4)
        with af1:
            r_dep = smart_num_input("Depósito Periódico (R $):", 500.0, key="calc3_r")
            st.markdown(f'<div class="val-badge">💵 Cuota R: ${fmt_m(r_dep)}</div>', unsafe_allow_html=True)
        with af2:
            i_dep = smart_num_input("Tasa Periódica (%):", 0.80, key="calc3_i") / 100.0
            st.markdown(f'<div class="val-badge">📈 Tasa: {fmt_n(i_dep*100, 2)}%</div>', unsafe_allow_html=True)
        with af3:
            n_dep = int(smart_num_input("Cantidad de Cuotas (n):", 300.0, key="calc3_n"))
            st.markdown(f'<div class="val-badge">⏳ Cuotas: {n_dep}</div>', unsafe_allow_html=True)
        with af4:
            tipo_anualidad = st.selectbox("Modalidad de Depósito:", ["Ordinaria / Vencida (Al final)", "Anticipada (Al inicio)"])
            
        vf_ord = r_dep * (((1 + i_dep)**n_dep - 1) / i_dep)
        if "Anticipada" in tipo_anualidad:
            vf_final = vf_ord * (1 + i_dep)
        else:
            vf_final = vf_ord
            
        total_aportes = r_dep * n_dep
        intereses_ganados = vf_final - total_aportes
        
        m_a1, m_a2, m_a3 = st.columns(3)
        m_a1.metric("Valor Futuro Acumulado (VF)", f"${fmt_m(vf_final)}")
        m_a2.metric("Total Aportes Efectuados", f"${fmt_m(total_aportes)}")
        m_a3.metric("Intereses Ganados", f"${fmt_m(intereses_ganados)}")

    # -------------------------------------------------------------
    # HERRAMIENTA IV: VALUACIÓN FLUJOS MÚLTIPLES
    # -------------------------------------------------------------
    elif calc_option.startswith("IV. "):
        st.subheader("🛠️ IV. Valuación de Flujos Múltiples e Irregulares")
        
        mf1, mf2 = st.columns(2)
        with mf1:
            tasa_flujos = smart_num_input("Tasa de Descuento/Capitalización (%):", 12.0, key="calc4_tasa") / 100.0
            st.markdown(f'<div class="val-badge">📈 Tasa: {fmt_n(tasa_flujos*100, 2)}%</div>', unsafe_allow_html=True)
        with mf2:
            num_flujos = int(smart_num_input("Cantidad de Flujos a Ingresar:", 4.0, key="calc4_num"))
            if num_flujos < 1: num_flujos = 1
            if num_flujos > 10: num_flujos = 10
            
        st.write("Ingresa los montos de cada flujo periódico:")
        flujos_inputs = []
        f_cols = st.columns(min(int(num_flujos), 5))
        for idx in range(int(num_flujos)):
            col_target = f_cols[idx % 5]
            with col_target:
                f_val = smart_num_input(f"Flujo Periodo {idx+1} ($):", 100.0 + idx*20.0, key=f"calc4_f_{idx}")
                st.markdown(f'<div class="val-badge">F{idx+1}: ${fmt_m(f_val)}</div>', unsafe_allow_html=True)
                flujos_inputs.append(f_val)
                
        vp_m = sum([f / ((1 + tasa_flujos)**(t+1)) for t, f in enumerate(flujos_inputs)])
        vf_m = sum([f * ((1 + tasa_flujos)**(num_flujos - (t+1))) for t, f in enumerate(flujos_inputs)])
        
        col_res1, col_res2 = st.columns(2)
        col_res1.metric("Valor Presente Total (VP en t=0)", f"${fmt_m(vp_m)}")
        col_res2.metric(f"Valor Futuro Total (VF en t={num_flujos})", f"${fmt_m(vf_m)}")

    # -------------------------------------------------------------
    # HERRAMIENTA V: DESPEJE DE PLAZO n Y TASA IMPLÍCITA
    # -------------------------------------------------------------
    elif calc_option.startswith("V. "):
        st.subheader("🛠️ V. Despeje de Plazo Requerido (n) para Metas de Capital")
        
        s2f1, s2f2, s2f3 = st.columns(3)
        with s2f1:
            s2_vp = smart_num_input("Capital Inicial (VP $):", 2000.0, key="calc5_vp")
            st.markdown(f'<div class="val-badge">💵 VP: ${fmt_m(s2_vp)}</div>', unsafe_allow_html=True)
        with s2f2:
            s2_vf = smart_num_input("Meta de Capital Futuro (VF $):", 3525.0, key="calc5_vf")
            st.markdown(f'<div class="val-badge">💵 VF Meta: ${fmt_m(s2_vf)}</div>', unsafe_allow_html=True)
        with s2f3:
            s2_tasa = smart_num_input("Tasa de Interés Anual (%):", 12.0, key="calc5_tasa") / 100.0
            st.markdown(f'<div class="val-badge">📈 Tasa Anual: {fmt_n(s2_tasa*100, 2)}%</div>', unsafe_allow_html=True)
            
        if s2_vf > s2_vp and s2_tasa > 0:
            n_req = math.log(s2_vf / s2_vp) / math.log(1 + s2_tasa)
            st.metric("Plazo Requerido (n)", f"{fmt_n(n_req, 2)} años", delta=f"{fmt_n(n_req*12, 1)} meses")
            st.info(f"Fórmula aplicada por el sistema: $n = \\frac{{\\ln({fmt_m(s2_vf)} / {fmt_m(s2_vp)})}}{{\\ln(1 + {s2_tasa:.2f})}} = {fmt_n(n_req, 2)}$ años.")
        else:
            st.error("El Valor Futuro (VF) debe ser mayor al Valor Presente (VP).")

    # -------------------------------------------------------------
    # HERRAMIENTA VI: CONVERSIÓN AVANZADA Y SPREAD FINANCIERO
    # -------------------------------------------------------------
    elif calc_option.startswith("VI. "):
        st.subheader("🛠️ VI. Conversión Avanzada de Tasas y Spread Financiero")
        
        cv1, cv2 = st.columns(2)
        with cv1:
            tna_base_input = smart_num_input("Tasa Nominal Anual Base (TNA %):", 24.0, key="calc6_tna") / 100.0
            st.markdown(f'<div class="val-badge">📊 TNA: {fmt_n(tna_base_input*100, 2)}%</div>', unsafe_allow_html=True)
            m_cap = int(smart_num_input("Frecuencia de Capitalización (m por año):", 4.0, key="calc6_m"))
            if m_cap < 1: m_cap = 1
            
            i_m_sub = tna_base_input / m_cap
            tea_res = ((1 + i_m_sub)**m_cap) - 1.0
            st.metric("Tasa Efectiva Anual (TEA)", f"{fmt_n(tea_res*100, 4)}%")
            
        with cv2:
            tasa_ref = smart_num_input("Tasa de Referencia de Mercado (TEA %):", 22.0, key="calc6_ref") / 100.0
            st.markdown(f'<div class="val-badge">📊 Referencia: {fmt_n(tasa_ref*100, 2)}%</div>', unsafe_allow_html=True)
            spread_bp = (tea_res - tasa_ref) * 10000.0
            st.metric("Diferencial / Spread Financiero", f"{fmt_n(spread_bp, 0)} puntos básicos (bps)", delta=f"{fmt_n((tea_res - tasa_ref)*100, 2)}%")

    # -------------------------------------------------------------
    # HERRAMIENTA VII: VP DE PAGOS FUTUROS ESPECÍFICOS DISCRETOS
    # -------------------------------------------------------------
    elif calc_option.startswith("VII. "):
        st.subheader("🛠️ VII. Valor Presente (VP) de Pagos Futuros Específicos Discretos en Meses")
        st.caption("Calcula el capital requerido hoy a una fecha de referencia para cubrir compromisos futuros en meses específicos.")
        
        u1, u2 = st.columns(2)
        with u1:
            tasa_univ = smart_num_input("Tasa de Interés Mensual (%):", 2.50, key="calc7_tasa") / 100.0
            st.markdown(f'<div class="val-badge">📈 Tasa Mensual: {fmt_n(tasa_univ*100, 2)}%</div>', unsafe_allow_html=True)
        with u2:
            num_pagos_u = int(smart_num_input("Cantidad de Pagos Futuros:", 3.0, key="calc7_num"))
            if num_pagos_u < 1: num_pagos_u = 1
            if num_pagos_u > 10: num_pagos_u = 10

        st.write("Ingresa el mes de desembolso y el monto de cada pago:")
        pagos_u_data = []
        p_cols = st.columns(min(int(num_pagos_u), 4))
        
        default_meses_u = [1.0, 3.0, 4.0, 6.0, 8.0, 10.0, 12.0, 15.0, 18.0, 24.0]
        default_montos_u = [5000000.0, 7000000.0, 12000000.0, 10000000.0, 8000000.0, 5000000.0, 10000000.0, 12000000.0, 15000000.0, 20000000.0]

        vp_total_u = 0.0
        for idx in range(int(num_pagos_u)):
            col_target = p_cols[idx % 4]
            with col_target:
                mes_u = smart_num_input(f"Mes Pago #{idx+1}:", default_meses_u[idx % len(default_meses_u)], key=f"calc7_m_{idx}")
                monto_u = smart_num_input(f"Monto Pago #{idx+1} ($):", default_montos_u[idx % len(default_montos_u)], key=f"calc7_v_{idx}")
                st.markdown(f'<div class="val-badge">Mes {int(mes_u)}: ${fmt_m(monto_u)}</div>', unsafe_allow_html=True)
                
                vp_ind = monto_u / ((1 + tasa_univ) ** mes_u)
                vp_total_u += vp_ind
                pagos_u_data.append({
                    "Pago #": idx + 1,
                    "Mes Desembolso": int(mes_u),
                    "Monto Futuro ($)": fmt_m(monto_u),
                    "Valor Presente Hoy ($)": fmt_m(vp_ind)
                })

        st.markdown("### 🎯 Resultados del Fondo Requerido:")
        st.metric("Capital Inicial Necesario Hoy (VP Total)", f"${fmt_m(vp_total_u)}")
        st.success(f"✅ Debe disponer u ahorrar hoy **${fmt_m(vp_total_u)}** para cubrir exactamente todos los pagos programados.")
        
        df_p_u = pd.DataFrame(pagos_u_data)
        st.dataframe(df_p_u, hide_index=True)
        export_dataframe_button(df_p_u, "tabla_vp_pagos_discretos")

    # -------------------------------------------------------------
    # HERRAMIENTA VIII: VF DE DEPÓSITOS PROYECTADOS CON TASAS VARIABLES
    # -------------------------------------------------------------
    elif calc_option.startswith("VIII. "):
        st.subheader("🛠️ VIII. Valor Futuro (VF) de Depósitos Proyectados Discretos en Meses Específicos (Tasas Variables)")
        st.caption("Permite definir depósitos en meses específicos y configurar tasas de interés variables por tramo o por mes.")
        
        v1, v2, v3 = st.columns(3)
        with v1:
            horizonte_v = int(smart_num_input("Horizonte Total de Inversión (Meses):", 12.0, key="calc8_horiz"))
            st.markdown(f'<div class="val-badge">⏳ Horizonte: {horizonte_v} meses</div>', unsafe_allow_html=True)
        with v2:
            num_deps_v = int(smart_num_input("Cantidad de Depósitos a Realizar:", 4.0, key="calc8_num_deps"))
            if num_deps_v < 1: num_deps_v = 1
            if num_deps_v > 12: num_deps_v = 12
        with v3:
            momento_dep = st.selectbox(
                "Momento del Depósito en el Mes:",
                ["Fin del Mes / Vencido (por defecto)", "Inicio del Mes / Anticipado"],
                key="calc8_momento"
            )

        st.markdown("#### 📈 Configuración de Tasas de Interés por Período:")
        modo_tasa = st.radio(
            "Modalidad de Tasas de Interés:",
            ["Tasa Fija Mensual", "Cambio de Tasa desde un Mes Específico", "Matriz / Tabla de Tasa Específica por Mes"],
            horizontal=True,
            key="calc8_modo_tasa"
        )

        tasas_mes = [0.03] * horizonte_v

        if modo_tasa == "Tasa Fija Mensual":
            t_fija = smart_num_input("Tasa de Interés Mensual (%):", 3.0, key="calc8_tfija") / 100.0
            tasas_mes = [t_fija] * horizonte_v

        elif modo_tasa == "Cambio de Tasa desde un Mes Específico":
            tc1, tc2, tc3 = st.columns(3)
            with tc1:
                t_ini = smart_num_input("Tasa Inicial (% Mensual):", 3.0, key="calc8_tini") / 100.0
            with tc2:
                mes_cambio = int(smart_num_input("Mes de Cambio de Tasa (Ej. Mes 6 o 7):", 7.0, key="calc8_mcambio"))
            with tc3:
                t_nueva = smart_num_input("Nueva Tasa (% Mensual):", 4.0, key="calc8_tnueva") / 100.0
                
            for m_idx in range(1, horizonte_v + 1):
                if m_idx < mes_cambio:
                    tasas_mes[m_idx - 1] = t_ini
                else:
                    tasas_mes[m_idx - 1] = t_nueva

        else:
            st.write("Ingresa la tasa de interés mensual específica para cada mes:")
            t_cols = st.columns(min(horizonte_v, 6))
            for m_idx in range(1, horizonte_v + 1):
                col_t = t_cols[(m_idx - 1) % 6]
                with col_t:
                    default_t_val = 3.0 if m_idx <= 6 else 4.0
                    t_m_input = smart_num_input(f"Tasa Mes {m_idx} (%):", default_t_val, key=f"calc8_tm_{m_idx}") / 100.0
                    tasas_mes[m_idx - 1] = t_m_input

        st.markdown("#### 💵 Ingreso de Depósitos por Mes:")
        default_meses_v = [1, 2, 3, 4, 8, 5, 6, 7, 9, 10, 11, 12]
        default_montos_v = [30000000.0, 40000000.0, 50000000.0, 50000000.0, 40000000.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        
        depositos_dict = {}
        d_cols = st.columns(min(int(num_deps_v), 4))
        for idx in range(int(num_deps_v)):
            col_d = d_cols[idx % 4]
            with col_d:
                m_dep = int(smart_num_input(f"Mes Depósito #{idx+1}:", default_meses_v[idx % len(default_meses_v)], key=f"calc8_md_{idx}"))
                v_dep = smart_num_input(f"Monto Depósito #{idx+1} ($):", default_montos_v[idx % len(default_montos_v)], key=f"calc8_vd_{idx}")
                st.markdown(f'<div class="val-badge">Mes {m_dep}: ${fmt_m(v_dep)}</div>', unsafe_allow_html=True)
                depositos_dict[m_dep] = depositos_dict.get(m_dep, 0.0) + v_dep

        # Simulación Mes a Mes
        saldo = 0.0
        evolucion_meses = []
        total_depositado = sum(depositos_dict.values())
        
        is_anticipado = "Anticipado" in momento_dep

        for m_idx in range(1, horizonte_v + 1):
            tasa_m = tasas_mes[m_idx - 1]
            dep_m = depositos_dict.get(m_idx, 0.0)
            
            saldo_inicial_m = saldo
            if is_anticipado:
                base_interes = saldo_inicial_m + dep_m
                interes_m = base_interes * tasa_m
                saldo_final_m = base_interes + interes_m
            else:
                interes_m = saldo_inicial_m * tasa_m
                saldo_final_m = saldo_inicial_m + interes_m + dep_m
                
            evolucion_meses.append({
                "Mes": f"Mes {m_idx}",
                "Saldo Inicial ($)": fmt_m(saldo_inicial_m),
                "Depósito Ingresado ($)": fmt_m(dep_m),
                "Tasa Aplicada (%)": f"{fmt_n(tasa_m*100, 2)}%",
                "Interés del Mes ($)": fmt_m(interes_m),
                "Saldo Final ($)": fmt_m(saldo_final_m)
            })
            saldo = saldo_final_m

        # Cálculo de VF Individual de cada depósito
        desglose_indiv = []
        suma_vf_indiv = 0.0
        dep_idx_count = 1
        
        for m_dep, v_dep in sorted(depositos_dict.items()):
            if v_dep > 0:
                if is_anticipado:
                    m_cap = horizonte_v - m_dep + 1
                    tasa_indices = range(m_dep - 1, horizonte_v)
                else:
                    m_cap = horizonte_v - m_dep
                    tasa_indices = range(m_dep, horizonte_v)
                    
                factor_acum = 1.0
                for idx_t in tasa_indices:
                    factor_acum *= (1.0 + tasas_mes[idx_t])
                    
                vf_indiv = v_dep * factor_acum
                suma_vf_indiv += vf_indiv
                
                desglose_indiv.append({
                    "Abono #": dep_idx_count,
                    "Mes del Depósito": f"Mes {m_dep}",
                    "Monto Depositado ($)": fmt_m(v_dep),
                    "Meses Capitalizados": m_cap,
                    "Tasa Acumulada Efectiva (%)": f"{fmt_n((factor_acum - 1.0)*100, 2)}%",
                    "Valor Futuro del Depósito ($)": fmt_m(vf_indiv),
                    "Raw_VF": vf_indiv
                })
                dep_idx_count += 1

        df_indiv = pd.DataFrame(desglose_indiv)
        if not df_indiv.empty and saldo > 0:
            df_indiv["Participación en VF Final (%)"] = df_indiv["Raw_VF"].apply(lambda x: f"{fmt_n((x / saldo)*100, 2)}%")
            df_indiv_show = df_indiv.drop(columns=["Raw_VF"])
        else:
            df_indiv_show = df_indiv

        st.markdown("### 🎯 Resultados Consolidados:")
        c_v1, c_v2, c_v3 = st.columns(3)
        c_v1.metric("Valor Futuro Total Acumulado (t=12)", f"${fmt_m(saldo)}")
        c_v2.metric("Total Capital Depositado", f"${fmt_m(total_depositado)}")
        c_v3.metric("Total Intereses Ganados", f"${fmt_m(saldo - total_depositado)}")

        st.markdown("#### 📌 1. Desglose del Valor Futuro Individual de Cada Depósito:")
        st.dataframe(df_indiv_show, hide_index=True)
        export_dataframe_button(df_indiv_show, "tabla_vf_individual_depositos")

        st.markdown("#### 📊 2. Evolución Mensual Detallada del Fondo:")
        df_evol = pd.DataFrame(evolucion_meses)
        st.dataframe(df_evol, hide_index=True)
        export_dataframe_button(df_evol, "tabla_evolucion_fondo_meses")

    # -------------------------------------------------------------
    # HERRAMIENTA IX: COMPARADOR BANCARIO CON MÚLTIPLES TIPOS DE TASAS
    # -------------------------------------------------------------
    elif calc_option.startswith("IX. "):
        st.subheader("🛠️ IX. Comparador de Ofertas Bancarias a Plazo Fijo / Depósitos (Múltiples Bancos y Tipos de Tasa)")
        st.caption("Compara múltiples ofertas bancarias con diferentes denominaciones y estructuras de tasa. Convierte automáticamente a TEA y Tasa Mensual Equivalente.")
        
        b1, b2 = st.columns(2)
        with b1:
            monto_inv_comp = smart_num_input("Monto de Inversión Inicial ($):", 17000000.0, key="calc9_monto")
            st.markdown(f'<div class="val-badge">💵 Inversión: ${fmt_m(monto_inv_comp)}</div>', unsafe_allow_html=True)
        with b2:
            plazo_meses_comp = int(smart_num_input("Plazo de Inversión (Meses):", 24.0, key="calc9_plazo"))
            st.markdown(f'<div class="val-badge">⏳ Plazo: {plazo_meses_comp} meses ({fmt_n(plazo_meses_comp/12, 2)} años)</div>', unsafe_allow_html=True)
            
        num_bancos = int(smart_num_input("Cantidad de Bancos a Comparar (2 a 5):", 3.0, key="calc9_num_bancos"))
        if num_bancos < 2: num_bancos = 2
        if num_bancos > 5: num_bancos = 5
        
        st.write("Configura la tasa de interés ofrecida por cada entidad:")
        
        opciones_tasas = [
            "TEA (Efectiva Anual)",
            "TEC (Efectiva Cuatrimestral)",
            "TES (Efectiva Semestral)",
            "TET (Efectiva Trimestral)",
            "TEB (Efectiva Bimestral)",
            "TEM (Efectiva Mensual)",
            "TED (Efectiva Diaria)",
            "TNC (Nominal Cuatrimestral - Cap. Mensual m=4)",
            "TNC (Nominal Cuatrimestral - Cap. Diaria m=120)",
            "TNS (Nominal Semestral - Cap. Mensual m=6)",
            "TNT (Nominal Trimestral - Cap. Mensual m=3)",
            "TNA (Nominal Anual)",
            "Tasa Simple Anual",
            "Tasa Simple Cuatrimestral",
            "Tasa Simple Semestral",
            "Tasa Simple Trimestral",
            "Tasa Simple Mensual"
        ]
        
        bancos_res = []
        b_cols = st.columns(min(int(num_bancos), 3))
        
        for idx in range(int(num_bancos)):
            col_b = b_cols[idx % 3]
            with col_b:
                nombre_b = st.text_input(f"Nombre del Banco #{idx+1}:", value="", key=f"calc9_bname_{idx}", help="Escribe el nombre de la entidad (ej. Banco de Chile, Banco Estado, Santander)")
                if not nombre_b.strip():
                    nombre_b = f"Banco {idx+1}"
                    
                default_rate_val = 12.50 if idx == 0 else (4.10 if idx == 1 else 1.00)
                default_tipo = "TEA (Efectiva Anual)" if idx == 0 else ("TEC (Efectiva Cuatrimestral)" if idx == 1 else "TEM (Efectiva Mensual)")
                
                t_val_in = smart_num_input(f"Tasa Ingresada para {nombre_b} (%):", default_rate_val, key=f"calc9_trate_{idx}")
                st.markdown(f'<div class="val-badge">{fmt_n(t_val_in, 2)}%</div>', unsafe_allow_html=True)
                
                tipo_tasa_sel = st.selectbox(f"Tipo de Tasa ({nombre_b}):", opciones_tasas, index=opciones_tasas.index(default_tipo) if default_tipo in opciones_tasas else 0, key=f"calc9_ttype_{idx}")
                
                m_cap_custom = 12
                if tipo_tasa_sel == "TNA (Nominal Anual)":
                    m_cap_custom = int(smart_num_input(f"Cap. por año (m) para {nombre_b}:", 4.0, key="calc9_mcap_{idx}"))
                
                # Conversión a TEA y Tasa Mensual Equivalente (TEM)
                i_dec = t_val_in / 100.0
                
                if tipo_tasa_sel == "TEA (Efectiva Anual)":
                    tea_calc = i_dec
                elif tipo_tasa_sel == "TEC (Efectiva Cuatrimestral)":
                    tea_calc = ((1.0 + i_dec) ** 3.0) - 1.0
                elif tipo_tasa_sel == "TES (Efectiva Semestral)":
                    tea_calc = ((1.0 + i_dec) ** 2.0) - 1.0
                elif tipo_tasa_sel == "TET (Efectiva Trimestral)":
                    tea_calc = ((1.0 + i_dec) ** 4.0) - 1.0
                elif tipo_tasa_sel == "TEB (Efectiva Bimestral)":
                    tea_calc = ((1.0 + i_dec) ** 6.0) - 1.0
                elif tipo_tasa_sel == "TEM (Efectiva Mensual)":
                    tea_calc = ((1.0 + i_dec) ** 12.0) - 1.0
                elif tipo_tasa_sel == "TED (Efectiva Diaria)":
                    tea_calc = ((1.0 + i_dec) ** 360.0) - 1.0
                elif tipo_tasa_sel == "TNC (Nominal Cuatrimestral - Cap. Mensual m=4)":
                    i_m = i_dec / 4.0
                    tea_calc = ((1.0 + i_m) ** 12.0) - 1.0
                elif tipo_tasa_sel == "TNC (Nominal Cuatrimestral - Cap. Diaria m=120)":
                    i_d = i_dec / 120.0
                    tea_calc = ((1.0 + i_d) ** 360.0) - 1.0
                elif tipo_tasa_sel == "TNS (Nominal Semestral - Cap. Mensual m=6)":
                    i_m = i_dec / 6.0
                    tea_calc = ((1.0 + i_m) ** 12.0) - 1.0
                elif tipo_tasa_sel == "TNT (Nominal Trimestral - Cap. Mensual m=3)":
                    i_m = i_dec / 3.0
                    tea_calc = ((1.0 + i_m) ** 12.0) - 1.0
                elif tipo_tasa_sel == "TNA (Nominal Anual)":
                    tea_calc = ((1.0 + (i_dec / m_cap_custom)) ** m_cap_custom) - 1.0
                elif tipo_tasa_sel == "Tasa Simple Anual":
                    vf_simple = monto_inv_comp * (1.0 + i_dec * (plazo_meses_comp / 12.0))
                    tea_calc = ((vf_simple / monto_inv_comp) ** (12.0 / plazo_meses_comp)) - 1.0
                elif tipo_tasa_sel == "Tasa Simple Cuatrimestral":
                    vf_simple = monto_inv_comp * (1.0 + i_dec * (plazo_meses_comp / 4.0))
                    tea_calc = ((vf_simple / monto_inv_comp) ** (12.0 / plazo_meses_comp)) - 1.0
                elif tipo_tasa_sel == "Tasa Simple Semestral":
                    vf_simple = monto_inv_comp * (1.0 + i_dec * (plazo_meses_comp / 2.0))
                    tea_calc = ((vf_simple / monto_inv_comp) ** (12.0 / plazo_meses_comp)) - 1.0
                elif tipo_tasa_sel == "Tasa Simple Trimestral":
                    vf_simple = monto_inv_comp * (1.0 + i_dec * (plazo_meses_comp / 3.0))
                    tea_calc = ((vf_simple / monto_inv_comp) ** (12.0 / plazo_meses_comp)) - 1.0
                else: # Tasa Simple Mensual
                    vf_simple = monto_inv_comp * (1.0 + i_dec * plazo_meses_comp)
                    tea_calc = ((vf_simple / monto_inv_comp) ** (12.0 / plazo_meses_comp)) - 1.0

                # Tasa Mensual Equivalente (TEM)
                tem_calc = ((1.0 + tea_calc) ** (1.0 / 12.0)) - 1.0
                
                # Monto Final Acumulado e Intereses
                monto_final = monto_inv_comp * ((1.0 + tea_calc) ** (plazo_meses_comp / 12.0))
                intereses_ganados = monto_final - monto_inv_comp
                
                bancos_res.append({
                    "Entidad Bancaria": nombre_b,
                    "Tasa Ofrecida": f"{fmt_n(t_val_in, 2)}% ({tipo_tasa_sel.split('(')[0].strip()})",
                    "TEA Equivalente (%)": fmt_n(tea_calc * 100, 4),
                    "Tasa Mensual Equivalente (%)": fmt_n(tem_calc * 100, 4),
                    "Monto Final Acumulado ($)": fmt_m(monto_final),
                    "Intereses Ganados ($)": fmt_m(intereses_ganados),
                    "Raw_Int": intereses_ganados,
                    "Raw_TEA": tea_calc
                })

        # Ordenar por rentabilidad descendente
        bancos_res.sort(key=lambda x: x["Raw_Int"], reverse=True)
        
        best_bank = bancos_res[0]
        second_best = bancos_res[1] if len(bancos_res) > 1 else best_bank
        diff_best = best_bank["Raw_Int"] - second_best["Raw_Int"]
        spread_best_bps = (best_bank["Raw_TEA"] - second_best["Raw_TEA"]) * 10000.0

        st.markdown("### 🏆 Ranking de Rentabilidad Bancaria:")
        st.success(
            f"✅ **Oferta Ganadora:** **{best_bank['Entidad Bancaria']}** con un Interés Ganado Total de **${best_bank['Intereses Ganados ($)']}** "
            f"(TEA: **{best_bank['TEA Equivalente (%)']}%** | Tasa Mensual: **{best_bank['Tasa Mensual Equivalente (%)']}%**).\n\n"
            f"📈 **Ventaja Financiera:** Genera **${fmt_m(diff_best)}** adicionales ({fmt_n(spread_best_bps, 0)} bps superiores) respecto a la segunda mejor opción ({second_best['Entidad Bancaria']})."
        )

        for b_entry in bancos_res:
            diff_curr = best_bank["Raw_Int"] - b_entry["Raw_Int"]
            b_entry["Diferencia vs. Mejor ($)"] = "🥇 Mejor Oferta" if diff_curr == 0 else f"-${fmt_m(diff_curr)}"

        df_bancos_show = pd.DataFrame(bancos_res).drop(columns=["Raw_Int", "Raw_TEA"])
        st.dataframe(df_bancos_show, hide_index=True)
        export_dataframe_button(df_bancos_show, "comparativa_ofertas_bancarias")

    # -------------------------------------------------------------
    # HERRAMIENTA X: CRÉDITO COMERCIAL / CAMIONETA
    # -------------------------------------------------------------
    elif calc_option.startswith("X. "):
        st.subheader("🛠️ X. Calculadora de Crédito Comercial / Bienes de Capital (Pagos Anuales & Cuota Mensual)")
        st.caption("Especializada en créditos comerciales o leasing vehicular pagados en cuotas anuales con tasas semestrales u otras periodicidades.")
        
        cam1, cam2, cam3 = st.columns(3)
        with cam1:
            monto_cam = smart_num_input("Valor Comercial / Préstamo ($):", 12000000.0, key="calc10_monto")
            st.markdown(f'<div class="val-badge">💵 Valor: ${fmt_m(monto_cam)}</div>', unsafe_allow_html=True)
        with cam2:
            plazo_meses_cam = int(smart_num_input("Plazo Total en Meses:", 36.0, key="calc10_plazo"))
            st.markdown(f'<div class="val-badge">⏳ Plazo: {plazo_meses_cam} meses</div>', unsafe_allow_html=True)
        with cam3:
            tasa_sem_cam = smart_num_input("Tasa Semestral (%):", 7.40, key="calc10_tasa") / 100.0
            st.markdown(f'<div class="val-badge">📈 Tasa Semestral: {fmt_n(tasa_sem_cam*100, 2)}%</div>', unsafe_allow_html=True)

        tea_cam = ((1 + tasa_sem_cam) ** 2) - 1.0
        n_anos_cam = int(round(plazo_meses_cam / 12.0))
        if n_anos_cam < 1: n_anos_cam = 1
        
        cuota_anual_cam = monto_cam * (tea_cam / (1 - (1 + tea_cam)**(-n_anos_cam)))
        i_mensual_cam = ((1 + tea_cam) ** (1.0 / 12.0)) - 1.0
        cuota_mensual_eq = monto_cam * (i_mensual_cam / (1 - (1 + i_mensual_cam)**(-plazo_meses_cam)))

        total_pagado_cam = cuota_anual_cam * n_anos_cam
        intereses_totales_cam = total_pagado_cam - monto_cam

        m_cam1, m_cam2, m_cam3, m_cam4 = st.columns(4)
        m_cam1.metric("Cuota Anual ($)", f"${fmt_m(cuota_anual_cam)}")
        m_cam2.metric("Cuota Mensual Equivalente ($)", f"${fmt_m(cuota_mensual_eq)}")
        m_cam3.metric("TEA Equivalente", f"{fmt_n(tea_cam*100, 4)}%")
        m_cam4.metric("Intereses Totales Crédito", f"${fmt_m(intereses_totales_cam)}")

        st.success(f"✅ Al final de los {n_anos_cam} años del crédito, pagará **${fmt_m(intereses_totales_cam)}** sólo por concepto de intereses.")

        saldo_cam = monto_cam
        tabla_cam_data = []
        for ano in range(1, n_anos_cam + 1):
            int_ano = saldo_cam * tea_cam
            amort_ano = cuota_anual_cam - int_ano
            saldo_next_cam = max(0.0, saldo_cam - amort_ano)
            tabla_cam_data.append({
                "Periodo (Año)": f"Año {ano}",
                "Cuota ($)": fmt_m(cuota_anual_cam),
                "Amortización ($)": fmt_m(amort_ano),
                "Interés ($)": fmt_m(int_ano),
                "Saldo Final ($)": fmt_m(saldo_next_cam)
            })
            saldo_cam = saldo_next_cam

        df_tabla_cam = pd.DataFrame(tabla_cam_data)
        st.markdown("#### 📊 Tabla de Desarrollo del Crédito Comercial (Anual):")
        st.dataframe(df_tabla_cam, hide_index=True)
        export_dataframe_button(df_tabla_cam, "tabla_desarrollo_credito_comercial")

    # -------------------------------------------------------------
    # HERRAMIENTA XI: TASA IMPLÍCITA PAGO ÚNICO
    # -------------------------------------------------------------
    elif calc_option.startswith("XI. "):
        st.subheader("🛠️ XI. Tasa Implícita Anual para Créditos o Inversiones de Pago Único")
        
        imp1, imp2, imp3 = st.columns(3)
        with imp1:
            vp_imp = smart_num_input("Monto Inicial / Préstamo ($):", 5000000.0, key="calc11_vp")
            st.markdown(f'<div class="val-badge">💵 Préstamo Inicial: ${fmt_m(vp_imp)}</div>', unsafe_allow_html=True)
        with imp2:
            vf_imp = smart_num_input("Monto Único Pagado al Final ($):", 8000000.0, key="calc11_vf")
            st.markdown(f'<div class="val-badge">💵 Pago Único: ${fmt_m(vf_imp)}</div>', unsafe_allow_html=True)
        with imp3:
            plazo_imp_num = smart_num_input("Plazo Total de la Operación:", 12.0, key="calc11_plazo")
            unidad_imp = st.selectbox("Unidad del Plazo:", ["Trimestres", "Meses", "Años", "Semestres", "Cuatrimestres"], key="calc11_unit")

        if unidad_imp == "Trimestres":
            anos_imp = plazo_imp_num / 4.0
            per_por_ano = 4.0
        elif unidad_imp == "Meses":
            anos_imp = plazo_imp_num / 12.0
            per_por_ano = 12.0
        elif unidad_imp == "Años":
            anos_imp = plazo_imp_num
            per_por_ano = 1.0
        elif unidad_imp == "Semestres":
            anos_imp = plazo_imp_num / 2.0
            per_por_ano = 2.0
        else:
            anos_imp = plazo_imp_num / 3.0
            per_por_ano = 3.0

        if vf_imp > vp_imp and anos_imp > 0:
            tea_imp = ((vf_imp / vp_imp) ** (1.0 / anos_imp)) - 1.0
            i_trimestral = ((1 + tea_imp) ** (1.0 / 4.0)) - 1.0
            i_periodica = ((1 + tea_imp) ** (1.0 / per_por_ano)) - 1.0
            tna_imp = i_periodica * per_por_ano

            m_imp1, m_imp2, m_imp3, m_imp4 = st.columns(4)
            m_imp1.metric("Tasa Efectiva Anual (TEA)", f"{fmt_n(tea_imp*100, 4)}%")
            m_imp2.metric("Tasa Trimestral Equivalente", f"{fmt_n(i_trimestral*100, 4)}%")
            m_imp3.metric(f"Tasa Periódica ({unidad_imp[:-1] if unidad_imp.endswith('s') else unidad_imp})", f"{fmt_n(i_periodica*100, 4)}%")
            m_imp4.metric("Tasa Nominal Anual (TNA)", f"{fmt_n(tna_imp*100, 4)}%")

            st.info(f"Fórmula aplicada por el sistema: $TEA = ({fmt_m(vf_imp)} / {fmt_m(vp_imp)})^{{1 / {fmt_n(anos_imp, 2)}}} - 1 = {fmt_n(tea_imp*100, 4)}\\%$")
        else:
            st.error("El Valor Pagado (VF) debe ser superior al Préstamo Inicial (VP).")

    # -------------------------------------------------------------
    # HERRAMIENTA XII: VALOR PRESENTE CON 4 DECIMALES
    # -------------------------------------------------------------
    else:
        st.subheader("🛠️ XII. Valor Presente de Cero / Descuento (4 Decimales de Precisión)")
        st.caption("Calcula el Valor Presente exacto con precisión matemática de 4 decimales (utilizando coma como separador decimal).")
        
        dp1, dp2, dp3 = st.columns(3)
        with dp1:
            vf_p = smart_num_input("Valor Único Futuro / Pago ($):", 3545900.0, key="calc12_vf")
            st.markdown(f'<div class="val-badge">💵 Pago Futuro: ${fmt_m(vf_p)}</div>', unsafe_allow_html=True)
        with dp2:
            meses_p = smart_num_input("Plazo Total en Meses:", 24.0, key="calc12_meses")
            st.markdown(f'<div class="val-badge">⏳ Plazo: {meses_p} meses</div>', unsafe_allow_html=True)
        with dp3:
            tasa_p_anual = smart_num_input("Tasa Efectiva Anual (%):", 14.80, key="calc12_tasa") / 100.0
            st.markdown(f'<div class="val-badge">📈 TEA: {fmt_n(tasa_p_anual*100, 2)}%</div>', unsafe_allow_html=True)
            
        anos_p = meses_p / 12.0
        vp_exact = vf_p / ((1 + tasa_p_anual) ** anos_p)
        formatted_exact_4 = fmt_n(vp_exact, 4)
        
        st.markdown("### 🎯 Valor Presente Exacto con 4 Decimales:")
        st.success(f"**{formatted_exact_4}**")
        st.info(f"Fórmula de cálculo: $VP = \\frac{{{fmt_m(vf_p)}}}{{(1 + {fmt_n(tasa_p_anual*100, 2)}\\%)^{{({fmt_n(meses_p, 0)}/12)}}}} = {formatted_exact_4}$")

st.markdown("---")
st.caption("Plataforma de Simulación & Cálculo Financiero — Generado para Gemini Notebook")
