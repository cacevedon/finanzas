import streamlit as st
import numpy as np
import pandas as pd
import numpy_financial as npf
import math

# Configuración de la página
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
    .val-badge {
        background-color: #E2EFDA;
        color: #276A3C;
        padding: 4px 10px;
        border-radius: 4px;
        font-weight: bold;
        font-size: 0.95rem;
        display: inline-block;
        margin-top: 4px;
        margin-bottom: 8px;
    }
    .stButton>button {
        background-color: #2F5496;
        color: white;
        border-radius: 5px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Helper functions para formato chileno/latinoamericano (punto para miles, coma para decimales)
def parse_num(val_str, default=0.0):
    if isinstance(val_str, (int, float)):
        return float(val_str)
    try:
        cleaned = str(val_str).replace('$', '').replace(' ', '').strip()
        if '.' in cleaned and ',' in cleaned:
            cleaned = cleaned.replace('.', '').replace(',', '.')
        elif ',' in cleaned:
            cleaned = cleaned.replace(',', '.')
        elif '.' in cleaned:
            parts = cleaned.split('.')
            if len(parts) > 2 or (len(parts) == 2 and len(parts[1]) == 3):
                cleaned = cleaned.replace('.', '')
        return float(cleaned)
    except:
        return float(default)

def fmt_m(val):
    try:
        v = float(val)
        return f"${v:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    except:
        return "$0,00"

def fmt_n(val, decimals=2):
    try:
        v = float(val)
        pattern = f"{{:,.{decimals}f}}"
        return pattern.format(v).replace(',', 'X').replace('.', ',').replace('X', '.')
    except:
        return "0,00"

def num_input_fmt(label, default_val, key, is_currency=True, help_text=None):
    def_str = fmt_n(default_val, 2) if is_currency else str(default_val)
    user_str = st.text_input(label, value=def_str, key=key, help=help_text)
    num_val = parse_num(user_str, default_val)
    prefix = "$" if is_currency else ""
    st.markdown(f'<div class="val-badge">💵 Registrado: {prefix}{fmt_n(num_val, 2)}</div>', unsafe_allow_html=True)
    return num_val

# Encabezado Principal
st.markdown('<div class="main-header">04 FINANZAS — Solucionario Web & Simulación Financiera</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Plataforma interactiva basada en los contenidos, guías, talleres y solemnes de la asignatura.</div>', unsafe_allow_html=True)

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
st.sidebar.info("💡 **Tip:** Puedes modificar los parámetros de los simuladores en tiempo real. Todos los montos incluyen separadores de miles.")

# ==========================================
# MÓDULO 1: FUNDAMENTOS
# ==========================================
if modulo == "1. Fundamentos y Decisiones":
    st.header("Unidad 1: Fundamentos y Decisiones Financieras")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📚 Marco Teórico Clave")
        st.markdown("""
        - **Valor del Dinero en el Tiempo (VDT):** Un peso hoy vale más que un peso mañana debido a la capacidad de generar intereses, la inflación y el riesgo.
        - **Costo de Oportunidad:** El rendimiento de la mejor alternativa sacrificada al tomar una decisión financiera.
        - **Liquidez vs. Rentabilidad:** A mayor liquidez inmediata, menor suele ser el rendimiento generado.
        - **Intermediación Financiera:** Bancos e instituciones canalizan el ahorro de agentes superavitarios hacia agentes deficitarios.
        """)
        
    with col2:
        st.subheader("🎯 Matriz de Decisiones Cotidianas")
        caso = st.selectbox("Selecciona un Caso Práctico:", [
            "Caso 1: Lucía y el bono de $500.000",
            "Caso 2: Carlos y la compra a crédito de $600.000",
            "Caso 3: Presupuesto familiar ($1.200.000) con imprevisto (15%)",
            "Caso 4: Excedente de caja de $5.000.000 en Pyme Rápido"
        ])
        
        if "Lucía" in caso:
            st.info(f"**Situación:** Lucía recibe un bono de {fmt_m(500000)} y duda entre gastarlo en vacaciones o depositarlo a plazo fijo al 0,60% mensual.")
            st.success(f"**Recomendación Financiera:** Depositar a plazo o invertir en un fondo mutuo conservador. En 12 meses obtendría {fmt_m(537026)}. Prioriza acumulación de capital y VDT.")
        elif "Carlos" in caso:
            st.info(f"**Situación:** Carlos evalúa comprar una laptop al contado ({fmt_m(600000)}) o en 12 cuotas de {fmt_m(62000)} (Total {fmt_m(744000)}).")
            st.warning("**Recomendación Financiera:** Comprar al contado si cuenta con liquidez. La alternativa a crédito implica un costo financiero total (CAE) implícito superior al 40,00% anual.")
        elif "Presupuesto" in caso:
            st.info(f"**Situación:** Familia con ingresos de {fmt_m(1200000)} sufre un gasto médico imprevisto equivalente al 15,00% de sus ingresos ({fmt_m(180000)}).")
            st.error("**Recomendación Financiera:** Recurrir al fondo de emergencia. Si no existe, reestructurar gastos prescindibles del mes y evitar créditos rotativos de tarjeta.")
        else:
            st.info(f"**Situación:** Pyme Rápido tiene {fmt_m(5000000)} ociosos en la cuenta corriente operativa.")
            st.success(f"**Recomendación Financiera:** Colocar el 60,00% ({fmt_m(3000000)}) en pactos diarios o fondos de liquidez inmediata para rentabilizar el saldo sin perder operatividad.")

# ==========================================
# MÓDULO 2: INTERÉS SIMPLE Y COMPUESTO
# ==========================================
elif modulo == "2. Interés Simple y Compuesto":
    st.header("Unidad 2: Interés Simple e Interés Compuesto")
    
    st.subheader("⚙️ Calculadora Universal de Interés")
    
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        vp_input = num_input_fmt("Capital Inicial (VP):", 1000000.0, "m2_vp")
    with c2:
        tasa_input = num_input_fmt("Tasa Periódica (%):", 1.5, "m2_tasa", is_currency=False) / 100.0
    with c3:
        n_input = int(num_input_fmt("Plazo (Periodos):", 12, "m2_n", is_currency=False))
    with c4:
        regimen = st.selectbox("Régimen:", ["Interés Compuesto", "Interés Simple", "Comparar Ambos"])
        
    vf_simple = vp_input * (1 + tasa_input * n_input)
    vf_compuesto = vp_input * ((1 + tasa_input) ** n_input)
    
    res_df = pd.DataFrame({
        "Periodo": list(range(0, n_input + 1)),
        "Interés Simple ($)": [vp_input * (1 + tasa_input * t) for t in range(0, n_input + 1)],
        "Interés Compuesto ($)": [vp_input * ((1 + tasa_input) ** t) for t in range(0, n_input + 1)]
    })
    
    st.markdown("#### Resultados Proyectados")
    mc1, mc2, mc3 = st.columns(3)
    mc1.metric("Valor Futuro (Simple)", fmt_m(vf_simple))
    mc2.metric("Valor Futuro (Compuesto)", fmt_m(vf_compuesto))
    mc3.metric("Diferencia por Capitalización", fmt_m(vf_compuesto - vf_simple))
    
    st.line_chart(res_df.set_index("Periodo"))
    
    st.markdown("---")
    st.subheader("📝 Resolutor de Casos Complejos del Curso")
    prob_sel = st.selectbox("Selecciona un Caso Práctico:", [
        "Caso 1: Matrimonio y Fondo de $25.000.000 (Simple 0,8% vs Compuesto 0,75%)",
        "Caso 2: Inversión de $75.000.000 dividida en dos depósitos",
        "Caso 3: Inversión de $980.000.000 en Banco A y B para ganar $5.500.000/mes",
        "Caso 4: Igualación de Flujos (Deuda de $70M al 3,5% vs Inversión $50M al 7%)",
        "Caso 5: División de Capital $33.000.000 al 12% y 9% simple"
    ])
    
    if "Caso 1:" in prob_sel:
        vf_mat_a = 25000000 * (1 + 0.008 * 60)
        vf_mat_b = 25000000 * ((1 + 0.0075) ** 60)
        st.write(f"• **Opción A (Simple 0,80%):** $VF = {fmt_m(25000000)} \times (1 + 0,008 \times 60) =$ **{fmt_m(vf_mat_a)}**")
        st.write(f"• **Opción B (Compuesto 0,75%):** $VF = {fmt_m(25000000)} \times (1 + 0,0075)^{{60}} =$ **{fmt_m(vf_mat_b)}**")
        st.success(f"✅ Conviene la **Opción B (Interés Compuesto)** por una diferencia a favor de **{fmt_m(vf_mat_b - vf_mat_a)}**.")
    elif "Caso 2:" in prob_sel:
        st.write(f"• **Depósito 1 ({fmt_m(45000000)} al 0,90% mensual simple por 18 meses):** {fmt_m(45000000 * (1 + 0.009 * 18))}")
        st.write(f"• **Depósito 2 ({fmt_m(30000000)} al 0,85% mensual compuesto por 18 meses):** {fmt_m(30000000 * ((1 + 0.0085)**18))}")
        st.success(f"✅ **Monto Total Acumulado:** **{fmt_m(45000000 * (1 + 0.009 * 18) + 30000000 * ((1 + 0.0085)**18))}**")
    elif "Caso 3:" in prob_sel:
        y_val = (5500000 - 0.0042 * 980000000) / (0.0070 - 0.0042)
        x_val = 980000000 - y_val
        st.write(f"• **Banco A (5,04% anual simple = 0,42% mens):** {fmt_m(x_val)}")
        st.write(f"• **Banco B (2,10% trimestral simple = 0,70% mens):** {fmt_m(y_val)}")
        st.success(f"✅ **Interés mensual generado:** {fmt_m(x_val * 0.0042 + y_val * 0.0070)}")
    elif "Caso 4:" in prob_sel:
        n_eq = math.log(70000000 / 50000000) / math.log(1.07 / 1.035)
        st.write(f"• **Ecuación:** $50M \times (1,07)^n = 70M \times (1,035)^n \\Rightarrow n = {fmt_n(n_eq, 2)}$ meses")
        st.success(f"✅ **Plazo de Igualación:** **{fmt_n(n_eq, 2)} meses** ({fmt_n(n_eq*30, 0)} días)")
    else:
        st.write(f"• **Tercio al 12% anual simple por 2 años ({fmt_m(11000000)}):** Interés = {fmt_m(11000000 * 0.12 * 2)}")
        st.write(f"• **Dos tercios al 9% anual simple por 2 años ({fmt_m(22000000)}):** Interés = {fmt_m(22000000 * 0.09 * 2)}")
        st.success(f"✅ **Interés Total Combinado:** **{fmt_m(11000000 * 0.12 * 2 + 22000000 * 0.09 * 2)}**")

# ==========================================
# MÓDULO 3: CONVERSIÓN DE TASAS
# ==========================================
elif modulo == "3. Conversión de Tasas (TNA/TEA)":
    st.header("Unidad 3: Conversión y Decodificación de Tasas")
    
    col_t1, col_t2 = st.columns(2)
    
    with col_t1:
        st.subheader("🔄 Conversor TNA ➔ TEA")
        tna_val = num_input_fmt("Tasa Nominal Anual (TNA %):", 24.0, "m3_tna", is_currency=False) / 100.0
        freq_dict = {
            "Mensual (m=12)": 12,
            "Bimestral (m=6)": 6,
            "Trimestral (m=4)": 4,
            "Semestral (m=2)": 2,
            "Diaria (m=360)": 360,
            "Diaria (m=365)": 365
        }
        freq_sel = st.selectbox("Frecuencia de Capitalización (m):", list(freq_dict.keys()))
        m_val = freq_dict[freq_sel]
        
        i_per = tna_val / m_val
        tea_calc = ((1 + i_per) ** m_val) - 1.0
        
        st.write(f"• **Tasa Periódica ($i'$):** {fmt_n(i_per*100, 4)}%")
        st.metric("Tasa Efectiva Anual (TEA Equiv)", f"{fmt_n(tea_calc*100, 4)}%")

    with col_t2:
        st.subheader("⚖️ Comparador Banco X vs. Banco Y")
        st.markdown(f"""
        - **Banco X:** 9,00% TNA con capitalización trimestral ($m=4$).
        - **Banco Y:** 9,20% TEA directa.
        """)
        tea_x = ((1 + 0.09/4)**4) - 1.0
        tea_y = 0.092
        
        st.write(f"• **TEA Banco X:** $(1 + 0,09/4)^4 - 1 =$ **{fmt_n(tea_x*100, 4)}%**")
        st.write(f"• **TEA Banco Y:** **{fmt_n(tea_y*100, 4)}%**")
        st.success(f"✅ **Para Invertir:** Conviene **Banco X** ({fmt_n(tea_x*100, 2)}% TEA).\n\n✅ **Para Crédito:** Conviene **Banco Y** (9,20% TEA).")

# ==========================================
# MÓDULO 4: ANUALIDADES
# ==========================================
elif modulo == "4. Anualidades y Amortización":
    st.header("Unidad 4: Anualidades y Tablas de Amortización")
    
    st.subheader("💳 Simulador de Préstamos y Amortización (Método Francés)")
    
    ac1, ac2, ac3 = st.columns(3)
    with ac1:
        monto_prestamo = num_input_fmt("Monto del Préstamo ($):", 30000.0, "m4_monto")
    with ac2:
        tasa_mensual_anu = num_input_fmt("Tasa Efectiva Mensual (%):", 1.2, "m4_tasa", is_currency=False) / 100.0
    with ac3:
        plazo_meses = int(num_input_fmt("Plazo en Meses (n):", 36, "m4_plazo", is_currency=False))
        
    cuota_fija = monto_prestamo * (tasa_mensual_anu / (1 - (1 + tasa_mensual_anu)**(-plazo_meses)))
    st.metric("Cuota Mensual Calculada (R)", fmt_m(cuota_fija))
    
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
    st.dataframe(df_amort.style.format({
        "Saldo Inicial": lambda v: fmt_m(v),
        "Cuota ($)": lambda v: fmt_m(v),
        "Interés ($)": lambda v: fmt_m(v),
        "Amortización ($)": lambda v: fmt_m(v),
        "Saldo Final": lambda v: fmt_m(v)
    }), height=300)
    
    st.bar_chart(df_amort.set_index("Mes")[["Interés ($)", "Amortización ($)"]])

# ==========================================
# MÓDULO 5: GRADIENTES
# ==========================================
elif modulo == "5. Gradientes Financieros":
    st.header("Unidad 5: Gradientes Financieros (Series Variables)")
    
    st.subheader("📈 Comparativa de Series: Constante vs Aritmética vs Geométrica")
    
    gc1, gc2, gc3 = st.columns(3)
    with gc1:
        base_a = num_input_fmt("Flujo Base Inicial (A):", 1000.0, "m5_base")
    with gc2:
        grad_g = num_input_fmt("Gradiente Aritmético (G $):", 200.0, "m5_grad_g")
    with gc3:
        grad_pct = num_input_fmt("Gradiente Geométrico (g %):", 10.0, "m5_grad_pct", is_currency=False) / 100.0
        
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
    vp_perpetuidad_4 = 800000 / (0.12 - 0.05)
    vp_hoy_0 = vp_perpetuidad_4 / ((1 + 0.12)**4)
    st.write(f"• **Valor Presente en Año 4 ($VP_4$):** {fmt_m(800000)} / (0,12 - 0,05) = **{fmt_m(vp_perpetuidad_4)}**")
    st.write(f"• **Valor Presente Hoy ($VP_0$):** {fmt_m(vp_perpetuidad_4)} / (1,12)^4 = **{fmt_m(vp_hoy_0)}**")

# ==========================================
# MÓDULO 6: PRESUPUESTOS
# ==========================================
elif modulo == "6. Presupuesto y Flujo de Caja":
    st.header("Unidad 6: Presupuestos y Control de Caja Operacional")
    
    st.subheader("📊 Simulador de Presupuesto Mensual a 12 Meses con Inflación")
    
    pc1, pc2, pc3 = st.columns(3)
    with pc1:
        v_base = num_input_fmt("Ventas Mes 1 ($):", 15000.0, "m6_vbase")
    with pc2:
        g_ventas = num_input_fmt("Crecimiento Ventas Mensual (%):", 1.5, "m6_gventas", is_currency=False) / 100.0
    with pc3:
        inf_mensual = num_input_fmt("Inflación Costos Mensual (%):", 0.5, "m6_inf", is_currency=False) / 100.0
        
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
    df_pres["Mes"] = pd.Categorical(df_pres["Mes"], categories=[f"Mes {i}" for i in range(1, meses_p + 1)], ordered=True)
    
    st.dataframe(df_pres.style.format({
        "Ventas ($)": lambda v: fmt_m(v),
        "Total Egresos ($)": lambda v: fmt_m(v),
        "Flujo Neto ($)": lambda v: fmt_m(v),
        "Caja Acumulada ($)": lambda v: fmt_m(v)
    }))
    
    st.bar_chart(df_pres.set_index("Mes")[["Ventas ($)", "Total Egresos ($)"]])

# ==========================================
# MÓDULO 7: EVALUACIÓN DE PROYECTOS
# ==========================================
elif modulo == "7. Evaluación de Proyectos (VAN/TIR)":
    st.header("Unidad 7: Evaluación Financiera de Proyectos")
    
    st.subheader("🎯 Punto de Equilibrio Operacional")
    eq1, eq2, eq3 = st.columns(3)
    with eq1:
        cf_val = num_input_fmt("Costos Fijos Totales ($):", 120000.0, "m7_cf")
    with eq2:
        p_val = num_input_fmt("Precio Unitario ($):", 50.0, "m7_p")
    with eq3:
        cv_val = num_input_fmt("Costo Variable Unitario ($):", 30.0, "m7_cv")
        
    mc_unit = p_val - cv_val
    if mc_unit > 0:
        q_eq = cf_val / mc_unit
        ing_eq = q_eq * p_val
        st.success(f"• **Punto de Equilibrio en Unidades:** **{fmt_n(q_eq, 0)} unidades**")
        st.success(f"• **Ingreso de Equilibrio:** **{fmt_m(ing_eq)}**")
    else:
        st.error("El precio unitario debe ser mayor al costo variable.")
        
    st.markdown("---")
    st.subheader("💰 Evaluación de Flujos de Caja (VAN y TIR)")
    
    inv_ini = num_input_fmt("Inversión Inicial ($):", 500000.0, "m7_inv")
    tmar_val = num_input_fmt("Tasa de Descuento / TMAR (%):", 10.0, "m7_tmar", is_currency=False) / 100.0
    
    st.write("Ingresa los flujos proyectados a 5 años:")
    fc_cols = st.columns(5)
    flujos = []
    for idx, col in enumerate(fc_cols):
        with col:
            f_val = num_input_fmt(f"Año {idx+1} ($):", 140000.0 + idx*10000.0, f"m7_f{idx+1}")
            flujos.append(f_val)
            
    van_val = npf.npv(tmar_val, [0] + flujos) - inv_ini
    tir_val = npf.irr([-inv_ini] + flujos)
    
    col_v1, col_v2 = st.columns(2)
    col_v1.metric("Valor Actual Neto (VAN)", fmt_m(van_val), delta="Viable" if van_val > 0 else "No Viable")
    col_v2.metric("Tasa Interna de Retorno (TIR)", f"{fmt_n(tir_val*100, 2)}%", delta="TIR > TMAR" if tir_val > tmar_val else "TIR < TMAR")

# ==========================================
# MÓDULO 8: CALCULADORAS ESPECIALIZADAS
# ==========================================
elif modulo == "8. Calculadoras Especializadas":
    st.header("Módulo 8: Calculadoras Especializadas")
    st.markdown("Herramientas cuantitativas para cálculo exacto de operaciones financieras del curso.")
    
    calc_opt = st.selectbox("Selecciona la Calculadora Especializada:", [
        "1. Valor Futuro con Interés Compuesto (Plazos Enteros y Fraccionados)",
        "2. Valor Futuro de la Cuota / Anualidad (VF Ordinaria y Anticipada)",
        "3. Valor Futuro y Valor Presente de Flujos Múltiples / Irregulares",
        "4. Desglose de Interés y Amortización para una Cuota Específica (k)",
        "5. Despeje de Plazo Requerido y Tasa Implícita",
        "6. Conversión de Tasas Nominales/Efectivas y Spread Financiero"
    ])
    
    st.markdown("---")
    
    if "1. Valor Futuro con Interés Compuesto" in calc_opt:
        st.subheader("1. Valor Futuro con Interés Compuesto")
        sc1, sc2, sc3 = st.columns(3)
        with sc1:
            s1_vp = num_input_fmt("Capital Inicial (VP):", 1000.0, "s1_vp")
        with sc2:
            s1_tasa = num_input_fmt("Tasa Anual Efectiva (%):", 5.0, "s1_tasa", is_currency=False) / 100.0
        with sc3:
            s1_meses = num_input_fmt("Plazo en Meses (n):", 16.0, "s1_meses", is_currency=False)
            
        s1_vf = s1_vp * ((1 + s1_tasa) ** (s1_meses / 12.0))
        st.metric("Valor Futuro Resultante (VF)", fmt_m(s1_vf))
        st.info(f"Fórmula aplicada: $VF = {fmt_m(s1_vp)} \times (1 + {fmt_n(s1_tasa*100, 2)}\\%)^{{({fmt_n(s1_meses, 0)}/12)}} = {fmt_m(s1_vf)}$")

    elif "2. Valor Futuro de la Cuota" in calc_opt:
        st.subheader("2. Valor Futuro de la Cuota / Anualidad")
        ac1, ac2, ac3, ac4 = st.columns(4)
        with ac1:
            s2_renta = num_input_fmt("Cuota Periódica (R):", 500.0, "s2_renta")
        with ac2:
            s2_tasa = num_input_fmt("Tasa Periódica (%):", 0.8, "s2_tasa", is_currency=False) / 100.0
        with ac3:
            s2_n = int(num_input_fmt("Número de Cuotas (n):", 300, "s2_n", is_currency=False))
        with ac4:
            s2_tipo = st.selectbox("Tipo de Anualidad:", ["Ordinaria (Vencida)", "Anticipada"])
            
        vf_ord = s2_renta * (((1 + s2_tasa)**s2_n - 1) / s2_tasa)
        vf_final = vf_ord * (1 + s2_tasa) if "Anticipada" in s2_tipo else vf_ord
        
        st.metric(f"Valor Futuro Acumulado ({s2_tipo})", fmt_m(vf_final))
        st.write(f"• **Total Aportado en Cuotas:** {fmt_m(s2_renta * s2_n)}")
        st.write(f"• **Intereses Ganados:** {fmt_m(vf_final - s2_renta * s2_n)}")

    elif "3. Valor Futuro y Valor Presente de Flujos Múltiples" in calc_opt:
        st.subheader("3. Flujos Múltiples / Irregulares (VP y VF)")
        mc1, mc2 = st.columns(2)
        with mc1:
            sf_tasa = num_input_fmt("Tasa de Descuento/Interés Periódica (%):", 12.0, "sf_tasa", is_currency=False) / 100.0
        with mc2:
            sf_num = int(num_input_fmt("Número de Flujos (N):", 4, "sf_num", is_currency=False))
            
        f_list = []
        f_cols = st.columns(min(sf_num, 5))
        for i in range(sf_num):
            with f_cols[i % len(f_cols)]:
                f_val = num_input_fmt(f"Flujo en t={i+1} ($):", 100.0 + i*20.0, f"sf_f_{i}")
                f_list.append(f_val)
                
        vp_mult = sum(f / ((1 + sf_tasa)**(t+1)) for t, f in enumerate(f_list))
        vf_mult = sum(f * ((1 + sf_tasa)**(sf_num - (t+1))) for t, f in enumerate(f_list))
        
        m_res1, m_res2 = st.columns(2)
        m_res1.metric("Valor Presente Total (VP en t=0)", fmt_m(vp_mult))
        m_res2.metric("Valor Futuro Total (VF en t=N)", fmt_m(vf_mult))

    elif "4. Desglose de Interés y Amortización" in calc_opt:
        st.subheader("4. Desglose de Interés y Amortización para una Cuota Específica (k)")
        k1, k2, k3, k4 = st.columns(4)
        with k1:
            k_monto = num_input_fmt("Monto del Préstamo ($):", 1000000.0, "k_monto")
        with k2:
            k_tasa = num_input_fmt("Tasa Periódica (%):", 18.0, "k_tasa", is_currency=False) / 100.0
        with k3:
            k_n = int(num_input_fmt("Plazo Total (n):", 5, "k_n", is_currency=False))
        with k4:
            k_target = int(num_input_fmt("Cuota a Analizar (k):", 4, "k_target", is_currency=False))
            
        cuota_k = k_monto * (k_tasa / (1 - (1 + k_tasa)**(-k_n)))
        saldo_curr = k_monto
        for period in range(1, k_target):
            int_p = saldo_curr * k_tasa
            cap_p = cuota_k - int_p
            saldo_curr -= cap_p
            
        int_k = saldo_curr * k_tasa
        cap_k = cuota_k - int_k
        saldo_post = saldo_curr - cap_k
        
        st.success(f"📌 **Resultados para la Cuota N° {k_target}:**")
        rk1, rk2, rk3, rk4 = st.columns(4)
        rk1.metric("Saldo Inicial Periodo k", fmt_m(saldo_curr))
        rk2.metric("Interés de la Cuota k", fmt_m(int_k))
        rk3.metric("Amortización de Capital k", fmt_m(cap_k))
        rk4.metric("Saldo Final Tras Cuota k", fmt_m(saldo_post))

    elif "5. Despeje de Plazo Requerido" in calc_opt:
        st.subheader("5. Despeje de Plazo Requerido (n) y Tasa Implícita")
        p1, p2, p3 = st.columns(3)
        with p1:
            s2_vp = num_input_fmt("Capital Inicial (VP):", 2000.0, "s2_vp_p")
        with p2:
            s2_vf = num_input_fmt("Valor Futuro Deseado (VF):", 3525.0, "s2_vf_p")
        with p3:
            s2_tasa = num_input_fmt("Tasa Anual (%):", 12.0, "s2_tasa_p", is_currency=False) / 100.0
            
        if s2_vf > s2_vp and s2_tasa > 0:
            n_calc = math.log(s2_vf / s2_vp) / math.log(1 + s2_tasa)
            st.metric("Plazo Requerido (n)", f"{fmt_n(n_calc, 2)} periodos/años")
            st.info(f"Fórmula aplicada: n = ln({fmt_m(s2_vf)} / {fmt_m(s2_vp)}) / ln(1 + {fmt_n(s2_tasa*100, 2)}%)")

    else:
        st.subheader("6. Conversión de Tasas Nominales/Efectivas y Spread Financiero")
        t1, t2, t3 = st.columns(3)
        with t1:
            sp_tna = num_input_fmt("Tasa Nominal Anual (TNA %):", 24.0, "sp_tna", is_currency=False) / 100.0
        with t2:
            sp_m = int(num_input_fmt("Capitalizaciones por Año (m):", 4, "sp_m", is_currency=False))
        with t3:
            sp_ref = num_input_fmt("Tasa Referencia de Mercado (%):", 22.0, "sp_ref", is_currency=False) / 100.0
            
        tea_res = ((1 + sp_tna / sp_m) ** sp_m) - 1.0
        spread = tea_res - sp_ref
        
        st.metric("Tasa Efectiva Anual (TEA Equiv)", f"{fmt_n(tea_res*100, 4)}%")
        st.metric("Spread / Diferencial vs Referencia", f"{fmt_n(spread*100, 4)}%", delta=f"{fmt_n(spread*100, 2)}% p.p.")

st.markdown("---")
st.caption("04 Finanzas App Web — Generado automáticamente para Gemini Notebook")
