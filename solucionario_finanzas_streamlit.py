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
    .val-badge {
        background-color: #E2EFDA;
        color: #276A3C;
        padding: 4px 10px;
        border-radius: 4px;
        font-weight: 600;
        font-size: 0.9rem;
        margin-top: -10px;
        margin-bottom: 10px;
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

# Helper para formato con separador de miles
def fmt_m(val):
    if val is None:
        return "$0"
    if isinstance(val, (int, float)):
        if abs(val) >= 1000 or val == int(val):
            return f"${val:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        return f"${val:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    return str(val)

def fmt_n(val):
    if isinstance(val, (int, float)):
        if val == int(val):
            return f"{int(val):,}".replace(',', '.')
        return f"{val:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    return str(val)

def parse_num(val_str):
    if not val_str:
        return 0.0
    s = str(val_str).strip().replace('$', '')
    if ',' in s and '.' in s:
        if s.rfind(',') > s.rfind('.'):
            s = s.replace('.', '').replace(',', '.')
        else:
            s = s.replace(',', '')
    elif '.' in s:
        parts = s.split('.')
        if len(parts) > 2 or (len(parts) == 2 and len(parts[1]) != 2):
            s = s.replace('.', '')
    elif ',' in s:
        parts = s.split(',')
        if len(parts) > 2 or (len(parts) == 2 and len(parts[1]) != 2):
            s = s.replace(',', '')
        else:
            s = s.replace(',', '.')
    try:
        return float(s)
    except ValueError:
        return 0.0

def money_input(label, default_val, key):
    if key not in st.session_state:
        st.session_state[key] = fmt_n(default_val)
    
    def on_change():
        parsed = parse_num(st.session_state[key])
        st.session_state[key] = fmt_n(parsed)

    st.text_input(label, key=key, on_change=on_change)
    return parse_num(st.session_state[key])

# Encabezado Principal
st.markdown('<div class="main-header">04 FINANZAS — Plataforma Web & Solucionario Integral</div>', unsafe_allow_html=True)
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
st.sidebar.info("💡 **Tip:** Puedes ingresar montos con o sin puntos (ej: `1200000` o `1.200.000`) y el campo formateará automáticamente la casilla con separadores de miles al presionar Enter.")

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
            "Caso 2: Carlos y la compra a crédito ($600.000 vs 12 cuotas $62.000)",
            "Caso 3: Presupuesto familiar ($1.200.000) con imprevisto (15%)",
            "Caso 4: Excedente de caja en Pyme Rápido ($5.000.000)"
        ])
        
        if "Lucía" in caso:
            st.info(f"**Situación:** Lucía recibe un bono de {fmt_m(500000)} y duda entre gastarlo en vacaciones o depositarlo a plazo fijo al 0,60% mensual.")
            st.success(f"**Recomendación Financiera:** Depositar a plazo o invertir en un fondo mutuo conservador. En 12 meses obtendría {fmt_m(537026)}. Prioriza acumulación de capital y VDT.")
        elif "Carlos" in caso:
            st.info(f"**Situación:** Carlos evalúa comprar una laptop al contado ({fmt_m(600000)}) o en 12 cuotas de {fmt_m(62000)} (Total {fmt_m(744000)}).")
            st.warning(f"**Recomendación Financiera:** Comprar al contado si cuenta con liquidez. La alternativa a crédito implica un costo financiero total (CAE) implícito superior al 40% anual.")
        elif "Presupuesto" in caso:
            st.info(f"**Situación:** Familia con ingresos de {fmt_m(1200000)} sufre un gasto médico imprevisto equivalente al 15% de sus ingresos ({fmt_m(180000)}).")
            st.error(f"**Recomendación Financiera:** Recurrir al fondo de emergencia. Si no existe, reestructurar gastos prescindibles del mes y evitar créditos rotativos de tarjeta.")
        else:
            st.info(f"**Situación:** Pyme Rápido tiene {fmt_m(5000000)} ociosos en la cuenta corriente operativa.")
            st.success(f"**Recomendación Financiera:** Colocar el 60% ({fmt_m(3000000)}) en pactos diarios o fondos de liquidez inmediata para rentabilizar el saldo sin perder operatividad.")

