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
    .val-badge {
        background-color: #E2EFDA;
        color: #276A3C;
        padding: 4px 8px;
        border-radius: 4px;
        font-size: 0.88rem;
        font-weight: 600;
        margin-top: -10px;
        margin-bottom: 10px;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

# Helper de formateo numérico
def fmt_m(val, dec=2):
    try:
        val_f = float(val)
        s = f"{val_f:,.{dec}f}"
        s = s.replace(",", "X").replace(".", ",").replace("X", ".")
        return f"${s}"
    except:
        return f"${val}"

def fmt_n(val, dec=2):
    try:
        val_f = float(val)
        s = f"{val_f:,.{dec}f}"
        s = s.replace(",", "X").replace(".", ",").replace("X", ".")
        return s
    except:
        return str(val)

# Helper de conversión de frecuencia de periodos por año
FREQ_DICT = {
    "Mensual (12/año)": 12,
    "Bimestral (6/año)": 6,
    "Trimestral (4/año)": 4,
    "Cuatrimestral (3/año)": 3,
    "Semestral (2/año)": 2,
    "Anual (1/año)": 1,
    "Diario (360/año)": 360,
    "Diario (365/año)": 365
}

def convertir_tasa(tasa_val, tipo_origen, freq_origen_m, freq_destino_m):
    """
    Convierte cualquier tasa (Periódica, TNA o TEA) de una frecuencia de origen
    a la tasa periódica exacta de la frecuencia de destino.
    Cero cálculos externos para el usuario.
    """
    if tipo_origen == "Tasa Efectiva Anual (TEA %)":
        tea = tasa_val
    elif tipo_origen == "Tasa Nominal Anual (TNA %)":
        tea = ((1 + tasa_val / freq_origen_m) ** freq_origen_m) - 1.0
    else: # Tasa Periódica Directa (%)
        tea = ((1 + tasa_val) ** freq_origen_m) - 1.0
    
    # Tasa periódica en la frecuencia de destino
    i_destino = ((1 + tea) ** (1.0 / freq_destino_m)) - 1.0
    return i_destino, tea

# Encabezado Principal
st.markdown('<div class="main-header">04 FINANZAS — Solucionario Web & Simulación Financiera</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Plataforma integral basada en contenidos, guías, talleres y evaluaciones. Sistema 100% libre de cálculos externos.</div>', unsafe_allow_html=True)

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
st.sidebar.info("💡 **Tip:** Todos los módulos convierten automáticamente frecuencias de tasa y periodos. Todos los números incluyen separadores de miles.")

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
            "Caso 2: Carlos y la compra a crédito ($600.000)",
            "Caso 3: Presupuesto familiar con imprevisto (15%)",
            "Caso 4: Excedente de caja en Pyme Rápido ($5.000.000)"
        ])
        
        if "Lucía" in caso:
            st.info("**Situación:** Lucía recibe un bono de $500.000 y duda entre gastarlo en vacaciones o depositarlo a plazo fijo al 0,60% mensual.")
            vf_lucia = 500000 * ((1 + 0.006)**12)
            st.success(f"**Recomendación Financiera:** Depositar a plazo. En 12 meses obtendría **{fmt_m(vf_lucia)}** (ganancia neta de {fmt_m(vf_lucia - 500000)}). Prioriza acumulación de capital y VDT.")
        elif "Carlos" in caso:
            st.info("**Situación:** Carlos evalúa comprar una laptop al contado ($600.000) o en 12 cuotas de $62.000 (Total $744.000).")
            st.warning("**Recomendación Financiera:** Comprar al contado si cuenta con liquidez. La alternativa a crédito implica un pago total de $744.000 con un costo financiero implícito superior al 40% anual.")
        elif "Presupuesto" in caso:
            st.info("**Situación:** Familia con ingresos de $1.200.000 sufre un gasto médico imprevisto equivalente al 15% de sus ingresos ($180.000).")
            st.error("**Recomendación Financiera:** Recurrir al fondo de emergencia. Si no existe, reestructurar gastos prescindibles del mes e impedir créditos rotativos de tarjeta de crédito.")
        else:
            st.info("**Situación:** Pyme Rápido tiene $5.000.000 ociosos en la cuenta corriente operativa.")
            st.success("**Recomendación Financiera:** Colocar el 60% ($3.000.000) en pactos diarios o fondos de liquidez inmediata para rentabilizar el saldo sin perder operatividad.")

