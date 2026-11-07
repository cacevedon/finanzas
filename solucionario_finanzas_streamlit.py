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

# Helper para exportar cualquier DataFrame a un archivo Excel (.xlsx)
def to_excel(df, sheet_name="Tabla_Desarrollo"):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name=sheet_name)
    return output.getvalue()

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
    
    st.markdown("---")
    st.subheader("📝 Evaluación de Escenarios Complejos de Interés")
    
    prob_sel = st.selectbox("Selecciona un Caso Práctico de Estudio:", [
        "Caso 1: Evaluación de Fondo de $25.000.000 a 5 Años (Simple 0,8% vs Compuesto 0,75%)",
        "Caso 2: Inversión de $75.000.000 dividida en dos depósitos",
        "Caso 3: Sistema de Ecuaciones — Inversión de $980.000.000 para ganar $5.500.000 mensuales",
        "Caso 4: Igualación de Flujos — Deuda de $70M al 3,5% vs Inversión de $50M al 7,0%"
    ])
    
    if "Caso 1:" in prob_sel:
        vf_mat_a = 25000000 * (1 + 0.008 * 60)
        vf_mat_b = 25000000 * ((1 + 0.0075) ** 60)
        st.write(f"• **Opción A (Simple 0,8%):** $VF = $25.000.000 \\times (1 + 0,008 \\times 60) =$ **${fmt_m(vf_mat_a)}**")
        st.write(f"• **Opción B (Compuesto 0,75%):** $VF = $25.000.000 \\times (1 + 0,0075)^{{60}} =$ **${fmt_m(vf_mat_b)}**")
        st.success(f"✅ **Conclusión:** Conviene la **Opción B (Interés Compuesto)** por una diferencia a favor de **${fmt_m(vf_mat_b - vf_mat_a)}** gracias a la reinversión de intereses.")
        
    elif "Caso 2:" in prob_sel:
        m_tot = 75000000
        p1 = m_tot * 0.40
        p2 = m_tot * 0.60
        vf1 = p1 * ((1 + 0.012) ** 24)
        vf2 = p2 * (1 + 0.015 * 24)
        vf_tot = vf1 + vf2
        st.write(f"• **Depósito 1 (40% = ${fmt_m(p1)} al 1,2% compuesto por 24 meses):** $VF_1 =$ **${fmt_m(vf1)}**")
        st.write(f"• **Depósito 2 (60% = ${fmt_m(p2)} al 1,5% simple por 24 meses):** $VF_2 =$ **${fmt_m(vf2)}**")
        st.success(f"✅ **Monto Total Acumulado a los 2 años:** **${fmt_m(vf_tot)}**")

    elif "Caso 3:" in prob_sel:
        st.markdown(f"""
        - **Banco A:** 5,04% anual simple $\\Rightarrow i_A = 5,04% / 12 = 0,42%$ mensual.
        - **Banco B:** 2,10% trimestral simple $\\Rightarrow i_B = 2,10% / 3 = 0,70%$ mensual.
        - **Ecuaciones de Sistema:**
          1) $X + Y = {fmt_m(980000000)}$
          2) $0,0042 X + 0,0070 Y = {fmt_m(5500000)}$
        """)
        y_val = (5500000 - 0.0042 * 980000000) / (0.0070 - 0.0042)
        x_val = 980000000 - y_val
        st.success(f"✅ **Inversión en Banco A (X):** **${fmt_m(x_val)}** | **Inversión en Banco B (Y):** **${fmt_m(y_val)}**")

    elif "Caso 4:" in prob_sel:
        n_eq = math.log(70000000 / 50000000) / math.log(1.07 / 1.035)
        st.write(f"• **Ecuación:** $50M \\times (1,07)^n = 70M \\times (1,035)^n \\Rightarrow n = {fmt_n(n_eq, 2)}$ meses")
        st.success(f"✅ **Tiempo de Igualación de Flujos:** **{fmt_n(n_eq, 2)} meses** ({fmt_n(n_eq/12, 2)} años).")

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
            "Saldo Final ($)": fmt_m(saldo_final),
            "Raw_Interes": interes_mes,
            "Raw_Amort": capital_mes
        })
        saldo = saldo_final
        
    df_amort = pd.DataFrame(amort_data)
    
    st.markdown("#### Tabla de Amortización Dinámica")
    df_export_m4 = df_amort.drop(columns=["Raw_Interes", "Raw_Amort"])
    st.dataframe(df_export_m4, height=280)
    
    # Botón de exportación a Excel para Módulo 4
    excel_m4 = to_excel(df_export_m4, sheet_name="Amortizacion_Modulo_4")
    st.download_button(
        label="📥 Exportar Tabla de Amortización a Excel (.xlsx)",
        data=excel_m4,
        file_name="tabla_amortizacion_modulo4.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    
    chart_df = pd.DataFrame({
        "Mes": [d["Mes"] for d in amort_data],
        "Interés ($)": [d["Raw_Interes"] for d in amort_data],
        "Amortización ($)": [d["Raw_Amort"] for d in amort_data]
    }).set_index("Mes")
    
    st.markdown("#### Descomposición de la Cuota: Interés vs. Amortización")
    st.bar_chart(chart_df)

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
    
    st.markdown("---")
    st.subheader("🏗️ Caso Proyecto Planta de Desalinización")
    st.markdown(f"""
    - **Inversión Inicial / Construcción:** 4 años de diferimiento.
    - **Flujo en Año 5:** ${fmt_m(800000)} con crecimiento perpetuo al $g = 5,00%$ anual.
    - **Tasa de Descuento (TMAR):** 12,00% anual.
    """)
    vp_perpetuidad_4 = 800000 / (0.12 - 0.05)
    vp_hoy_0 = vp_perpetuidad_4 / ((1 + 0.12)**4)
    
    st.write(f"• **Valor Presente en Año 4 ($VP_4$):** ${fmt_m(800000)} / (0,12 - 0,05) = **${fmt_m(vp_perpetuidad_4)}**")
    st.write(f"• **Valor Presente Hoy ($VP_0$):** ${fmt_m(vp_perpetuidad_4)} / (1,12)^4 = **${fmt_m(vp_hoy_0)}**")

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
            "Caja Acumulada ($)": fmt_m(caja_acum),
            "Raw_Ventas": ventas_m,
            "Raw_Egresos": egresos_total
        })
        
    df_pres = pd.DataFrame(p_data)
    
    df_pres["Mes"] = pd.Categorical(
        df_pres["Mes"], 
        categories=[f"Mes {i}" for i in range(1, meses_p + 1)], 
        ordered=True
    )
    
    df_export_m6 = df_pres.drop(columns=["Raw_Ventas", "Raw_Egresos"])
    st.dataframe(df_export_m6)
    
    # Botón de exportación a Excel para Módulo 6
    excel_m6 = to_excel(df_export_m6, sheet_name="Presupuesto_Modulo_6")
    st.download_button(
        label="📥 Exportar Presupuesto a Excel (.xlsx)",
        data=excel_m6,
        file_name="presupuesto_modulo6.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    
    chart_pres = pd.DataFrame({
        "Mes": df_pres["Mes"],
        "Ventas ($)": df_pres["Raw_Ventas"],
        "Total Egresos ($)": df_pres["Raw_Egresos"]
    }).set_index("Mes")
    
    st.bar_chart(chart_pres)

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
        
    st.markdown("---")
    st.subheader("💰 Evaluación de Flujos de Caja (VAN y TIR)")
    
    inv_ini = smart_num_input("Inversión Inicial ($):", 500000.0, key="m7_inv")
    st.markdown(f'<div class="val-badge">💵 Inversión: ${fmt_m(inv_ini)}</div>', unsafe_allow_html=True)
    tmar_val = smart_num_input("Tasa de Descuento / TMAR (%):", 10.0, key="m7_tmar") / 100.0
    st.markdown(f'<div class="val-badge">📈 TMAR: {fmt_n(tmar_val*100, 2)}%</div>', unsafe_allow_html=True)
    
    st.write("Flujos netos proyectados a 5 años:")
    fc_cols = st.columns(5)
    flujos = []
    for idx, col in enumerate(fc_cols):
        with col:
            f_val = smart_num_input(f"Año {idx+1} ($):", 140000.0 + idx*10000.0, key=f"m7_f_{idx}")
            st.markdown(f'<div class="val-badge">Año {idx+1}: ${fmt_m(f_val)}</div>', unsafe_allow_html=True)
            flujos.append(f_val)
            
    van_val = npf.npv(tmar_val, [0] + flujos) - inv_ini
    tir_val = npf.irr([-inv_ini] + flujos)
    
    col_v1, col_v2 = st.columns(2)
    col_v1.metric("Valor Actual Neto (VAN)", f"${fmt_m(van_val)}", delta="Viable" if van_val > 0 else "No Viable")
    col_v2.metric("Tasa Interna de Retorno (TIR)", f"{fmt_n(tir_val*100, 2)}%", delta="TIR > TMAR" if tir_val > tmar_val else "TIR < TMAR")

# ==========================================
# MÓDULO 8: CALCULADORAS ESPECIALIZADAS
# ==========================================
elif modulo == "8. Calculadoras Especializadas":
    st.header("Módulo 8: Calculadoras Especializadas")
    st.markdown("Suite avanzada de cálculo e ingeniería financiera de precisión. Todos los modelos se ejecutan automáticamente en el sistema y permiten exportar las tablas de desarrollo a Excel (.xlsx).")
    
    calc_option = st.selectbox(
        "Selecciona la Herramienta de Cálculo:",
        [
            "I. Desglose de Interés y Amortización para una Cuota Específica (k) con Convertidor de Tasas",
            "II. Valor Futuro con Interés Compuesto (Plazos Enteros y Fraccionados)",
            "III. Valor Futuro de Anualidades y Fondos de Ahorro (Ordinarias y Anticipadas)",
            "IV. Valuación de Flujos Múltiples e Irregulares (VP en t=0 y VF en t=N)",
            "V. Despeje de Plazo Requerido (n) y Tasa Implícita para Metas de Capital",
            "VI. Conversión Avanzada de Tasas Nominales/Efectivas y Spread Financiero",
            "VII. Valor Presente (VP) de Pagos Futuros Específicos Discretos en Meses (Ej. Colegiaturas Universitarias)",
            "VIII. Valor Futuro (VF) de Depósitos Proyectados Discretos en Meses Específicos (Ej. Ahorro para Viaje)",
            "IX. Comparador de Ofertas Bancarias a Plazo Fijo / Depósitos (TEA vs TEC / Intereses Ganados)",
            "X. Crédito Comercial / Bienes de Capital (Pagos Anuales, Cuota Mensual y Tabla de Desarrollo)",
            "XI. Tasa Implícita Anual para Créditos o Inversiones de Pago Único",
            "XII. Valor Presente de Cero / Descuento con Alta Precisión Decimal (4 Decimales)"
        ]
    )
    
    st.markdown("---")
    
    # -------------------------------------------------------------
    # HERRAMIENTA I: DESGLOSE DE CUOTA k CON CONVERTIDOR AUTOMÁTICO
    # -------------------------------------------------------------
    if "I. Desglose" in calc_option:
        st.subheader("🛠️ I. Desglose de Interés y Amortización (Cuota Específica k)")
        st.caption("Configura el préstamo y la periodicidad de la tasa entregada. El sistema homogeneizará automáticamente la tasa y calculará la cuota y la tabla completa.")
        
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
                "Periodo": period,
                "Saldo Inicial ($)": fmt_m(saldo_curr),
                "Cuota ($)": fmt_m(cuota_r),
                "Amortización ($)": fmt_m(amort_p),
                "Interés ($)": fmt_m(int_p),
                "Saldo Final ($)": fmt_m(saldo_next)
            })
            saldo_curr = saldo_next

        st.markdown("#### 📊 Parámetros Homogeneizados Automáticamente por el Sistema:")
        st.write(f"• **Tasa Periódica Ajustada por Cuota ($i_{{pago}}$):** **{fmt_n(i_cuota*100, 4)}%** (TEA Equivalente: {fmt_n(tea_base*100, 2)}%)")
        st.write(f"• **Cantidad Total de Cuotas ($n$):** **{n_cuotas} cuotas**")
        st.write(f"• **Valor Cuota Fija ($R$):** **${fmt_m(cuota_r)}**")
        
        st.markdown(f"#### 🎯 Desglose Específico para la Cuota $k = {k_eval}$:")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Saldo Inicial Cuota k", f"${fmt_m(k_saldo_prev)}")
        m2.metric("Interés de la Cuota k", f"${fmt_m(k_interes)}")
        m3.metric("Amortización Cuota k", f"${fmt_m(k_amort)}")
        m4.metric("Saldo Insoluto Final", f"${fmt_m(k_saldo_final)}")
        
        df_k_export = pd.DataFrame(amort_full)
        st.markdown("#### 📋 Tabla de Desarrollo Completa")
        st.dataframe(df_k_export)
        
        excel_k = to_excel(df_k_export, sheet_name="Tabla_Desarrollo_k")
        st.download_button(
            label="📥 Exportar Tabla de Desarrollo a Excel (.xlsx)",
            data=excel_k,
            file_name=f"tabla_desarrollo_cuota_{k_eval}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    # -------------------------------------------------------------
    # HERRAMIENTA II: VALOR FUTURO INTERÉS COMPUESTO
    # -------------------------------------------------------------
    elif "II. Valor Futuro" in calc_option:
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
        st.info(f"Fórmula aplicada por el sistema: $VF = {fmt_m(s1_vp)} \\times (1 + {fmt_n(s1_tasa*100, 2)}%)^{{({fmt_n(s1_meses, 0)}/12)}} = {fmt_m(s1_vf)}$")

    # -------------------------------------------------------------
    # HERRAMIENTA III: VF ANUALIDADES Y FONDOS DE AHORRO
    # -------------------------------------------------------------
    elif "III. Valor Futuro de Anualidades" in calc_option:
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
    # HERRAMIENTA IV: VALUACIÓN FLUJOS MÚLTIPLES (VP Y VF)
    # -------------------------------------------------------------
    elif "IV. Valuación" in calc_option:
        st.subheader("🛠️ IV. Valuación de Flujos Múltiples e Irregulares (VP en t=0 y VF en t=N)")
        
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
    elif "V. Despeje" in calc_option:
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
    elif "VI. Conversión" in calc_option:
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
    # HERRAMIENTA VII: VP PAGOS FUTUROS DISCRETOS EN MESES (UNIVERSIDAD)
    # -------------------------------------------------------------
    elif "VII. Valor Presente" in calc_option:
        st.subheader("🛠️ VII. Valor Presente (VP) de Pagos Futuros Discretos en Meses Específicos")
        st.caption("Determina la reserva o ahorro necesario hoy (t=0) para cubrir compromisos futuros en meses exactos.")
        
        u1, u2 = st.columns(2)
        with u1:
            tasa_u = smart_num_input("Tasa de Interés Mensual de la Inversión (%):", 2.50, key="u_tasa") / 100.0
            st.markdown(f'<div class="val-badge">📈 Tasa Mensual: {fmt_n(tasa_u*100, 2)}%</div>', unsafe_allow_html=True)
        with u2:
            num_pagos_u = int(smart_num_input("Número de Pagos Programados:", 3.0, key="u_num"))
            if num_pagos_u < 1: num_pagos_u = 1
            
        pagos_u = []
        p_cols = st.columns(min(num_pagos_u, 4))
        
        for idx in range(num_pagos_u):
            c_target = p_cols[idx % 4]
            with c_target:
                st.markdown(f"**Pago #{idx+1}:**")
                m_num = int(smart_num_input(f"Mes del Pago #{idx+1}:", float([1, 3, 4, 6, 12][idx % 5]), key=f"u_m_{idx}"))
                p_monto = smart_num_input(f"Monto Pago #{idx+1} ($):", float([5000000, 7000000, 12000000, 10000000][idx % 4]), key=f"u_p_{idx}")
                pagos_u.append({"mes": m_num, "monto": p_monto})
                
        vp_total_u = sum([p["monto"] / ((1 + tasa_u)**p["mes"]) for p in pagos_u])
        
        st.markdown("#### 🎯 Reserva Requerida Hoy (t=0):")
        st.metric("Fondo / Reserva que Debe Ahorrar Hoy (VP)", f"${fmt_m(vp_total_u)}")
        st.success(f"✅ Debe disponer u ahorrar hoy **${fmt_m(vp_total_u)}** para cubrir exactamente todos los pagos programados.")

    # -------------------------------------------------------------
    # HERRAMIENTA VIII: VF DEPÓSITOS DISCRETOS EN MESES (VIAJE)
    # -------------------------------------------------------------
    elif "VIII. Valor Futuro" in calc_option:
        st.subheader("🛠️ VIII. Valor Futuro (VF) de Depósitos Proyectados Discretos en Meses Específicos")
        st.caption("Calcula el capital total acumulado al horizonte fijado a partir de aportes en meses intermedios.")
        
        v1, v2, v3 = st.columns(3)
        with v1:
            tasa_v = smart_num_input("Tasa de Interés Mensual (%):", 3.0, key="v_tasa") / 100.0
            st.markdown(f'<div class="val-badge">📈 Tasa Mensual: {fmt_n(tasa_v*100, 2)}%</div>', unsafe_allow_html=True)
        with v2:
            horiz_v = int(smart_num_input("Horizonte Total de Evaluación (Meses):", 12.0, key="v_horiz"))
            st.markdown(f'<div class="val-badge">⏳ Horizonte: {horiz_v} meses</div>', unsafe_allow_html=True)
        with v3:
            num_dep_v = int(smart_num_input("Cantidad de Depósitos a Realizar:", 4.0, key="v_num"))
            if num_dep_v < 1: num_dep_v = 1
            
        deps_v = []
        d_cols = st.columns(min(num_dep_v, 4))
        for idx in range(num_dep_v):
            c_target = d_cols[idx % 4]
            with c_target:
                st.markdown(f"**Depósito #{idx+1}:**")
                m_dep = int(smart_num_input(f"Mes del Depósito #{idx+1}:", float([1, 2, 3, 4, 6][idx % 5]), key=f"v_m_{idx}"))
                val_dep = smart_num_input(f"Monto Depósito #{idx+1} ($):", float([30000000, 40000000, 50000000, 50000000][idx % 4]), key=f"v_val_{idx}")
                deps_v.append({"mes": m_dep, "monto": val_dep})
                
        vf_total_v = sum([d["monto"] * ((1 + tasa_v)**(horiz_v - d["mes"])) for d in deps_v if d["mes"] <= horiz_v])
        
        st.markdown(f"#### 🎯 Capital Acumulado al Mes {horiz_v}:")
        st.metric("Fondo Total Acumulado (VF)", f"${fmt_m(vf_total_v)}")
        st.success(f"✅ Al final del mes {horiz_v}, dispondrá de **${fmt_m(vf_total_v)}** para su viaje u objetivo.")

    # -------------------------------------------------------------
    # HERRAMIENTA IX: COMPARADOR OFERTAS BANCARIAS A PLAZO FIJO
    # -------------------------------------------------------------
    elif "IX. Comparador" in calc_option:
        st.subheader("🛠️ IX. Comparador de Ofertas Bancarias a Plazo Fijo / Depósitos")
        
        b1, b2, b3 = st.columns(3)
        with b1:
            monto_b = smart_num_input("Monto Inicial a Invertir ($):", 17000000.0, key="b_monto")
            st.markdown(f'<div class="val-badge">💵 Inversión: ${fmt_m(monto_b)}</div>', unsafe_allow_html=True)
        with b2:
            plazo_meses_b = int(smart_num_input("Plazo Total (Meses):", 24.0, key="b_plazo"))
            st.markdown(f'<div class="val-badge">⏳ Plazo: {plazo_meses_b} meses</div>', unsafe_allow_html=True)
        with b3:
            st.write("Configuración de Tasas:")
            
        b_c1, b_c2 = st.columns(2)
        with b_c1:
            st.markdown("**Banco 1:**")
            tasa_b1_val = smart_num_input("Tasa Banco 1 (%):", 12.50, key="b1_val") / 100.0
            tipo_b1 = st.selectbox("Tipo de Tasa Banco 1:", ["Efectiva Anual (TEA)", "Efectiva Mensual (TEM)", "Efectiva Cuatrimestral (TEC)"], key="b1_tipo")
            
            if "TEA" in tipo_b1: tea_b1 = tasa_b1_val
            elif "TEM" in tipo_b1: tea_b1 = ((1 + tasa_b1_val)**12) - 1.0
            else: tea_b1 = ((1 + tasa_b1_val)**3) - 1.0
            
            vf_b1 = monto_b * ((1 + tea_b1)**(plazo_meses_b / 12.0))
            int_b1 = vf_b1 - monto_b
            st.metric("Valor Futuro Banco 1", f"${fmt_m(vf_b1)}", delta=f"Intereses: ${fmt_m(int_b1)}")
            
        with b_c2:
            st.markdown("**Banco 2:**")
            tasa_b2_val = smart_num_input("Tasa Banco 2 (%):", 4.10, key="b2_val") / 100.0
            tipo_b2 = st.selectbox("Tipo de Tasa Banco 2:", ["Efectiva Cuatrimestral (TEC)", "Efectiva Anual (TEA)", "Efectiva Mensual (TEM)"], key="b2_tipo")
            
            if "TEC" in tipo_b2: tea_b2 = ((1 + tasa_b2_val)**3) - 1.0
            elif "TEA" in tipo_b2: tea_b2 = tasa_b2_val
            else: tea_b2 = ((1 + tasa_b2_val)**12) - 1.0
            
            vf_b2 = monto_b * ((1 + tea_b2)**(plazo_meses_b / 12.0))
            int_b2 = vf_b2 - monto_b
            st.metric("Valor Futuro Banco 2", f"${fmt_m(vf_b2)}", delta=f"Intereses: ${fmt_m(int_b2)}")
            
        diff_b = abs(int_b1 - int_b2)
        if int_b1 > int_b2:
            st.success(f"✅ **Ganará más intereses en el Banco 1** por una diferencia a favor de **${fmt_m(diff_b)}**.")
        else:
            st.success(f"✅ **Ganará más intereses en el Banco 2** por una diferencia a favor de **${fmt_m(diff_b)}**.")

    # -------------------------------------------------------------
    # HERRAMIENTA X: CRÉDITO COMERCIAL / BIENES DE CAPITAL (CAMIONETA)
    # -------------------------------------------------------------
    elif "X. Crédito Comercial" in calc_option:
        st.subheader("🛠️ X. Crédito Comercial / Bienes de Capital (Pagos Anuales & Cuota Mensual)")
        st.caption("Evalúa créditos comerciales con amortización periódica, entregando la cuota anual, la cuota mensual equivalente y la tabla de desarrollo completa con exportación a Excel.")
        
        cm1, cm2, cm3 = st.columns(3)
        with cm1:
            vp_cam = smart_num_input("Valor Comercial / Préstamo ($):", 12000000.0, key="cam_vp")
            st.markdown(f'<div class="val-badge">💵 Valor: ${fmt_m(vp_cam)}</div>', unsafe_allow_html=True)
            
            plazo_meses_cam = int(smart_num_input("Plazo Total en Meses:", 36.0, key="cam_meses"))
            st.markdown(f'<div class="val-badge">⏳ Plazo: {plazo_meses_cam} meses</div>', unsafe_allow_html=True)
            
        with cm2:
            tasa_sem_cam = smart_num_input("Tasa Semestral (%):", 7.40, key="cam_tasa_sem") / 100.0
            st.markdown(f'<div class="val-badge">📈 Tasa Semestral: {fmt_n(tasa_sem_cam*100, 2)}%</div>', unsafe_allow_html=True)
            
            pago_freq_cam = st.selectbox("Frecuencia Real de Pago:", ["Anual (1/año)", "Mensual (12/año)", "Semestral (2/año)"], key="cam_freq")
            
        with cm3:
            st.write("Parámetros del Financiamiento:")
            
        tea_cam = ((1 + tasa_sem_cam)**2) - 1.0
        n_anos_cam = int(round(plazo_meses_cam / 12.0))
        
        if "Anual" in pago_freq_cam:
            i_pago_cam = tea_cam
            n_pagos_cam = n_anos_cam if n_anos_cam >= 1 else 1
            cuota_anual_cam = vp_cam * (i_pago_cam / (1 - (1 + i_pago_cam)**(-n_pagos_cam)))
            # Cuota mensual equivalente
            i_mensual_cam = ((1 + tea_cam)**(1.0 / 12.0)) - 1.0
            cuota_mensual_equiv = vp_cam * (i_mensual_cam / (1 - (1 + i_mensual_cam)**(-plazo_meses_cam)))
        elif "Mensual" in pago_freq_cam:
            i_pago_cam = ((1 + tea_cam)**(1.0 / 12.0)) - 1.0
            n_pagos_cam = plazo_meses_cam
            cuota_anual_cam = vp_cam * (tea_cam / (1 - (1 + tea_cam)**(-n_anos_cam))) if n_anos_cam >= 1 else 0
            cuota_mensual_equiv = vp_cam * (i_pago_cam / (1 - (1 + i_pago_cam)**(-n_pagos_cam)))
        else:
            i_pago_cam = tasa_sem_cam
            n_pagos_cam = int(round(plazo_meses_cam / 6.0))
            cuota_anual_cam = vp_cam * (tea_cam / (1 - (1 + tea_cam)**(-n_anos_cam))) if n_anos_cam >= 1 else 0
            i_mensual_cam = ((1 + tea_cam)**(1.0 / 12.0)) - 1.0
            cuota_mensual_equiv = vp_cam * (i_mensual_cam / (1 - (1 + i_mensual_cam)**(-plazo_meses_cam)))

        st.markdown("#### 📊 Tasas y Cuotas Calculadas:")
        m_c1, m_c2, m_c3 = st.columns(3)
        m_c1.metric("Tasa Efectiva Anual (TEA)", f"{fmt_n(tea_cam*100, 4)}%")
        m_c2.metric("Valor Cuota Anual (R Anual)", f"${fmt_m(cuota_anual_cam)}")
        m_c3.metric("Valor Cuota Mensual Equivalente", f"${fmt_m(cuota_mensual_equiv)}")

        # Generar Tabla de Desarrollo Completa (Amortización)
        saldo_cam = vp_cam
        tabla_cam = []
        intereses_totales_cam = 0.0
        
        cuota_periodo_cam = vp_cam * (i_pago_cam / (1 - (1 + i_pago_cam)**(-n_pagos_cam)))
        for period in range(1, n_pagos_cam + 1):
            int_cam = saldo_cam * i_pago_cam
            amort_cam = cuota_periodo_cam - int_cam
            saldo_next_cam = max(0.0, saldo_cam - amort_cam)
            intereses_totales_cam += int_cam
            
            tabla_cam.append({
                "Periodo": period,
                "Cuota ($)": fmt_m(cuota_periodo_cam),
                "Amortización ($)": fmt_m(amort_cam),
                "Interés ($)": fmt_m(int_cam),
                "Saldo Final ($)": fmt_m(saldo_next_cam)
            })
            saldo_cam = saldo_next_cam

        df_tabla_cam = pd.DataFrame(tabla_cam)
        st.markdown("#### 📋 Tabla de Desarrollo de Crédito (Amortización)")
        st.dataframe(df_tabla_cam)
        
        # Botón de exportación a Excel para Herramienta X
        excel_cam = to_excel(df_tabla_cam, sheet_name="Tabla_Desarrollo_Credito")
        st.download_button(
            label="📥 Exportar Tabla de Desarrollo a Excel (.xlsx)",
            data=excel_cam,
            file_name="tabla_desarrollo_credito_comercial.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        
        st.success(f"✅ Al final de los {n_anos_cam} años del crédito, pagará **${fmt_m(intereses_totales_cam)}** sólo por concepto de intereses.")

    # -------------------------------------------------------------
    # HERRAMIENTA XI: TASA IMPLÍCITA ANUAL PAGO ÚNICO
    # -------------------------------------------------------------
    elif "XI. Tasa Implícita" in calc_option:
        st.subheader("🛠️ XI. Tasa Implícita Anual para Créditos o Inversiones de Pago Único")
        
        i1, i2, i3 = st.columns(3)
        with i1:
            vp_imp = smart_num_input("Monto Inicial / Préstamo (VP $):", 5000000.0, key="imp_vp")
            st.markdown(f'<div class="val-badge">💵 VP: ${fmt_m(vp_imp)}</div>', unsafe_allow_html=True)
        with i2:
            vf_imp = smart_num_input("Monto Único Pagado (VF $):", 8000000.0, key="imp_vf")
            st.markdown(f'<div class="val-badge">💵 VF: ${fmt_m(vf_imp)}</div>', unsafe_allow_html=True)
        with i3:
            plazo_imp = smart_num_input("Plazo Total:", 12.0, key="imp_plazo")
            unit_imp = st.selectbox("Unidad del Plazo:", ["Trimestres", "Meses", "Años", "Semestres", "Cuatrimestres"], key="imp_unit")
            
        freq_imp_map = {"Trimestres": 4.0, "Meses": 12.0, "Años": 1.0, "Semestres": 2.0, "Cuatrimestres": 3.0}
        m_imp = freq_imp_map[unit_imp]
        anos_imp = plazo_imp / m_imp
        
        if vf_imp > vp_imp and anos_imp > 0:
            tea_imp = ((vf_imp / vp_imp) ** (1.0 / anos_imp)) - 1.0
            t_trim = ((1 + tea_imp) ** (1.0 / 4.0)) - 1.0
            i_per_imp = ((vf_imp / vp_imp) ** (1.0 / plazo_imp)) - 1.0
            tna_imp = tea_imp if unit_imp == "Años" else (i_per_imp * m_imp)
            
            st.markdown("#### 🎯 Tasas Implícitas Calculadas:")
            m_i1, m_i2, m_i3, m_i4 = st.columns(4)
            m_i1.metric("Tasa Efectiva Anual (TEA)", f"{fmt_n(tea_imp*100, 4)}%")
            m_i2.metric("Tasa Interés Trimestral", f"{fmt_n(t_trim*100, 4)}%")
            m_i3.metric(f"Tasa Periódica ({unit_imp[:-1]})", f"{fmt_n(i_per_imp*100, 4)}%")
            m_i4.metric("Tasa Nominal Anual (TNA)", f"{fmt_n(tna_imp*100, 4)}%")
            
            st.info(f"Fórmula aplicada por el sistema: $TEA = ({fmt_m(vf_imp)} / {fmt_m(vp_imp)})^{{1 / {fmt_n(anos_imp, 2)}}} - 1 = {fmt_n(tea_imp*100, 4)}%$")

    # -------------------------------------------------------------
    # HERRAMIENTA XII: VALOR PRESENTE CON ALTA PRECISIÓN DECIMAL
    # -------------------------------------------------------------
    else:
        st.subheader("🛠️ XII. Valor Presente con Alta Precisión Decimal (4 Decimales)")
        
        e1, e2, e3 = st.columns(3)
        with e1:
            vf_exact = smart_num_input("Monto Pagado al Final (VF $):", 3545900.0, key="ex_vf")
            st.markdown(f'<div class="val-badge">💵 VF: ${fmt_m(vf_exact)}</div>', unsafe_allow_html=True)
        with e2:
            tasa_exact = smart_num_input("Tasa Anual (%):", 14.80, key="ex_tasa") / 100.0
            st.markdown(f'<div class="val-badge">📈 Tasa Anual: {fmt_n(tasa_exact*100, 2)}%</div>', unsafe_allow_html=True)
        with e3:
            meses_exact = smart_num_input("Plazo en Meses:", 24.0, key="ex_meses")
            st.markdown(f'<div class="val-badge">⏳ Plazo: {meses_exact} meses</div>', unsafe_allow_html=True)
            
        anos_exact = meses_exact / 12.0
        vp_exact_val = vf_exact / ((1 + tasa_exact)**anos_exact)
        
        # Formatear exactamente con 4 decimales usando coma como separador de decimales
        formatted_exact_4 = f"{vp_exact_val:,.4f}".replace(",", "X").replace(".", ",").replace("X", ".")
        
        st.metric("Valor Presente Exacto (VP)", formatted_exact_4)
        st.success(f"✅ **Valor Presente Exacto con 4 Decimales:** **{formatted_exact_4}**")

st.markdown("---")
st.caption("Plataforma de Simulación & Ingeniería Financiera — Generado para Gemini Notebook")