# ==========================================
# MÓDULO 2: INTERÉS SIMPLE Y COMPUESTO
# ==========================================
elif modulo == "2. Interés Simple y Compuesto":
    st.header("Unidad 2: Interés Simple e Interés Compuesto")
    
    st.subheader("⚙️ Calculadora Interactiva de Interés")
    
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        vp_input = money_input("Capital Inicial (VP):", 1000000.0, "m2_vp")
    with c2:
        tasa_input_pct = money_input("Tasa Periódica (%):", 1.5, "m2_tasa")
        tasa_input = tasa_input_pct / 100.0
    with c3:
        n_input_val = money_input("Plazo (Periodos):", 12.0, "m2_n")
        n_input = int(n_input_val) if n_input_val > 0 else 1
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
    st.subheader("📝 Resolución de Casos Complejos del Curso")
    prob_sel = st.selectbox("Selecciona un Ejercicio de las Fuentes:", [
        "Caso 1: Matrimonio y Fondo de $25.000.000 a 5 años (60 meses)",
        "Caso 2: Inversión dividida de $75.000.000 en 2 depósitos",
        "Caso 3: Sistema de Inversión de $980.000.000 en Banco A y Banco B",
        "Caso 4: Igualación de Deuda ($70M al 3,5%) e Inversión ($50M al 7%)",
        "Caso 5: División de Capital $33.000.000 al 12% y 9% simple"
    ])
    
    if "Caso 1:" in prob_sel:
        vf_mat_a = 25000000 * (1 + 0.008 * 60)
        vf_mat_b = 25000000 * ((1 + 0.0075) ** 60)
        st.markdown(f"""
        - **Opción A (Simple 0,80%):** $VF = {fmt_m(25000000)} \times (1 + 0,0080 \times 60) = $ **{fmt_m(vf_mat_a)}**
        - **Opción B (Compuesto 0,75%):** $VF = {fmt_m(25000000)} \times (1 + 0,0075)^{{60}} = $ **{fmt_m(vf_mat_b)}**
        """)
        if vf_mat_b > vf_mat_a:
            st.success(f"✅ Conviene la **Opción B (Interés Compuesto)** por una diferencia a favor de **{fmt_m(vf_mat_b - vf_mat_a)}**.")
    elif "Caso 2:" in prob_sel:
        st.markdown(f"""
        - **Depósito 1 (1/3 = {fmt_m(25000000)}):** $VF_1 = {fmt_m(25000000)} \times (1 + 0,01 \times 8) = {fmt_m(27000000)}$
        - **Depósito 2 (2/3 = {fmt_m(50000000)}):** $VF_2 = {fmt_m(50000000)} \times (1 + 0,0075 \times 12) = {fmt_m(54500000)}$
        - **Monto Total al Final:** ${fmt_m(27000000)} + {fmt_m(54500000)} = $ **{fmt_m(81500000)}**
        """)
    elif "Caso 3:" in prob_sel:
        st.markdown(fr"""
        - **Banco A:** 5,04% anual simple $\Rightarrow i_A = 5,04\% / 12 = 0,42\%$ mensual.
        - **Banco B:** 2,10% trimestral simple $\Rightarrow i_B = 2,10\% / 3 = 0,70\%$ mensual.
        - **Ecuaciones:**
          1) $X + Y = {fmt_m(980000000)}$
          2) $0,0042 X + 0,0070 Y = {fmt_m(5500000)}$
        """)
        y_val = (5500000 - 0.0042 * 980000000) / (0.0070 - 0.0042)
        x_val = 980000000 - y_val
        st.success(f"✅ **Invertir en Banco A (X):** **{fmt_m(x_val)}** | **Invertir en Banco B (Y):** **{fmt_m(y_val)}**")
    elif "Caso 4:" in prob_sel:
        n_meses_eq = math.log(70000000 / 50000000) / math.log(1.07 / 1.035)
        st.markdown(fr"""
        - **Ecuación:** $50.000.000 \times (1,07)^n = 70.000.000 \times (1,035)^n$
        - **Despeje:** $n = \frac{{\ln(70M / 50M)}}{{\ln(1,07 / 1,035)}} = \mathbf{{{n_meses_eq:.2f}\ \text{{meses}}}}\ (\approx 10\ \text{{meses y 4 días}})$
        """)
    elif "Caso 5:" in prob_sel:
        cap_1 = 33000000 / 3
        cap_2 = 33000000 * (2 / 3)
        int_total = cap_1 * 0.12 * 1 + cap_2 * 0.09 * 1
        st.success(f"✅ **Interés Total en 1 Año:** **{fmt_m(int_total)}** (Tasa promedio ponderada: 10,00% anual).")