# ==========================================
# MÓDULO 2: INTERÉS SIMPLE Y COMPUESTO
# ==========================================
elif modulo == "2. Interés Simple y Compuesto":
    st.header("Unidad 2: Interés Simple e Interés Compuesto")
    
    st.subheader("⚙️ Calculadora Interactiva de Interés")
    
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        vp_input = st.number_input("Capital Inicial (VP $):", value=1000000.0, step=50000.0)
        st.markdown(f'<div class="val-badge">💵 VP: {fmt_m(vp_input)}</div>', unsafe_allow_html=True)
    with c2:
        tasa_input = st.number_input("Tasa Periódica (%):", value=1.5, step=0.1) / 100.0
        st.markdown(f'<div class="val-badge">📈 Tasa: {fmt_n(tasa_input*100, 2)}%</div>', unsafe_allow_html=True)
    with c3:
        n_input = st.number_input("Plazo (Periodos):", value=12, min_value=1, max_value=120)
        st.markdown(f'<div class="val-badge">⏳ Plazo: {fmt_n(n_input, 0)} periodos</div>', unsafe_allow_html=True)
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
    st.subheader("📝 Caso Destacado: Matrimonio y Fondo de $25.000.000")
    st.markdown("""
    **Problema:** Un matrimonio dispone de $25.000.000 para invertir durante 5 años (60 meses).
    - Opción A: Interés Simple al 0,80% mensual.
    - Opción B: Interés Compuesto al 0,75% mensual.
    """)
    vf_mat_a = 25000000 * (1 + 0.008 * 60)
    vf_mat_b = 25000000 * ((1 + 0.0075) ** 60)
    
    st.write(f"- **Opción A (Simple 0,80%):** VF = $25.000.000 × (1 + 0,008 × 60) = **{fmt_m(vf_mat_a)}**")
    st.write(f"- **Opción B (Compuesto 0,75%):** VF = $25.000.000 × (1 + 0,0075)^60 = **{fmt_m(vf_mat_b)}**")
    if vf_mat_b > vf_mat_a:
        st.success(f"✅ Conviene la **Opción B (Interés Compuesto)** por una diferencia a favor de **{fmt_m(vf_mat_b - vf_mat_a)}** gracias a la reinversión de intereses.")
    else:
        st.success(f"✅ Conviene la **Opción A (Interés Simple)** por una diferencia a favor de **{fmt_m(vf_mat_a - vf_mat_b)}**.")

# ==========================================
# MÓDULO 3: CONVERSIÓN DE TASAS
# ==========================================
elif modulo == "3. Conversión de Tasas (TNA/TEA)":
    st.header("Unidad 3: Conversión y Decodificación de Tasas")
    
    col_t1, col_t2 = st.columns(2)
    
    with col_t1:
        st.subheader("🔄 Conversor TNA ➔ TEA")
        tna_val = st.number_input("Tasa Nominal Anual (TNA %):", value=24.0, step=0.5) / 100.0
        st.markdown(f'<div class="val-badge">📈 TNA: {fmt_n(tna_val*100, 2)}%</div>', unsafe_allow_html=True)
        freq_sel = st.selectbox("Frecuencia de Capitalización (m):", list(FREQ_DICT.keys()))
        m_val = FREQ_DICT[freq_sel]
        
        i_per = tna_val / m_val
        tea_calc = ((1 + i_per) ** m_val) - 1.0
        
        st.write(f"• **Tasa Periódica ($i$):** {fmt_n(i_per*100, 4)}%")
        st.metric("Tasa Efectiva Anual (TEA Equivalent)", f"{fmt_n(tea_calc*100, 4)}%")

    with col_t2:
        st.subheader("⚖️ Comparador Banco X vs. Banco Y")
        st.markdown("""
        - **Banco X:** 9,00% TNA con capitalización trimestral ($m=4$).
        - **Banco Y:** 9,20% TEA directa.
        """)
        tea_x = ((1 + 0.09/4)**4) - 1.0
        tea_y = 0.092
        
        st.write(f"• **TEA Banco X:** $(1 + 0,09/4)^4 - 1 =$ **{fmt_n(tea_x*100, 4)}%**")
        st.write(f"• **TEA Banco Y:** **{fmt_n(tea_y*100, 4)}%**")
        
        if tea_x > tea_y:
            st.success(f"✅ **Para Invertir/Ahorrar:** Conviene **Banco X** ({fmt_n(tea_x*100, 2)}% TEA).\n\n✅ **Para Solicitar Crédito:** Conviene **Banco Y** (9,20% TEA).")

