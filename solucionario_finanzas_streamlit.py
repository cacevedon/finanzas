import streamlit as st
import numpy as np
import pandas as pd
import numpy_financial as npf
import math

# Configuración de página
st.set_page_config(
    page_title="04 Finanzas - Plataforma Web Interactiva",
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
    .metric-card {
        background-color: #F8F9FA;
        border-left: 5px solid #2F5496;
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 10px;
    }
    .stButton>button {
        background-color: #2F5496;
        color: white;
        border-radius: 5px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Funciones helper para formateo chileno/latinoamericano con separadores de miles
def fmt_m(val):
    """Formatea montos de dinero en moneda con punto para miles y coma para decimales."""
    try:
        val = float(val)
        formatted = f"{val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        return f"${formatted}"
    except:
        return str(val)

def fmt_n(val, decimals=0):
    """Formatea cantidades o periodos con punto para miles."""
    try:
        val = float(val)
        if decimals == 0:
            formatted = f"{val:,.0f}".replace(",", "X").replace(".", ",").replace("X", ".")
        else:
            formatted = f"{val:,.{decimals}f}".replace(",", "X").replace(".", ",").replace("X", ".")
        return formatted
    except:
        return str(val)

def fmt_p(val):
    """Formatea porcentajes."""
    try:
        val = float(val)
        formatted = f"{val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        return f"{formatted}%"
    except:
        return str(val)

# Helper para crear número de entrada con etiqueta y caption formateado en tiempo real
def numero_entrada_moneda(label, value, step=1000.0, key=None):
    val = st.number_input(label, value=float(value), step=float(step), key=key)
    st.caption(f"💵 **Monto registrado:** `{fmt_m(val)}`")
    return val

def numero_entrada_tasa(label, value, step=0.1, key=None):
    val = st.number_input(label, value=float(value), step=float(step), key=key)
    st.caption(f"📈 **Tasa registrada:** `{fmt_p(val)}`")
    return val

def numero_entrada_cantidad(label, value, step=1.0, decimals=0, key=None):
    val = st.number_input(label, value=float(value), step=float(step), key=key)
    st.caption(f"🔢 **Valor registrado:** `{fmt_n(val, decimals)}`")
    return val

# Encabezado Principal
st.markdown('<div class="main-header">04 FINANZAS — Solucionario Web & Simulación Financiera</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Plataforma interactiva master basada en los contenidos, guías, talleres, publicaciones y exámenes de la asignatura.</div>', unsafe_allow_html=True)

# Barra lateral de navegación
st.sidebar.title("📌 Navegación del Curso")
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
st.sidebar.info("💡 **Tip de Uso:** Todos los campos numéricos muestran automáticamente sus separadores de miles y notación chilena en tiempo real.")

# ==========================================
# MÓDULO 1: FUNDAMENTOS
# ==========================================
if modulo == "1. Fundamentos y Decisiones":
    st.header("Módulo 1: Fundamentos de Finanzas & Toma de Decisiones Estratégicas")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📚 Marco Teórico Clave")
        st.markdown(f"""
        - **Valor del Dinero en el Tiempo (VDT):** Un peso recibido hoy vale más que un peso recibido en el futuro debido a la capacidad de generar rendimiento financiero, el efecto inflacionario y el riesgo de crédito.
        - **Costo de Oportunidad:** La tasa de rentabilidad de la mejor alternativa de inversión sacrificada al tomar una decisión financiera.
        - **Compensación Riesgo-Liquidez-Rentabilidad:** Existe una relación inversa entre liquidez inmediata y rentabilidad esperada, y una relación directa entre riesgo asumido y retorno exigido.
        - **Decisiones Corporativas Fundamentales:**
          1. *Decisiones de Inversión:* Definir en qué activos productivos o financieros colocar los recursos.
          2. *Decisiones de Financiamiento:* Seleccionar la estructura óptima de capital (deuda vs. patrimonio).
          3. *Decisiones de Dividendos:* Definir qué proporción de las utilidades se reinvierte y cuál se distribuye.
        """)
        
    with col2:
        st.subheader("🎯 Matriz de Decisiones Cotidianas (Casos Reales)")
        caso = st.selectbox("Selecciona un Caso Práctico:", [
            f"Caso 1: Lucía y el bono de {fmt_m(500000)}",
            f"Caso 2: Carlos y la compra a crédito por {fmt_m(600000)}",
            f"Caso 3: Presupuesto familiar con imprevisto ({fmt_p(15)})",
            f"Caso 4: Excedente de caja en Pyme Rápido de {fmt_m(5000000)}"
        ])
        
        if "Lucía" in caso:
            st.info(f"**Situación:** Lucía recibe un bono de **{fmt_m(500000)}** y evalúa gastarlo en vacaciones o depositarlo a plazo fijo al **{fmt_p(0.6)}** mensual.")
            st.success(f"**Recomendación Financiera:** Depositar a plazo fijo o en un fondo de liquidez conservador. En 12 meses acumularía **{fmt_m(537026)}**. Prioriza la acumulación de patrimonio y la disciplina financiera.")
        elif "Carlos" in caso:
            st.info(f"**Situación:** Carlos evalúa comprar un equipo al contado por **{fmt_m(600000)}** o en 12 cuotas mensuales de **{fmt_m(62000)}** (Total: **{fmt_m(744000)}**).")
            st.warning(f"**Recomendación Financiera:** Pagar al contado si cuenta con la liquidez. La modalidad a crédito implica un costo financiero total implícito superior al **{fmt_p(40)}** anual.")
        elif "Presupuesto" in caso:
            st.info(f"**Situación:** Una familia con ingresos de **{fmt_m(1200000)}** enfrenta una emergencia médica del **{fmt_p(15)}** de sus ingresos (**{fmt_m(180000)}**).")
            st.error(f"**Recomendación Financiera:** Cubrir la contingencia mediante el fondo de reserva de liquidez. En caso de no poseerlo, reajustar gastos prescindibles del mes y evitar el uso de crédito rotativo de alto costo.")
        else:
            st.info(f"**Situación:** Pyme Rápido mantiene **{fmt_m(5000000)}** ociosos en su cuenta corriente operativa.")
            st.success(f"**Recomendación Financiera:** Destinar el **{fmt_p(60)}** (**{fmt_m(3000000)}**) a fondos de inversión de rescate diario o pactos comerciales para rentabilizar el saldo sin comprometer la liquidez operativa.")

# ==========================================
# MÓDULO 2: INTERÉS SIMPLE Y COMPUESTO
# ==========================================
elif modulo == "2. Interés Simple y Compuesto":
    st.header("Módulo 2: Regímenes de Capitalización (Interés Simple vs. Compuesto)")
    
    st.subheader("⚙️ Calculadora Universal de Interés")
    
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        vp_input = numero_entrada_moneda("Capital Inicial (VP):", 1000000.0, step=50000.0, key="m2_vp")
    with c2:
        tasa_input_pct = numero_entrada_tasa("Tasa Periódica (%):", 1.5, step=0.1, key="m2_tasa")
        tasa_input = tasa_input_pct / 100.0
    with c3:
        n_input = numero_entrada_cantidad("Plazo (Periodos):", 12, step=1.0, key="m2_n")
        n_input_int = int(n_input)
    with c4:
        regimen = st.selectbox("Régimen de Capitalización:", ["Interés Compuesto", "Interés Simple", "Comparar Ambos"])
        
    vf_simple = vp_input * (1 + tasa_input * n_input_int)
    vf_compuesto = vp_input * ((1 + tasa_input) ** n_input_int)
    
    res_df = pd.DataFrame({
        "Periodo": list(range(0, n_input_int + 1)),
        "Interés Simple ($)": [vp_input * (1 + tasa_input * t) for t in range(0, n_input_int + 1)],
        "Interés Compuesto ($)": [vp_input * ((1 + tasa_input) ** t) for t in range(0, n_input_int + 1)]
    })
    
    st.markdown("#### Resultados Proyectados")
    mc1, mc2, mc3 = st.columns(3)
    mc1.metric("Valor Futuro (Simple)", fmt_m(vf_simple))
    mc2.metric("Valor Futuro (Compuesto)", fmt_m(vf_compuesto))
    mc3.metric("Diferencia por Interés Sobre Interés", fmt_m(vf_compuesto - vf_simple))
    
    st.line_chart(res_df.set_index("Periodo"))
    
    st.markdown("---")
    st.subheader("📝 Resoluciones del 100% de los Casos de la Unidad")
    
    prob_sel = st.selectbox("Selecciona un Caso Práctico a Revisar:", [
        f"Caso 1: Matrimonio e Inversión de {fmt_m(25000000)} a 5 Años",
        f"Caso 2: División de Inversión de {fmt_m(75000000)}",
        f"Caso 3: Sistema de Ecuaciones — Inversión de {fmt_m(980000000)} en Bancos A y B",
        f"Caso 4: Igualación de Flujos de Deuda ({fmt_m(70000000)}) vs Inversión ({fmt_m(50000000)})",
        f"Caso 5: División de Capital de {fmt_m(33000000)} al 12% y 9% Simple"
    ])
    
    if "Caso 1:" in prob_sel:
        st.markdown(f"""
        - **Monto Inicial:** `{fmt_m(25000000)}` por un plazo de **60 meses** (5 años).
        - **Opción A (Interés Simple {fmt_p(0.8)} mensual):**  
          $VF_A = {fmt_m(25000000)} \\times (1 + 0,008 \\times 60) =$ **{fmt_m(25000000 * (1 + 0.008 * 60))}**
        - **Opción B (Interés Compuesto {fmt_p(0.75)} mensual):**  
          $VF_B = {fmt_m(25000000)} \\times (1 + 0,0075)^{{60}} =$ **{fmt_m(25000000 * ((1 + 0.0075)**60))}**
        """)
        diff = (25000000 * ((1 + 0.0075)**60)) - (25000000 * (1 + 0.008 * 60))
        st.success(f"✅ Conviene la **Opción B (Interés Compuesto)** con un excedente a favor de **{fmt_m(diff)}** gracias al efecto de capitalización.")

    elif "Caso 2:" in prob_sel:
        st.markdown(f"""
        - **Capital Total:** `{fmt_m(75000000)}`.
        - **Tramo 1 ({fmt_m(45000000)}):** Invertido al **{fmt_p(1.2)}** mensual compuesto durante 36 meses.  
          $VF_1 = {fmt_m(45000000)} \\times (1 + 0,012)^{{36}} =$ **{fmt_m(45000000 * ((1 + 0.012)**36))}**
        - **Tramo 2 ({fmt_m(30000000)}):** Invertido al **{fmt_p(1.0)}** mensual compuesto durante 36 meses.  
          $VF_2 = {fmt_m(30000000)} \\times (1 + 0,010)^{{36}} =$ **{fmt_m(30000000 * ((1 + 0.010)**36))}**
        """)
        total_vf = (45000000 * ((1 + 0.012)**36)) + (30000000 * ((1 + 0.010)**36))
        st.success(f"✅ **Monto Acumulado Total al Año 3:** **{fmt_m(total_vf)}**")

    elif "Caso 3:" in prob_sel:
        st.markdown(f"""
        - **Banco A:** {fmt_p(5.04)} anual simple $\\Rightarrow i_A = 5,04\\% / 12 = {fmt_p(0.42)}$ mensual.
        - **Banco B:** {fmt_p(2.1)} trimestral simple $\\Rightarrow i_B = 2,1\\% / 3 = {fmt_p(0.70)}$ mensual.
        - **Sistema de Ecuaciones:**
          1) $X + Y = {fmt_m(980000000)}$  
          2) $0,0042 X + 0,0070 Y = {fmt_m(5500000)}$
        """)
        y_val = (5500000 - 0.0042 * 980000000) / (0.0070 - 0.0042)
        x_val = 980000000 - y_val
        st.success(f"✅ **Monto en Banco A (X):** **{fmt_m(x_val)}** | **Monto en Banco B (Y):** **{fmt_m(y_val)}**")

    elif "Caso 4:" in prob_sel:
        st.markdown(f"""
        - **Ecuación de Igualación:** $VF_{{\text{{Inversión}}}} = VF_{{\text{{Deuda}}}}$
        - ${fmt_m(50000000)} \\times (1,07)^n = {fmt_m(70000000)} \\times (1,035)^n$
        - $(1,07 / 1,035)^n = {fmt_m(70000000)} / {fmt_m(50000000)} = 1,40$
        - $n \\times \\ln(1,03381643) = \\ln(1,40)$
        """)
        n_res = math.log(1.40) / math.log(1.07 / 1.035)
        st.success(f"✅ **Tiempo Exacto de Igualación:** **{fmt_n(n_res, 2)} períodos/años** ({fmt_n(n_res * 12, 1)} meses).")

    else:
        st.markdown(f"""
        - **Capital Total:** `{fmt_m(33000000)}`.
        - **Parte 1 (Un Tercio = {fmt_m(11000000)}):** Invertido al **{fmt_p(12)}** anual simple por 8 meses.  
          $I_1 = {fmt_m(11000000)} \\times 0,01 \\times 8 =$ **{fmt_m(11000000 * 0.01 * 8)}**
        - **Parte 2 (Dos Tercios = {fmt_m(22000000)}):** Invertido al **{fmt_p(9)}** anual simple ($0,75\\%$ mensual).  
          Interés Meta Restante $= {fmt_m(2860000)} - {fmt_m(880000)} =$ **{fmt_m(1980000)}**
        """)
        n_meses_part2 = 1980000 / (22000000 * 0.0075)
        st.success(f"✅ **Tiempo Requerido para la Segunda Parte:** **{fmt_n(n_meses_part2, 0)} meses**.")

# ==========================================
# MÓDULO 3: CONVERSIÓN DE TASAS
# ==========================================
elif modulo == "3. Conversión de Tasas (TNA/TEA)":
    st.header("Módulo 3: Conversión y Decodificación de Tasas de Interés")
    
    col_t1, col_t2 = st.columns(2)
    
    with col_t1:
        st.subheader("🔄 Conversor Universal de TNA ➔ TEA")
        tna_input_pct = numero_entrada_tasa("Tasa Nominal Anual (TNA %):", 24.0, step=0.5, key="m3_tna")
        tna_val = tna_input_pct / 100.0
        
        freq_dict = {
            "Mensual (m=12)": 12,
            "Bimestral (m=6)": 6,
            "Trimestral (m=4)": 4,
            "Cuatrimestral (m=3)": 3,
            "Semestral (m=2)": 2,
            "Diaria (m=360)": 360,
            "Diaria (m=365)": 365
        }
        freq_sel = st.selectbox("Frecuencia de Capitalización (m):", list(freq_dict.keys()))
        m_val = freq_dict[freq_sel]
        
        i_per = tna_val / m_val
        tea_calc = ((1 + i_per) ** m_val) - 1.0
        
        st.write(f"• **Tasa Periódica ($i'$):** `{fmt_p(i_per * 100)}`")
        st.metric("Tasa Efectiva Anual (TEA Equivalente)", fmt_p(tea_calc * 100))

    with col_t2:
        st.subheader("⚖️ Comparador Financiero de Alternativas")
        st.markdown(f"""
        - **Banco X:** {fmt_p(9.0)} TNA con capitalización trimestral ($m=4$).
        - **Banco Y:** {fmt_p(9.2)} TEA directa.
        """)
        tea_x = ((1 + 0.09/4)**4) - 1.0
        tea_y = 0.092
        
        st.write(f"• **TEA Banco X:** $(1 + 0,09/4)^4 - 1 =$ `{fmt_p(tea_x * 100)}`")
        st.write(f"• **TEA Banco Y:** `{fmt_p(tea_y * 100)}`")
        
        if tea_x > tea_y:
            st.success(f"✅ **Para Invertir/Ahorrar:** Conviene **Banco X** ({fmt_p(tea_x * 100)} TEA).\n\n✅ **Para Solicitar Crédito:** Conviene **Banco Y** ({fmt_p(9.2)} TEA).")

# ==========================================
# MÓDULO 4: ANUALIDADES
# ==========================================
elif modulo == "4. Anualidades y Amortización":
    st.header("Módulo 4: Anualidades y Tablas de Amortización de Deudas")
    
    st.subheader("💳 Simulador de Préstamos y Amortización (Método Francés)")
    
    ac1, ac2, ac3 = st.columns(3)
    with ac1:
        monto_prestamo = numero_entrada_moneda("Monto del Préstamo ($):", 30000.0, step=1000.0, key="m4_monto")
    with ac2:
        tasa_mensual_pct = numero_entrada_tasa("Tasa Efectiva Mensual (%):", 1.2, step=0.1, key="m4_tasa")
        tasa_mensual_anu = tasa_mensual_pct / 100.0
    with ac3:
        plazo_meses_input = numero_entrada_cantidad("Plazo en Meses (n):", 36, step=1.0, key="m4_plazo")
        plazo_meses = int(plazo_meses_input)
        
    # Cuota fija (PMT)
    cuota_fija = monto_prestamo * (tasa_mensual_anu / (1 - (1 + tasa_mensual_anu)**(-plazo_meses)))
    
    st.metric("Cuota Mensual Calculada (R)", fmt_m(cuota_fija))
    
    # Tabla de Amortización
    saldo = monto_prestamo
    amort_data = []
    for mes in range(1, plazo_meses + 1):
        interes_mes = saldo * tasa_mensual_anu
        capital_mes = cuota_fija - interes_mes
        saldo_final = max(0.0, saldo - capital_mes)
        amort_data.append({
            "Mes": mes,
            "Saldo Inicial": saldo,
            "Cuota ($)": cuota_fija,
            "Interés ($)": interes_mes,
            "Amortización ($)": capital_mes,
            "Saldo Final": saldo_final
        })
        saldo = saldo_final
        
    df_amort = pd.DataFrame(amort_data)
    
    st.markdown("#### Tabla de Amortización Dinámica")
    
    # Formateador para dataframes con formato chileno
    formatted_df = df_amort.copy()
    for col in ["Saldo Inicial", "Cuota ($)", "Interés ($)", "Amortización ($)", "Saldo Final"]:
        formatted_df[col] = formatted_df[col].apply(fmt_m)
        
    st.dataframe(formatted_df, height=300)
    
    st.markdown("#### Descomposición de la Cuota: Intereses vs. Amortización")
    st.bar_chart(df_amort.set_index("Mes")[["Interés ($)", "Amortización ($)"]])

# ==========================================
# MÓDULO 5: GRADIENTES
# ==========================================
elif modulo == "5. Gradientes Financieros":
    st.header("Módulo 5: Gradientes Financieros (Series Variables)")
    
    st.subheader("📈 Comparativa de Series: Constante vs. Aritmética vs. Geométrica")
    
    gc1, gc2, gc3 = st.columns(3)
    with gc1:
        base_a = numero_entrada_moneda("Flujo Base Inicial (A):", 1000.0, step=100.0, key="m5_a")
    with gc2:
        grad_g = numero_entrada_moneda("Gradiente Aritmético (G $):", 200.0, step=50.0, key="m5_g")
    with gc3:
        grad_pct_val = numero_entrada_tasa("Gradiente Geométrico (g %):", 10.0, step=1.0, key="m5_pct")
        grad_pct = grad_pct_val / 100.0
        
    periodos_g = 10
    grad_df = pd.DataFrame({
        "Año": list(range(1, periodos_g + 1)),
        "Serie Constante": [base_a] * periodos_g,
        "Gradiente Aritmético (+G)": [base_a + (t - 1) * grad_g for t in range(1, periodos_g + 1)],
        "Gradiente Geométrico (+g)": [base_a * ((1 + grad_pct)**(t - 1)) for t in range(1, periodos_g + 1)]
    })
    
    st.line_chart(grad_df.set_index("Año"))
    
    st.markdown("---")
    st.subheader("🏗️ Caso Destacado: Proyecto Planta de Desalinización")
    st.markdown(f"""
    - **Inversión Inicial:** `{fmt_m(5000000)}` diferida al término del año 4.
    - **Flujo del Año 5:** `{fmt_m(800000)}` con crecimiento perpetuo al $g = {fmt_p(5)}$ anual.
    - **Tasa de Descuento (TMAR):** {fmt_p(12)} anual.
    """)
    vp_perpetuidad_4 = 800000 / (0.12 - 0.05)
    vp_hoy_0 = vp_perpetuidad_4 / ((1 + 0.12)**4)
    st.write(f"• **Valor Presente en Año 4 ($VP_4$):** `{fmt_m(800000)} / (0,12 - 0,05) =` **{fmt_m(vp_perpetuidad_4)}**")
    st.write(f"• **Valor Presente Hoy ($VP_0$):** `{fmt_m(vp_perpetuidad_4)} / (1,12)^4 =` **{fmt_m(vp_hoy_0)}**")

# ==========================================
# MÓDULO 6: PRESUPUESTOS
# ==========================================
elif modulo == "6. Presupuesto y Flujo de Caja":
    st.header("Módulo 6: Presupuestos y Control de Caja Operacional")
    
    st.subheader("📊 Simulador de Presupuesto Mensual a 12 Meses con Inflación")
    
    pc1, pc2, pc3 = st.columns(3)
    with pc1:
        v_base = numero_entrada_moneda("Ventas Mes 1 ($):", 15000.0, step=1000.0, key="m6_vbase")
    with pc2:
        g_ventas_pct = numero_entrada_tasa("Crecimiento Ventas Mensual (%):", 1.5, step=0.1, key="m6_gventas")
        g_ventas = g_ventas_pct / 100.0
    with pc3:
        inf_mensual_pct = numero_entrada_tasa("Inflación Costos Mensual (%):", 0.5, step=0.1, key="m6_inf")
        inf_mensual = inf_mensual_pct / 100.0
        
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
            "Ventas ($)": ventas_m,
            "Total Egresos ($)": egresos_total,
            "Flujo Neto ($)": flujo_neto,
            "Caja Acumulada ($)": caja_acum
        })
        
    df_pres = pd.DataFrame(p_data)
    
    # Garantizar orden cronológico estricto en la columna de Meses
    df_pres["Mes"] = pd.Categorical(
        df_pres["Mes"],
        categories=[f"Mes {i}" for i in range(1, meses_p + 1)],
        ordered=True
    )
    
    df_pres_formatted = df_pres.copy()
    for col in ["Ventas ($)", "Total Egresos ($)", "Flujo Neto ($)", "Caja Acumulada ($)"]:
        df_pres_formatted[col] = df_pres_formatted[col].apply(fmt_m)
        
    st.dataframe(df_pres_formatted)
    st.bar_chart(df_pres.set_index("Mes")[["Ventas ($)", "Total Egresos ($)"]])