# ==========================================
# MÓDULO 3: CONVERSIÓN DE TASAS
# ==========================================
elif modulo == "3. Conversión de Tasas (TNA/TEA)":
    st.header("Unidad 3: Conversión y Decodificación de Tasas")
    
    col_t1, col_t2 = st.columns(2)
    
    with col_t1:
        st.subheader("🔄 Conversor TNA ➔ TEA")
        tna_val_pct = money_input("Tasa Nominal Anual (TNA %):", 24.0, "m3_tna")
        tna_val = tna_val_pct / 100.0
        freq_dict = {
            "Mensual (m=12)": 12,
            "Bimestral (m=6)": 6,
            "Trimestral (m=4)": 4,
            "Semestral (m=2)": 2,
            "Diaria (m=360)": 360
        }
        freq_sel = st.selectbox("Frecuencia de Capitalización (m):", list(freq_dict.keys()))
        m_val = freq_dict[freq_sel]
        
        i_per = tna_val / m_val
        tea_calc = ((1 + i_per) ** m_val) - 1.0
        
        st.write(f"• **Tasa Periódica ($i'$):** {i_per*100:.4f}%")
        st.metric("Tasa Efectiva Anual (TEA Equivalent)", f"{tea_calc*100:.4f}%")

    with col_t2:
        st.subheader("⚖️ Comparador Banco X vs. Banco Y")
        st.markdown("""
        - **Banco X:** 9,00% TNA con capitalización trimestral ($m=4$).
        - **Banco Y:** 9,20% TEA directa.
        """)
        tea_x = ((1 + 0.09/4)**4) - 1.0
        tea_y = 0.092
        
        st.write(f"• **TEA Banco X:** $(1 + 0,09/4)^4 - 1 =$ **{tea_x*100:.4f}%**")
        st.write(f"• **TEA Banco Y:** **{tea_y*100:.4f}%**")
        
        if tea_x > tea_y:
            st.success(f"""✅ **Para Invertir/Ahorrar:** Conviene **Banco X** ({tea_x*100:.2f}% TEA).

✅ **Para Solicitar Crédito:** Conviene **Banco Y** (9,20% TEA).""")