# ==========================================
# MÓDULO 4: ANUALIDADES
# ==========================================
elif modulo == "4. Anualidades y Amortización":
    st.header("Unidad 4: Anualidades y Tablas de Amortización")
    
    st.subheader("💳 Simulador de Préstamos y Amortización (Método Francés)")
    
    ac1, ac2, ac3 = st.columns(3)
    with ac1:
        monto_prestamo = st.number_input("Monto del Préstamo ($):", value=30000.0, step=1000.0)
        st.markdown(f'<div class="val-badge">💵 Préstamo: {fmt_m(monto_prestamo)}</div>', unsafe_allow_html=True)
    with ac2:
        tasa_mensual_anu = st.number_input("Tasa Efectiva Mensual (%):", value=1.2, step=0.1) / 100.0
        st.markdown(f'<div class="val-badge">📈 Tasa Mensual: {fmt_n(tasa_mensual_anu*100, 2)}%</div>', unsafe_allow_html=True)
    with ac3:
        plazo_meses = st.slider("Plazo en Meses (n):", min_value=6, max_value=60, value=36)
        st.markdown(f'<div class="val-badge">⏳ Plazo: {fmt_n(plazo_meses, 0)} meses</div>', unsafe_allow_html=True)
        
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
        "Saldo Inicial": lambda x: fmt_m(x),
        "Cuota ($)": lambda x: fmt_m(x),
        "Interés ($)": lambda x: fmt_m(x),
        "Amortización ($)": lambda x: fmt_m(x),
        "Saldo Final": lambda x: fmt_m(x)
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
        base_a = st.number_input("Flujo Base Inicial (A $):", value=1000.0, step=100.0)
        st.markdown(f'<div class="val-badge">💵 Base A: {fmt_m(base_a)}</div>', unsafe_allow_html=True)
    with gc2:
        grad_g = st.number_input("Gradiente Aritmético (G $):", value=200.0, step=50.0)
        st.markdown(f'<div class="val-badge">➕ Gradiente G: {fmt_m(grad_g)}</div>', unsafe_allow_html=True)
    with gc3:
        grad_pct = st.number_input("Gradiente Geométrico (g %):", value=10.0, step=1.0) / 100.0
        st.markdown(f'<div class="val-badge">📈 Crecimiento g: {fmt_n(grad_pct*100, 2)}%</div>', unsafe_allow_html=True)
        
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
    st.markdown("""
    - **Inversión Inicial:** $5.000.000 al término del año 4.
    - **Flujo Año 5:** $800.000 con crecimiento perpetuo al $g = 5,00\\%$ anual.
    - **Tasa de Descuento (TMAR):** 12,00% anual.
    """)
    vp_perpetuidad_4 = 800000 / (0.12 - 0.05)
    vp_hoy_0 = vp_perpetuidad_4 / ((1 + 0.12)**4)
    st.write(f"• **Valor Presente en Año 4 ($VP_4$):** $800.000 / (0,12 - 0,05) = **{fmt_m(vp_perpetuidad_4)}**")
    st.write(f"• **Valor Presente Hoy ($VP_0$):** {fmt_m(vp_perpetuidad_4)} / (1,12)^4 = **{fmt_m(vp_hoy_0)}**")