# ==========================================
# MÓDULO 7: EVALUACIÓN DE PROYECTOS
# ==========================================
elif modulo == "7. Evaluación de Proyectos (VAN/TIR)":
    st.header("Módulo 7: Evaluación Financiera de Proyectos")
    
    st.subheader("🎯 Punto de Equilibrio Operacional")
    eq1, eq2, eq3 = st.columns(3)
    with eq1:
        cf_val = numero_entrada_moneda("Costos Fijos Totales ($):", 120000.0, step=5000.0, key="m7_cf")
    with eq2:
        p_val = numero_entrada_moneda("Precio Unitario ($):", 50.0, step=1.0, key="m7_p")
    with eq3:
        cv_val = numero_entrada_moneda("Costo Variable Unitario ($):", 30.0, step=1.0, key="m7_cv")
        
    mc_unit = p_val - cv_val
    if mc_unit > 0:
        q_eq = cf_val / mc_unit
        ing_eq = q_eq * p_val
        st.success(f"• **Punto de Equilibrio en Unidades:** **{fmt_n(q_eq, 0)} unidades**")
        st.success(f"• **Ingreso de Equilibrio:** **{fmt_m(ing_eq)}**")
    else:
        st.error("El precio unitario debe ser estrictamente mayor al costo variable.")
        
    st.markdown("---")
    st.subheader("💰 Evaluación de Flujos de Caja (VAN y TIR)")
    
    inv_ini = numero_entrada_moneda("Inversión Inicial ($):", 500000.0, step=10000.0, key="m7_inv")
    tmar_pct = numero_entrada_tasa("Tasa de Descuento / TMAR (%):", 10.0, step=0.5, key="m7_tmar")
    tmar_val = tmar_pct / 100.0
    
    st.write("Ingresa los flujos proyectados a 5 años:")
    fc_cols = st.columns(5)
    flujos = []
    for idx, col in enumerate(fc_cols):
        with col:
            f_val = numero_entrada_moneda(f"Año {idx+1} ($):", 140000.0 + idx*10000.0, step=5000.0, key=f"m7_f{idx+1}")
            flujos.append(f_val)
            
    van_val = npf.npv(tmar_val, [0] + flujos) - inv_ini
    tir_val = npf.irr([-inv_ini] + flujos)
    
    col_v1, col_v2 = st.columns(2)
    col_v1.metric("Valor Actual Neto (VAN)", fmt_m(van_val), delta="Proyecto Viable" if van_val > 0 else "No Viable")
    col_v2.metric("Tasa Interna de Retorno (TIR)", fmt_p(tir_val * 100), delta="TIR > TMAR" if tir_val > tmar_val else "TIR < TMAR")