# ==========================================
# MÓDULO 4: ANUALIDADES
# ==========================================
elif modulo == "4. Anualidades y Amortización":
    st.header("Unidad 4: Anualidades y Tablas de Amortización")
    
    st.subheader("💳 Simulador de Préstamos y Amortización (Método Francés)")
    
    ac1, ac2, ac3 = st.columns(3)
    with ac1:
        monto_prestamo = money_input("Monto del Préstamo ($):", 30000.0, "m4_monto")
    with ac2:
        tasa_mensual_anu_pct = money_input("Tasa Efectiva Mensual (%):", 1.2, "m4_tasa")
        tasa_mensual_anu = tasa_mensual_anu_pct / 100.0
    with ac3:
        plazo_meses_val = money_input("Plazo en Meses (n):", 36.0, "m4_plazo")
        plazo_meses = int(plazo_meses_val) if plazo_meses_val > 0 else 1
        
    cuota_fija = monto_prestamo * (tasa_mensual_anu / (1 - (1 + tasa_mensual_anu)**(-plazo_meses)))
    
    st.metric("Cuota Mensual Calculada (R)", fmt_m(cuota_fija))
    
    saldo = monto_prestamo
    amort_data = []
    for mes in range(1, plazo_meses + 1):
        interes_mes = saldo * tasa_mensual_anu
        capital_mes = cuota_fija - interes_mes
        saldo_final = max(0.0, saldo - capital_mes)
        amort_data.append({
            "Mes": f"Mes {mes}",
            "Saldo Inicial ($)": saldo,
            "Cuota ($)": cuota_fija,
            "Interés ($)": interes_mes,
            "Amortización ($)": capital_mes,
            "Saldo Final ($)": saldo_final
        })
        saldo = saldo_final
        
    df_amort = pd.DataFrame(amort_data)
    df_amort["Mes"] = pd.Categorical(df_amort["Mes"], categories=[f"Mes {i}" for i in range(1, plazo_meses + 1)], ordered=True)
    
    st.markdown("#### Tabla de Amortización Dinámica")
    st.dataframe(df_amort.style.format({
        "Saldo Inicial ($)": lambda v: fmt_m(v),
        "Cuota ($)": lambda v: fmt_m(v),
        "Interés ($)": lambda v: fmt_m(v),
        "Amortización ($)": lambda v: fmt_m(v),
        "Saldo Final ($)": lambda v: fmt_m(v)
    }), height=300)
    
    st.markdown("#### Descomposición Cuota: Interés vs. Amortización")
    st.bar_chart(df_amort.set_index("Mes")[["Interés ($)", "Amortización ($)"]])

# ==========================================
# MÓDULO 5: GRADIENTES
# ==========================================
elif modulo == "5. Gradientes Financieros":
    st.header("Unidad 5: Gradientes Financieros (Series Variables)")
    
    st.subheader("📈 Comparativa de Series: Constante vs Aritmética vs Geométrica")
    
    gc1, gc2, gc3 = st.columns(3)
    with gc1:
        base_a = money_input("Flujo Base Inicial (A $):", 1000.0, "m5_base")
    with gc2:
        grad_g = money_input("Gradiente Aritmético (G $):", 200.0, "m5_grad_g")
    with gc3:
        grad_pct_val = money_input("Gradiente Geométrico (g %):", 10.0, "m5_grad_pct")
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
    st.subheader("🏗️ Caso Proyecto Planta de Desalinización")
    st.markdown(fr"""
    - **Inversión Inicial:** {fmt_m(5000000)} al término del año 4.
    - **Flujo Año 5:** {fmt_m(800000)} con crecimiento perpetuo al $g = 5,00\%$ anual.
    - **Tasa de Descuento (TMAR):** 12,00% anual.
    """)
    vp_perpetuidad_4 = 800000 / (0.12 - 0.05)
    vp_hoy_0 = vp_perpetuidad_4 / ((1 + 0.12)**4)
    st.write(f"• **Valor Presente en Año 4 ($VP_4$):** ${fmt_m(800000)} / (0,12 - 0,05) = $ **{fmt_m(vp_perpetuidad_4)}**")
    st.write(f"• **Valor Presente Hoy ($VP_0$):** ${fmt_m(vp_perpetuidad_4)} / (1,12)^4 = $ **{fmt_m(vp_hoy_0)}**")