# ==========================================
# MÓDULO 6: PRESUPUESTOS
# ==========================================
elif modulo == "6. Presupuesto y Flujo de Caja":
    st.header("Unidad 6: Presupuestos y Control de Caja Operacional")
    
    st.subheader("📊 Simulador de Presupuesto Mensual a 12 Meses con Inflación")
    
    pc1, pc2, pc3 = st.columns(3)
    with pc1:
        v_base = st.number_input("Ventas Mes 1 ($):", value=15000.0, step=1000.0)
        st.markdown(f'<div class="val-badge">💵 Ventas M1: {fmt_m(v_base)}</div>', unsafe_allow_html=True)
    with pc2:
        g_ventas = st.number_input("Crecimiento Ventas Mensual (%):", value=1.5, step=0.1) / 100.0
        st.markdown(f'<div class="val-badge">📈 Crecimiento: {fmt_n(g_ventas*100, 2)}%</div>', unsafe_allow_html=True)
    with pc3:
        inf_mensual = st.number_input("Inflación Costos Mensual (%):", value=0.5, step=0.1) / 100.0
        st.markdown(f'<div class="val-badge">🏷️ Inflación: {fmt_n(inf_mensual*100, 2)}%</div>', unsafe_allow_html=True)
        
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
        "Ventas ($)": lambda x: fmt_m(x),
        "Total Egresos ($)": lambda x: fmt_m(x),
        "Flujo Neto ($)": lambda x: fmt_m(x),
        "Caja Acumulada ($)": lambda x: fmt_m(x)
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
        cf_val = st.number_input("Costos Fijos Totales ($):", value=120000.0, step=5000.0)
        st.markdown(f'<div class="val-badge">💵 Costos Fijos: {fmt_m(cf_val)}</div>', unsafe_allow_html=True)
    with eq2:
        p_val = st.number_input("Precio Unitario ($):", value=50.0, step=1.0)
        st.markdown(f'<div class="val-badge">🏷️ Precio: {fmt_m(p_val)}</div>', unsafe_allow_html=True)
    with eq3:
        cv_val = st.number_input("Costo Variable Unitario ($):", value=30.0, step=1.0)
        st.markdown(f'<div class="val-badge">📦 CV Unitario: {fmt_m(cv_val)}</div>', unsafe_allow_html=True)
        
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
    
    inv_ini = st.number_input("Inversión Inicial ($):", value=500000.0, step=10000.0)
    st.markdown(f'<div class="val-badge">💵 Inversión Inicial: {fmt_m(inv_ini)}</div>', unsafe_allow_html=True)
    tmar_val = st.number_input("Tasa de Descuento / TMAR (%):", value=10.0, step=0.5) / 100.0
    st.markdown(f'<div class="val-badge">📈 TMAR: {fmt_n(tmar_val*100, 2)}%</div>', unsafe_allow_html=True)
    
    st.write("Ingresa los flujos proyectados a 5 años:")
    fc_cols = st.columns(5)
    flujos = []
    for idx, col in enumerate(fc_cols):
        with col:
            f_val = st.number_input(f"Año {idx+1} ($):", value=140000.0 + idx*10000.0, step=5000.0)
            st.markdown(f'<div class="val-badge">F{idx+1}: {fmt_m(f_val)}</div>', unsafe_allow_html=True)
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
    st.header("Módulo 8: Calculadoras Especializadas (Solucionador Financiero Universal)")
    st.info("💡 **Cero cálculos externos:** Esta suite convierte automáticamente cualquier frecuencia de tasa (mensual, cuatrimestral, semestral, TNA, TEA) a la frecuencia de las cuotas y ajusta plazos.")

    calc_mode = st.selectbox(
        "Selecciona la Herramienta de Cálculo:",
        [
            "I. Desglose de Interés y Amortización para Cuota Específica (k) [Con Conversor Automático de Tasa Cuatrimestral/Mensual]",
            "II. Valor Futuro y Valor Presente de Interés Compuesto",
            "III. Valor Futuro y Valor Presente de Anualidades (Ordinarias, Anticipadas, Diferidas)",
            "IV. Valor Presente (VP) y Valor Futuro (VF) de Flujos Múltiples e Irregulares",
            "V. Despeje Logarítmico de Plazo (n) y Tasa Implícita (i)",
            "VI. Conversor Universal de Tasas y Spread Financiero"
        ]
    )

    # ---------------------------------------------------------
    # TOOL I: DESGLOSE DE CUOTA ESPECÍFICA (k)
    # ---------------------------------------------------------
    if "I. Desglose" in calc_mode:
        st.subheader("🛠️ Desglose de Interés, Amortización y Saldo para la Cuota k")
        st.markdown("Permite ingresar tasas en **cualquier periodicidad** (cuatrimestral, mensual, semestral, TNA, TEA) y cuotas en **cualquier frecuencia**, realizando la conversión en tiempo real.")

        c1, c2 = st.columns(2)
        with c1:
            monto_credito = st.number_input("Monto Principal del Préstamo (VP $):", value=74000000.0, step=1000000.0)
            st.markdown(f'<div class="val-badge">💵 Capital: {fmt_m(monto_credito)}</div>', unsafe_allow_html=True)
            
            tipo_tasa_in = st.selectbox("Tipo de Tasa Ingresada:", ["Tasa Periódica Directa (%)", "Tasa Nominal Anual (TNA %)", "Tasa Efectiva Anual (TEA %)"])
            tasa_val_in = st.number_input("Valor de la Tasa Ingresada (%):", value=7.45, step=0.1) / 100.0
            st.markdown(f'<div class="val-badge">📈 Tasa Ingresada: {fmt_n(tasa_val_in*100, 4)}%</div>', unsafe_allow_html=True)
            
            freq_tasa_in = st.selectbox("Periodicidad de la Tasa Ingresada:", list(FREQ_DICT.keys()), index=3) # Cuatrimestral default
            
        with c2:
            freq_pago_in = st.selectbox("Periodicidad de Pago de las Cuotas:", list(FREQ_DICT.keys()), index=0) # Mensual default
            
            plazo_unidad = st.selectbox("Unidad de Plazo Total:", ["Meses", "Años", "Cuatrimestres", "Trimestres", "Semestres"])
            plazo_cant = st.number_input(f"Plazo Total ({plazo_unidad}):", value=60 if plazo_unidad=="Meses" else 5, min_value=1)
            st.markdown(f'<div class="val-badge">⏳ Plazo: {fmt_n(plazo_cant, 0)} {plazo_unidad}</div>', unsafe_allow_html=True)
            
            cuota_k = st.number_input("Número de Cuota a Evaluar (k):", value=8, min_value=1)
            st.markdown(f'<div class="val-badge">📌 Evaluar Cuota #: {fmt_n(cuota_k, 0)}</div>', unsafe_allow_html=True)

        # Conversiones automáticas
        m_tasa = FREQ_DICT[freq_tasa_in]
        m_pago = FREQ_DICT[freq_pago_in]

        # Tasa periódica por pago de cuota
        i_cuota, tea_equivalente = convertir_tasa(tasa_val_in, tipo_tasa_in, m_tasa, m_pago)

        # Calcular n total de cuotas
        if plazo_unidad == "Años":
            n_total_cuotas = int(plazo_cant * m_pago)
        elif plazo_unidad == "Meses":
            n_total_cuotas = int(plazo_cant * (m_pago / 12.0))
        elif plazo_unidad == "Cuatrimestres":
            n_total_cuotas = int(plazo_cant * (m_pago / 3.0))
        elif plazo_unidad == "Trimestres":
            n_total_cuotas = int(plazo_cant * (m_pago / 4.0))
        else: # Semestres
            n_total_cuotas = int(plazo_cant * (m_pago / 2.0))

        if cuota_k > n_total_cuotas:
            st.error(f"La cuota k ({cuota_k}) no puede ser mayor al número total de cuotas del crédito ({n_total_cuotas}).")
        else:
            # Renta R
            r_cuota = monto_credito * (i_cuota / (1 - (1 + i_cuota)**(-n_total_cuotas)))

            # Simulación hasta la cuota k
            saldo_act = monto_credito
            for p in range(1, cuota_k + 1):
                int_p = saldo_act * i_cuota
                amort_p = r_cuota - int_p
                saldo_ini_p = saldo_act
                saldo_act = max(0.0, saldo_act - amort_p)

            st.markdown("---")
            st.subheader(f"📊 Desglose Oficial para la Cuota #{cuota_k}")

            res_col1, res_col2, res_col3, res_col4 = st.columns(4)
            res_col1.metric("Cuota Fija a Pagar (R)", fmt_m(r_cuota))
            res_col2.metric(f"Interés del Período {cuota_k}", fmt_m(int_p))
            res_col3.metric(f"Amortización de Capital {cuota_k}", fmt_m(amort_p))
            res_col4.metric(f"Saldo Insoluto Final ({cuota_k})", fmt_m(saldo_act))

            st.info(f"""
            💡 **Parámetros Convertidos Automáticamente por la Plataforma:**
            - **Tasa Efectiva por Período de Pago ({freq_pago_in}):** **{fmt_n(i_cuota*100, 4)}%** (TEA equivalente: {fmt_n(tea_equivalente*100, 4)}%).
            - **Número Total de Cuotas (n):** **{fmt_n(n_total_cuotas, 0)} pagos**.
            - **Saldo Inicial antes de la cuota {cuota_k}:** **{fmt_m(saldo_ini_p)}**.
            - **Composición del pago {cuota_k}:** {fmt_n((int_p/r_cuota)*100, 2)}% Interés | {fmt_n((amort_p/r_cuota)*100, 2)}% Capital.
            """)

            with st.expander("👁️ Ver Tabla de Amortización Completa"):
                s_temp = monto_credito
                t_rows = []
                for p_idx in range(1, n_total_cuotas + 1):
                    i_temp = s_temp * i_cuota
                    a_temp = r_cuota - i_temp
                    s_fin_temp = max(0.0, s_temp - a_temp)
                    t_rows.append({
                        "Cuota #": p_idx,
                        "Saldo Inicial": s_temp,
                        "Cuota ($)": r_cuota,
                        "Interés ($)": i_temp,
                        "Amortización ($)": a_temp,
                        "Saldo Final": s_fin_temp
                    })
                    s_temp = s_fin_temp
                df_t_all = pd.DataFrame(t_rows)
                st.dataframe(df_t_all.style.format({
                    "Saldo Inicial": lambda x: fmt_m(x),
                    "Cuota ($)": lambda x: fmt_m(x),
                    "Interés ($)": lambda x: fmt_m(x),
                    "Amortización ($)": lambda x: fmt_m(x),
                    "Saldo Final": lambda x: fmt_m(x)
                }))

    # ---------------------------------------------------------
    # TOOL II: VALOR FUTURO Y VALOR PRESENTES
    # ---------------------------------------------------------
    elif "II. Valor Futuro" in calc_mode:
        st.subheader("📈 Calculadora Universal de Interés Compuesto (VF y VP)")
        
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            modo_comp = st.radio("Buscar:", ["Valor Futuro (VF) partiendo de VP", "Valor Presente (VP) partiendo de VF"])
            monto_base = st.number_input("Monto Conocido ($):", value=1000.0, step=100.0)
            st.markdown(f'<div class="val-badge">💵 Monto: {fmt_m(monto_base)}</div>', unsafe_allow_html=True)
            
            tipo_t_c = st.selectbox("Tipo de Tasa:", ["Tasa Periódica Directa (%)", "Tasa Nominal Anual (TNA %)", "Tasa Efectiva Anual (TEA %)"])
            tasa_val_c = st.number_input("Valor Tasa (%):", value=5.0, step=0.1) / 100.0
            freq_t_c = st.selectbox("Frecuencia Tasa:", list(FREQ_DICT.keys()), index=5) # Anual default
            
        with col_c2:
            plazo_u_c = st.selectbox("Unidad del Plazo:", ["Meses", "Años", "Cuatrimestres", "Días (360)"])
            plazo_c_val = st.number_input(f"Plazo ({plazo_u_c}):", value=16 if plazo_u_c=="Meses" else 1, step=1)
            st.markdown(f'<div class="val-badge">⏳ Plazo: {fmt_n(plazo_c_val, 0)} {plazo_u_c}</div>', unsafe_allow_html=True)

        m_t_c = FREQ_DICT[freq_t_c]
        i_per_c, tea_c = convertir_tasa(tasa_val_c, tipo_t_c, m_t_c, m_t_c)

        # Convertir plazo a la frecuencia de la tasa
        if plazo_u_c == "Años":
            n_per_c = plazo_c_val * m_t_c
        elif plazo_u_c == "Meses":
            n_per_c = plazo_c_val * (m_t_c / 12.0)
        elif plazo_u_c == "Cuatrimestres":
            n_per_c = plazo_c_val * (m_t_c / 3.0)
        else: # Días
            n_per_c = plazo_c_val * (m_t_c / 360.0)

        if "Valor Futuro" in modo_comp:
            res_vf = monto_base * ((1 + i_per_c)**n_per_c)
            st.success(f"🎯 **Valor Futuro (VF) Calculado:** **{fmt_m(res_vf)}** (Intereses ganados: {fmt_m(res_vf - monto_base)})")
        else:
            res_vp = monto_base / ((1 + i_per_c)**n_per_c)
            st.success(f"🎯 **Valor Presente (VP) Requerido:** **{fmt_m(res_vp)}** (Descuento total: {fmt_m(monto_base - res_vp)})")

    # ---------------------------------------------------------
    # TOOL III: ANUALIDADES
    # ---------------------------------------------------------
    elif "III. Valor Futuro" in calc_mode:
        st.subheader("🏦 Calculadora Universal de Anualidades (VF y VP)")
        
        col_a1, col_a2 = st.columns(2)
        with col_a1:
            tipo_anu = st.selectbox("Estructura de la Anualidad:", ["Ordinaria / Vencida", "Anticipada", "Diferida / Con Gracia"])
            renta_val = st.number_input("Valor de la Cuota/Renta (R $):", value=500.0, step=50.0)
            st.markdown(f'<div class="val-badge">💵 Renta R: {fmt_m(renta_val)}</div>', unsafe_allow_html=True)
            
            tipo_t_a = st.selectbox("Tipo Tasa:", ["Tasa Periódica Directa (%)", "Tasa Nominal Anual (TNA %)", "Tasa Efectiva Anual (TEA %)"])
            tasa_v_a = st.number_input("Tasa (%):", value=0.8, step=0.1) / 100.0
            freq_t_a = st.selectbox("Periodicidad Tasa:", list(FREQ_DICT.keys()), index=0)
            
        with col_a2:
            freq_c_a = st.selectbox("Periodicidad de Cuotas:", list(FREQ_DICT.keys()), index=0)
            plazo_cant_a = st.number_input("Número Total de Cuotas (n):", value=300, min_value=1)
            st.markdown(f'<div class="val-badge">⏳ Total Cuotas: {fmt_n(plazo_cant_a, 0)}</div>', unsafe_allow_html=True)
            
            gracia_k = 0
            if "Diferida" in tipo_anu:
                gracia_k = st.number_input("Períodos de Gracia (k):", value=36, min_value=1)

        m_t_a = FREQ_DICT[freq_t_a]
        m_c_a = FREQ_DICT[freq_c_a]
        i_cuota_a, _ = convertir_tasa(tasa_v_a, tipo_t_a, m_t_a, m_c_a)

        # Cálculos de Anualidad
        vp_base_a = renta_val * ((1 - (1 + i_cuota_a)**(-plazo_cant_a)) / i_cuota_a)
        vf_base_a = renta_val * (((1 + i_cuota_a)**plazo_cant_a - 1) / i_cuota_a)

        if "Anticipada" in tipo_anu:
            vp_final_a = vp_base_a * (1 + i_cuota_a)
            vf_final_a = vf_base_a * (1 + i_cuota_a)
        elif "Diferida" in tipo_anu:
            vp_final_a = vp_base_a / ((1 + i_cuota_a)**gracia_k)
            vf_final_a = vf_base_a
        else:
            vp_final_a = vp_base_a
            vf_final_a = vf_base_a

        st.markdown("---")
        res_a1, res_a2, res_a3 = st.columns(3)
        res_a1.metric("Valor Presente (VP)", fmt_m(vp_final_a))
        res_a2.metric("Valor Futuro (VF Acumulado)", fmt_m(vf_final_a))
        res_a3.metric("Total Aportado en Cuotas", fmt_m(renta_val * plazo_cant_a))

    # ---------------------------------------------------------
    # TOOL IV: FLUJOS MÚLTIPLES
    # ---------------------------------------------------------
    elif "IV. Valor Presente" in calc_mode:
        st.subheader("📊 Valor Presente y Futuro de Flujos Múltiples e Irregulares")
        
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            num_flujos = st.slider("Número de Flujos:", min_value=2, max_value=10, value=4)
            tasa_flujo = st.number_input("Tasa de Descuento Periódica (%):", value=12.0, step=0.5) / 100.0
            st.markdown(f'<div class="val-badge">📈 Tasa Descuento: {fmt_n(tasa_flujo*100, 2)}%</div>', unsafe_allow_html=True)
            
        with col_f2:
            periodo_unidad_f = st.selectbox("Unidad de los Períodos:", ["Años", "Meses", "Trimestres", "Semestres"])

        st.write("Ingresa el monto de cada flujo:")
        flujo_cols = st.columns(num_flujos)
        flujos_arr = []
        for f_i, f_col in enumerate(flujo_cols):
            with f_col:
                f_monto = st.number_input(f"Flujo {f_i+1} ($):", value=100.0 + f_i*20.0, step=10.0)
                flujos_arr.append(f_monto)

        vp_flujos_tot = sum([f_m / ((1 + tasa_flujo)**(t_i + 1)) for t_i, f_m in enumerate(flujos_arr)])
        vf_flujos_tot = vp_flujos_tot * ((1 + tasa_flujo)**num_flujos)

        st.markdown("---")
        mf1, mf2 = st.columns(2)
        mf1.metric(f"Valor Presente Total (VP en t=0)", fmt_m(vp_flujos_tot))
        mf2.metric(f"Valor Futuro Total (VF en t={num_flujos})", fmt_m(vf_flujos_tot))

    # ---------------------------------------------------------
    # TOOL V: DESPEJE LOGARÍTMICO
    # ---------------------------------------------------------
    elif "V. Despeje" in calc_mode:
        st.subheader("⌛ Despeje Logarítmico de Plazo (n) y Tasa Implícita (i)")
        
        c_l1, c_l2 = st.columns(2)
        with c_l1:
            vp_log = st.number_input("Capital Inicial (VP $):", value=2000.0, step=100.0)
            st.markdown(f'<div class="val-badge">💵 VP: {fmt_m(vp_log)}</div>', unsafe_allow_html=True)
            vf_log = st.number_input("Monto Meta Futuro (VF $):", value=3525.0, step=100.0)
            st.markdown(f'<div class="val-badge">🎯 VF Meta: {fmt_m(vf_log)}</div>', unsafe_allow_html=True)
            
        with c_l2:
            tasa_log = st.number_input("Tasa Periódica (%):", value=12.0, step=0.5) / 100.0
            st.markdown(f'<div class="val-badge">📈 Tasa: {fmt_n(tasa_log*100, 2)}%</div>', unsafe_allow_html=True)

        if vf_log > vp_log and tasa_log > 0:
            n_calc_log = math.log(vf_log / vp_log) / math.log(1 + tasa_log)
            
            st.success(f"🎯 **Plazo Necesario (n):** **{fmt_n(n_calc_log, 2)} períodos**")
            st.info(f"""
            💡 **Equivalencias de Tiempo Calculadas Automáticamente:**
            - **Años:** **{fmt_n(n_calc_log, 2)} años**
            - **Meses:** **{fmt_n(n_calc_log * 12, 1)} meses**
            - **Cuatrimestres:** **{fmt_n(n_calc_log * 3, 2)} cuatrimestres**
            - **Semestres:** **{fmt_n(n_calc_log * 2, 2)} semestres**
            """)

    # ---------------------------------------------------------
    # TOOL VI: CONVERSOR UNIVERSAL DE TASAS
    # ---------------------------------------------------------
    else:
        st.subheader("🔄 Conversor Universal de Tasas y Spread Financiero")
        
        c_conv1, c_conv2 = st.columns(2)
        with c_conv1:
            t_orig_v = st.number_input("Tasa de Origen (%):", value=24.0, step=0.5) / 100.0
            tipo_orig_t = st.selectbox("Tipo de Origen:", ["Tasa Nominal Anual (TNA %)", "Tasa Efectiva Anual (TEA %)", "Tasa Periódica Directa (%)"])
            freq_orig_t = st.selectbox("Frecuencia de Origen:", list(FREQ_DICT.keys()), index=2) # Trimestral
            
        with c_conv2:
            freq_dest_t = st.selectbox("Frecuencia de Destino Deseada:", list(FREQ_DICT.keys()), index=0) # Mensual
            tasa_ref_comp = st.number_input("Tasa de Mercado para Comparar (TEA %):", value=25.0, step=0.5) / 100.0

        m_o = FREQ_DICT[freq_orig_t]
        m_d = FREQ_DICT[freq_dest_t]
        
        i_dest_res, tea_res = convertir_tasa(t_orig_v, tipo_orig_t, m_o, m_d)
        spread_val = (tea_res - tasa_ref_comp) * 100.0

        st.markdown("---")
        tc1, tc2, tc3 = st.columns(3)
        tc1.metric(f"Tasa Periódica Destino ({freq_dest_t})", f"{fmt_n(i_dest_res*100, 4)}%")
        tc2.metric("Tasa Efectiva Anual Equivalente (TEA)", f"{fmt_n(tea_res*100, 4)}%")
        tc3.metric("Spread vs Mercado", f"{fmt_n(spread_val, 2)}%", delta="Superior" if spread_val>0 else "Inferior")

st.markdown("---")
st.caption("04 Finanzas App Web — Generado automáticamente para Gemini Notebook")