# ==========================================
# MÓDULO 8: CALCULADORAS ESPECIALIZADAS
# ==========================================
elif modulo == "8. Calculadoras Especializadas":
    st.header("Módulo 8: Calculadoras Especializadas")
    
    st.subheader("🛠️ Suite de Solucionadores Cuantitativos")
    
    solver = st.selectbox("Selecciona la Herramienta de Cálculo:", [
        "1. Calculadora de Valor Futuro a Plazos Fraccionados (Meses/Años)",
        "2. Solucionador de Plazo Requerido y Horizonte de Inversión (Despeje de n)",
        "3. Evaluador de Saldo Insoluto de Deuda al Período k",
        "4. Calculadora de Cuota de Crédito y Carga Financiera (PMT)",
        "5. Conversor Avanzado de Tasas Nominales y Diferenciales (TEA/TNA)"
    ])
    
    if "1. Calculadora" in solver:
        st.markdown("#### Proyección de Capital a Plazo Fraccionado")
        s1_col1, s1_col2, s1_col3 = st.columns(3)
        with s1_col1:
            s1_vp = numero_entrada_moneda("Capital Inicial (VP):", 1000.0, step=100.0, key="s1_vp")
        with s1_col2:
            s1_meses = numero_entrada_cantidad("Plazo en Meses (n):", 16.0, step=1.0, key="s1_meses")
        with s1_col3:
            s1_tasa_pct = numero_entrada_tasa("Tasa Anual Efectiva (%):", 5.0, step=0.5, key="s1_tasa")
            s1_tasa = s1_tasa_pct / 100.0
            
        s1_vf = s1_vp * ((1 + s1_tasa) ** (s1_meses / 12.0))
        st.success(f"✅ **Valor Futuro Acumulado (VF):** **{fmt_m(s1_vf)}**")
        st.info(f"Fórmula aplicada: $VF = {fmt_m(s1_vp)} \\times (1 + {s1_tasa_pct/100:.2f})^{{{s1_meses:.0f}/12}}$")

    elif "2. Solucionador" in solver:
        st.markdown("#### Despeje de Plazo Requerido ($n$)")
        s2_col1, s2_col2, s2_col3 = st.columns(3)
        with s2_col1:
            s2_vp = numero_entrada_moneda("Capital Inicial (VP):", 2000.0, step=100.0, key="s2_vp")
        with s2_col2:
            s2_vf = numero_entrada_moneda("Valor Futuro Meta (VF):", 3525.0, step=100.0, key="s2_vf")
        with s2_col3:
            s2_tasa_pct = numero_entrada_tasa("Tasa Anual Efectiva (%):", 12.0, step=0.5, key="s2_tasa")
            s2_tasa = s2_tasa_pct / 100.0
            
        if s2_vf > s2_vp and s2_tasa > 0:
            s2_n = math.log(s2_vf / s2_vp) / math.log(1 + s2_tasa)
            st.success(f"✅ **Plazo Necesario:** **{fmt_n(s2_n, 2)} años** ({fmt_n(s2_n * 12, 1)} meses).")
            st.info(f"Fórmula aplicada: $n = \\frac{{\\ln({fmt_m(s2_vf)} / {fmt_m(s2_vp)})}}{{\\ln(1 + {s2_tasa:.2f})}}$")

    elif "3. Evaluador" in solver:
        st.markdown("#### Saldo Insoluto de Deuda al Período $k$")
        s3_col1, s3_col2, s3_col3, s3_col4 = st.columns(4)
        with s3_col1:
            s3_monto = numero_entrada_moneda("Monto Préstamo:", 1000000.0, step=50000.0, key="s3_monto")
        with s3_col2:
            s3_plazo = numero_entrada_cantidad("Plazo Años:", 5.0, step=1.0, key="s3_plazo")
            s3_plazo_int = int(s3_plazo)
        with s3_col3:
            s3_tasa_pct = numero_entrada_tasa("Tasa Anual (%):", 18.0, step=0.5, key="s3_tasa")
            s3_tasa = s3_tasa_pct / 100.0
        with s3_col4:
            s3_k = numero_entrada_cantidad("Años Pagados (k):", 3.0, step=1.0, key="s3_k")
            s3_k_int = int(s3_k)
            
        # Cuota anual PMT
        s3_pmt = s3_monto * (s3_tasa / (1 - (1 + s3_tasa)**(-s3_plazo_int)))
        restantes = s3_plazo_int - s3_k_int
        s3_saldo = s3_pmt * ((1 - (1 + s3_tasa)**(-restantes)) / s3_tasa)
        
        st.write(f"• **Cuota Anual Fija (R):** `{fmt_m(s3_pmt)}`")
        st.success(f"✅ **Saldo Insoluto de Capital al Año {s3_k_int}:** **{fmt_m(s3_saldo)}**")

    elif "4. Calculadora" in solver:
        st.markdown("#### Cuota Fija de Crédito ($PMT$)")
        s4_col1, s4_col2, s4_col3 = st.columns(3)
        with s4_col1:
            s4_monto = numero_entrada_moneda("Monto Préstamo ($):", 1800.0, step=100.0, key="s4_monto")
        with s4_col2:
            s4_meses = numero_entrada_cantidad("Plazo en Meses:", 36.0, step=1.0, key="s4_meses")
            s4_meses_int = int(s4_meses)
        with s4_col3:
            s4_tasa_pct = numero_entrada_tasa("Tasa Mensual (%):", 1.25, step=0.05, key="s4_tasa")
            s4_tasa = s4_tasa_pct / 100.0
            
        s4_cuota = s4_monto * (s4_tasa / (1 - (1 + s4_tasa)**(-s4_meses_int)))
        s4_total_pago = s4_cuota * s4_meses_int
        s4_intereses = s4_total_pago - s4_monto
        
        st.success(f"✅ **Cuota Mensual Fija:** **{fmt_m(s4_cuota)}**")
        st.write(f"• **Total Pagado al Finalizar:** `{fmt_m(s4_total_pago)}`")
        st.write(f"• **Intereses Totales Abonados:** `{fmt_m(s4_intereses)}`")

    else:
        st.markdown("#### Conversión y Margen de Tasa Diferencial")
        s5_col1, s5_col2 = st.columns(2)
        with s5_col1:
            s5_tna_pct = numero_entrada_tasa("Tasa Nominal Anual (TNA %):", 24.0, step=0.5, key="s5_tna")
            s5_tna = s5_tna_pct / 100.0
            s5_m = numero_entrada_cantidad("Capitalizaciones al Año (m):", 4.0, step=1.0, key="s5_m")
            s5_m_int = int(s5_m)
            s5_tea = ((1 + s5_tna / s5_m_int)**s5_m_int) - 1.0
            st.metric("Tasa Efectiva Anual (TEA)", fmt_p(s5_tea * 100))
        with s5_col2:
            s5_ref_pct = numero_entrada_tasa("Tasa de Referencia Mercado (%):", 14.5, step=0.5, key="s5_ref")
            s5_diff = (s5_tea * 100) - s5_ref_pct
            st.metric("Margen Diferencial (Spread)", fmt_p(s5_diff), delta=f"{fmt_p(s5_diff)} vs Referencia")

st.markdown("---")
st.caption("04 Finanzas Plataforma Master — Generado automáticamente para Gemini Notebook")