# ==========================================
# MÓDULO 6: PRESUPUESTOS
# ==========================================
elif modulo == "6. Presupuesto y Flujo de Caja":
    st.header("Unidad 6: Presupuestos y Control de Caja Operacional")
    
    st.subheader("📊 Simulador de Presupuesto Mensual a 12 Meses con Inflación")
    
    pc1, pc2, pc3 = st.columns(3)
    with pc1:
        v_base = money_input("Ventas Mes 1 ($):", 15000.0, "m6_vbase")
    with pc2:
        g_ventas_pct = money_input("Crecimiento Ventas Mensual (%):", 1.5, "m6_gventas")
        g_ventas = g_ventas_pct / 100.0
    with pc3:
        inf_mensual_pct = money_input("Inflación Costos Mensual (%):", 0.5, "m6_inf")
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
        cf_val = money_input("Costos Fijos Totales ($):", 120000.0, "m7_cf")
    with eq2:
        p_val = money_input("Precio Unitario ($):", 50.0, "m7_p")
    with eq3:
        cv_val = money_input("Costo Variable Unitario ($):", 30.0, "m7_cv")
        
    mc_unit = p_val - cv_val
    if mc_unit > 0:
        q_eq = cf_val / mc_unit
        ing_eq = q_eq * p_val
        st.success(f"• **Punto de Equilibrio en Unidades:** **{fmt_n(q_eq)} unidades**")
        st.success(f"• **Ingreso de Equilibrio:** **{fmt_m(ing_eq)}**")
    else:
        st.error("El precio unitario debe ser mayor al costo variable.")
        
    st.markdown("---")
    st.subheader("💰 Evaluación de Flujos de Caja (VAN y TIR)")
    
    inv_ini = money_input("Inversión Inicial ($):", 500000.0, "m7_inv")
    tmar_val_pct = money_input("Tasa de Descuento / TMAR (%):", 10.0, "m7_tmar")
    tmar_val = tmar_val_pct / 100.0
    
    st.write("Ingresa los flujos proyectados a 5 años:")
    fc_cols = st.columns(5)
    flujos = []
    for idx, col in enumerate(fc_cols):
        with col:
            f_val = money_input(f"Año {idx+1} ($):", 140000.0 + idx*10000.0, f"m7_f{idx}")
            flujos.append(f_val)
            
    van_val = npf.npv(tmar_val, [0] + flujos) - inv_ini
    tir_val = npf.irr([-inv_ini] + flujos)
    
    col_v1, col_v2 = st.columns(2)
    col_v1.metric("Valor Actual Neto (VAN)", fmt_m(van_val), delta="Viable" if van_val > 0 else "No Viable")
    col_v2.metric("Tasa Interna de Retorno (TIR)", f"{tir_val*100:.2f}%", delta="TIR > TMAR" if tir_val > tmar_val else "TIR < TMAR")

# ==========================================
# MÓDULO 8: CALCULADORAS ESPECIALIZADAS
# ==========================================
elif modulo == "8. Calculadoras Especializadas":
    st.header("Módulo 8: Calculadoras Especializadas")
    
    calc_sel = st.selectbox("Selecciona la Herramienta de Cálculo:", [
        "I. Calculadora de Valor Futuro a Plazos Fraccionados (Meses/Años)",
        "II. Solucionador de Plazo Requerido y Horizonte de Inversión (Despeje de n)",
        "III. Evaluador de Saldo Insoluto de Deuda al Período k",
        "IV. Calculadora de Cuota de Crédito y Carga Financiera (PMT)",
        "V. Conversor Avanzado de Tasas Nominales y Diferenciales (TEA/TNA)"
    ])
    
    if "I." in calc_sel:
        st.subheader("I. Valor Futuro a Plazos Fraccionados")
        sc1, sc2, sc3 = st.columns(3)
        with sc1:
            s1_vp = money_input("Monto Inicial / Principal ($):", 1000.0, "s1_vp")
        with sc2:
            s1_tasa_pct = money_input("Tasa Anual Efectiva (%):", 5.0, "s1_tasa")
            s1_tasa = s1_tasa_pct / 100.0
        with sc3:
            s1_meses = money_input("Plazo en Meses:", 16.0, "s1_meses")
            
        s1_vf = s1_vp * ((1 + s1_tasa) ** (s1_meses / 12.0))
        st.metric("Valor Futuro Proyectado (VF)", fmt_m(s1_vf))
        st.info(fr"Fórmula aplicada: $VF = {fmt_m(s1_vp)} \times (1 + {s1_tasa:.2f})^{{({s1_meses:.0f}/12)}}$")

    elif "II." in calc_sel:
        st.subheader("II. Solucionador de Plazo Requerido (Despeje Logarítmico)")
        sc1, sc2, sc3 = st.columns(3)
        with sc1:
            s2_vp = money_input("Capital Inicial ($):", 2000.0, "s2_vp")
        with sc2:
            s2_vf = money_input("Meta de Valor Futuro ($):", 3525.0, "s2_vf")
        with sc3:
            s2_tasa_pct = money_input("Tasa Anual Efectiva (%):", 12.0, "s2_tasa")
            s2_tasa = s2_tasa_pct / 100.0
            
        if s2_vf > s2_vp and s2_tasa > 0:
            s2_n = math.log(s2_vf / s2_vp) / math.log(1 + s2_tasa)
            st.metric("Tiempo Necesario (Años)", f"{s2_n:.2f} años")
            st.info(fr"Fórmula aplicada: $n = \frac{{\ln({fmt_m(s2_vf)} / {fmt_m(s2_vp)})}}{{\ln(1 + {s2_tasa:.2f})}}$")

    elif "III." in calc_sel:
        st.subheader("III. Evaluador de Saldo Insoluto de Deuda al Período k")
        sc1, sc2, sc3 = st.columns(3)
        with sc1:
            s3_monto = money_input("Monto del Préstamo Original ($):", 1000000.0, "s3_monto")
        with sc2:
            s3_tasa_pct = money_input("Tasa Anual del Crédito (%):", 18.0, "s3_tasa")
            s3_tasa = s3_tasa_pct / 100.0
        with sc3:
            s3_plazo_val = money_input("Plazo Total en Años:", 5.0, "s3_plazo")
            s3_plazo = int(s3_plazo_val) if s3_plazo_val > 0 else 1
            
        s3_pmt = s3_monto * (s3_tasa / (1 - (1 + s3_tasa)**(-s3_plazo)))
        st.write(f"• **Cuota Anual Fija (PMT):** **{fmt_m(s3_pmt)}**")
        
        pagos_k_val = money_input("Número de Pagos Realizados (k):", 3.0, "s3_pagos")
        pagos_k = int(pagos_k_val)
        remanente_n = s3_plazo - pagos_k
        if remanente_n > 0:
            saldo_k = s3_pmt * ((1 - (1 + s3_tasa)**(-remanente_n)) / s3_tasa)
            st.metric(f"Saldo Insoluto al Inicio del Año {pagos_k + 1}", fmt_m(saldo_k))

    elif "IV." in calc_sel:
        st.subheader("IV. Calculadora de Cuota de Crédito (PMT)")
        sc1, sc2, sc3 = st.columns(3)
        with sc1:
            s4_vp = money_input("Monto Solicitado ($):", 1800.0, "s4_vp")
        with sc2:
            s4_tasa_pct = money_input("Tasa Periódica Mensual (%):", 1.25, "s4_tasa")
            s4_tasa = s4_tasa_pct / 100.0
        with sc3:
            s4_n_val = money_input("Número de Cuotas (n):", 36.0, "s4_n")
            s4_n = int(s4_n_val) if s4_n_val > 0 else 1
            
        s4_r = s4_vp * (s4_tasa / (1 - (1 + s4_tasa)**(-s4_n)))
        st.metric("Cuota Periódica Mensual (R)", fmt_m(s4_r))

    else:
        st.subheader("V. Conversor Avanzado de Tasas Nominales y Diferenciales")
        sc1, sc2 = st.columns(2)
        with sc1:
            s5_tna_pct = money_input("Tasa Nominal Anual (TNA %):", 24.0, "s5_tna")
            s5_tna = s5_tna_pct / 100.0
        with sc2:
            s5_m_val = money_input("Frecuencia de Capitalización (m):", 4.0, "s5_m")
            s5_m = int(s5_m_val) if s5_m_val > 0 else 1
            
        s5_tea = ((1 + (s5_tna / s5_m)) ** s5_m) - 1.0
        st.metric("Tasa Efectiva Anual Equivalente (TEA)", f"{s5_tea*100:.4f}%")

st.markdown("---")
st.caption("04 Finanzas App Web — Generado automáticamente para Gemini Notebook")
