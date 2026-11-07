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
st.sidebar.info("💡 **Tip:** Puedes modificar los parámetros de los simuladores en tiempo real para ver cómo cambian los resultados.")

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
            "Caso 1: Lucía y el bono de $500",
            "Caso 2: Carlos y la compra a crédito",
            "Caso 3: Presupuesto familiar con imprevisto (15%)",
            "Caso 4: Excedente de caja en Pyme Rápido"
        ])
        
        if "Lucía" in caso:
            st.info("**Situación:** Lucía recibe un bono de $500.000 y duda entre gastarlo en vacaciones o depositarlo a plazo fijo al 0.6% mensual.")
            st.success("**Recomendación Financiera:** Depositar a plazo o invertir en un fondo mutuo conservador. En 12 meses obtendría $537.026. Prioriza acumulación de capital y VDT.")
        elif "Carlos" in caso:
            st.info("**Situación:** Carlos evalúa comprar una laptop al contado ($600.000) o en 12 cuotas de $62.000 (Total $744.000).")
            st.warning("**Recomendación Financiera:** Comprar al contado si cuenta con liquidez. La alternativa a crédito implica un costo financiero total (CAE) implícito superior al 40% anual.")
        elif "Presupuesto" in caso:
            st.info("**Situación:** Familia con ingresos de $1.200.000 sufre un gasto médico imprevisto equivalente al 15% de sus ingresos ($180.000).")
            st.error("**Recomendación Financiera:** Recurrir al fondo de emergencia. Si no existe, reestructurar gastos prescindibles del mes y evitar créditos rotativos de tarjeta.")
        else:
            st.info("**Situación:** Pyme Rápido tiene $5.000.000 ociosos en la cuenta corriente operativa.")
            st.success("**Recomendación Financiera:** Colocar el 60% en pactos diarios o fondos de liquidez inmediata para rentabilizar el saldo sin perder operatividad.")

# ==========================================
# MÓDULO 2: INTERÉS SIMPLE Y COMPUESTO
# ==========================================
elif modulo == "2. Interés Simple y Compuesto":
    st.header("Unidad 2: Interés Simple e Interés Compuesto")
    
    st.subheader("⚙️ Calculadora Interactiva de Interés")
    
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        vp_input = st.number_input("Capital Inicial (VP):", value=1000000.0, step=50000.0)
    with c2:
        tasa_input = st.number_input("Tasa Periódica (%):", value=1.5, step=0.1) / 100.0
    with c3:
        n_input = st.number_input("Plazo (Periodos):", value=12, min_value=1, max_value=120)
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
    mc1.metric("Valor Futuro (Simple)", f"${vf_simple:,.2f}")
    mc2.metric("Valor Futuro (Compuesto)", f"${vf_compuesto:,.2f}")
    mc3.metric("Diferencia por Capitalización", f"${(vf_compuesto - vf_simple):,.2f}")
    
    st.line_chart(res_df.set_index("Periodo"))
    
    st.markdown("---")
    st.subheader("📝 Caso Destacado: Matrimonio y Fondo de $25.000.000")
    st.markdown("""
    **Problema:** Un matrimonio dispone de $25.000.000 para invertir durante 5 años (60 meses).
    - Opción A: Interés Simple al 0.8% mensual.
    - Opción B: Interés Compuesto al 0.75% mensual.
    """)
    vf_mat_a = 25000000 * (1 + 0.008 * 60)
    vf_mat_b = 25000000 * ((1 + 0.0075) ** 60)
    
    st.write(f"- **Opción A (Simple 0.8%):** VF = $25M × (1 + 0.008 × 60) = **${vf_mat_a:,.2f}**")
    st.write(f"- **Opción B (Compuesto 0.75%):** VF = $25M × (1 + 0.0075)^60 = **${vf_mat_b:,.2f}**")
    if vf_mat_b > vf_mat_a:
        st.success(f"✅ Conviene la **Opción B (Interés Compuesto)** por una diferencia a favor de **${(vf_mat_b - vf_mat_a):,.2f}** gracias a la reinversión de intereses.")
    else:
        st.success(f"✅ Conviene la **Opción A (Interés Simple)** por una diferencia a favor de **${(vf_mat_a - vf_mat_b):,.2f}**.")

# ==========================================
# MÓDULO 3: CONVERSIÓN DE TASAS
# ==========================================
elif modulo == "3. Conversión de Tasas (TNA/TEA)":
    st.header("Unidad 3: Conversión y Decodificación de Tasas")
    
    col_t1, col_t2 = st.columns(2)
    
    with col_t1:
        st.subheader("🔄 Conversor TNA ➔ TEA")
        tna_val = st.number_input("Tasa Nominal Anual (TNA %):", value=24.0, step=0.5) / 100.0
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
        
        st.write(f"• **Tasa Periódica ($i$):** {i_per*100:.4f}%")
        st.metric("Tasa Efectiva Anual (TEA Equivalent)", f"{tea_calc*100:.4f}%")

    with col_t2:
        st.subheader("⚖️ Comparador Banco X vs. Banco Y")
        st.markdown("""
        - **Banco X:** 9,0% TNA con capitalización trimestral ($m=4$).
        - **Banco Y:** 9,2% TEA directa.
        """)
        tea_x = ((1 + 0.09/4)**4) - 1.0
        tea_y = 0.092
        
        st.write(f"• **TEA Banco X:** $(1 + 0.09/4)^4 - 1 =$ **{tea_x*100:.4f}%**")
        st.write(f"• **TEA Banco Y:** **{tea_y*100:.4f}%**")
        
        if tea_x > tea_y:
            st.success(f"✅ **Para Invertir/Ahorrar:** Conviene **Banco X** ({tea_x*100:.2f}% TEA).\n\n✅ **Para Solicitar Crédito:** Conviene **Banco Y** (9.20% TEA).")

# ==========================================
# MÓDULO 4: ANUALIDADES
# ==========================================
elif modulo == "4. Anualidades y Amortización":
    st.header("Unidad 4: Anualidades y Tablas de Amortización")
    
    st.subheader("💳 Simulador de Préstamos y Amortización (Método Francés)")
    
    ac1, ac2, ac3 = st.columns(3)
    with ac1:
        monto_prestamo = st.number_input("Monto del Préstamo ($):", value=30000.0, step=1000.0)
    with ac2:
        tasa_mensual_anu = st.number_input("Tasa Efectiva Mensual (%):", value=1.2, step=0.1) / 100.0
    with ac3:
        plazo_meses = st.slider("Plazo en Meses (n):", min_value=6, max_value=60, value=36)
        
    # Cuota fija (PMT)
    cuota_fija = monto_prestamo * (tasa_mensual_anu / (1 - (1 + tasa_mensual_anu)**(-plazo_meses)))
    
    st.metric("Cuota Mensual Calculada (R)", f"${cuota_fija:,.2f}")
    
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
    st.dataframe(df_amort.style.format({
        "Saldo Inicial": "${:,.2f}",
        "Cuota ($)": "${:,.2f}",
        "Interés ($)": "${:,.2f}",
        "Amortización ($)": "${:,.2f}",
        "Saldo Final": "${:,.2f}"
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
        base_a = st.number_input("Flujo Base Inicial (A):", value=1000.0, step=100.0)
    with gc2:
        grad_g = st.number_input("Gradiente Aritmético (G $):", value=200.0, step=50.0)
    with gc3:
        grad_pct = st.number_input("Gradiente Geométrico (g %):", value=10.0, step=1.0) / 100.0
        
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
    st.markdown(r"""
    - **Inversión Inicial:** $5.000.000 al término del año 4.
    - **Flujo Año 5:** $800.000 con crecimiento perpetuo al $g = 5\%$ anual.
    - **Tasa de Descuento (TMAR):** 12% anual.
    """)
    vp_perpetuidad_4 = 800000 / (0.12 - 0.05)
    vp_hoy_0 = vp_perpetuidad_4 / ((1 + 0.12)**4)
    st.write(f"• **Valor Presente en Año 4 ($VP_4$):** $800.000 / (0.12 - 0.05) = **${vp_perpetuidad_4:,.2f}**")
    st.write(f"• **Valor Presente Hoy ($VP_0$):** ${vp_perpetuidad_4:,.2f} / (1.12)^4 = **${vp_hoy_0:,.2f}**")

# ==========================================
# MÓDULO 6: PRESUPUESTOS
# ==========================================
elif modulo == "6. Presupuesto y Flujo de Caja":
    st.header("Unidad 6: Presupuestos y Control de Caja Operacional")
    
    st.subheader("📊 Simulador de Presupuesto Mensual a 12 Meses con Inflación")
    
    pc1, pc2, pc3 = st.columns(3)
    with pc1:
        v_base = st.number_input("Ventas Mes 1 ($):", value=15000.0, step=1000.0)
    with pc2:
        g_ventas = st.number_input("Crecimiento Ventas Mensual (%):", value=1.5, step=0.1) / 100.0
    with pc3:
        inf_mensual = st.number_input("Inflación Costos Mensual (%):", value=0.5, step=0.1) / 100.0
        
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
    st.dataframe(df_pres.style.format({
        "Ventas ($)": "${:,.2f}",
        "Total Egresos ($)": "${:,.2f}",
        "Flujo Neto ($)": "${:,.2f}",
        "Caja Acumulada ($)": "${:,.2f}"
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
    with eq2:
        p_val = st.number_input("Precio Unitario ($):", value=50.0, step=1.0)
    with eq3:
        cv_val = st.number_input("Costo Variable Unitario ($):", value=30.0, step=1.0)
        
    mc_unit = p_val - cv_val
    if mc_unit > 0:
        q_eq = cf_val / mc_unit
        ing_eq = q_eq * p_val
        st.success(f"• **Punto de Equilibrio en Unidades:** **{q_eq:,.0f} unidades**")
        st.success(f"• **Ingreso de Equilibrio:** **${ing_eq:,.2f}**")
    else:
        st.error("El precio unitario debe ser mayor al costo variable.")
        
    st.markdown("---")
    st.subheader("💰 Evaluación de Flujos de Caja (VAN y TIR)")
    
    inv_ini = st.number_input("Inversión Inicial ($):", value=500000.0, step=10000.0)
    tmar_val = st.number_input("Tasa de Descuento / TMAR (%):", value=10.0, step=0.5) / 100.0
    
    st.write("Ingresa los flujos proyectados a 5 años:")
    fc_cols = st.columns(5)
    flujos = []
    for idx, col in enumerate(fc_cols):
        with col:
            f_val = st.number_input(f"Año {idx+1} ($):", value=140000.0 + idx*10000.0, step=5000.0)
            flujos.append(f_val)
            
    van_val = npf.npv(tmar_val, [0] + flujos) - inv_ini
    tir_val = npf.irr([-inv_ini] + flujos)
    
    col_v1, col_v2 = st.columns(2)
    col_v1.metric("Valor Actual Neto (VAN)", f"${van_val:,.2f}", delta="Viable" if van_val > 0 else "No Viable")
    col_v2.metric("Tasa Interna de Retorno (TIR)", f"{tir_val*100:.2f}%", delta="TIR > TMAR" if tir_val > tmar_val else "TIR < TMAR")

# ==========================================
# MÓDULO 8: SOLEMNES Y EXÁMENES
# ==========================================
elif modulo == "8. Calculadoras Especializadas":
    st.header("Módulo 8: Calculadoras Especializadas")
    
    preg = st.selectbox("Selecciona la Pregunta a Revisar:", [
        "Pregunta 1: Valor Futuro USD 1.000 a 16 meses al 5% anual",
        "Pregunta 2: Tiempo para alcanzar USD 3.525 desde USD 2.000 al 12%",
        "Pregunta 9: Saldo de Préstamo al inicio del Año 4 (18% anual)",
        "Pregunta 10: Cuota de Préstamo de USD 1.800 a 36 meses (1.25% mens)",
        "Pregunta 11: Conversión de TEA al 24% Nominal Trimestral"
    ])
    
    if "Pregunta 1:" in preg:
        st.markdown(r"""
        **Enunciado:** Calcular el Valor Futuro de USD 1.000 a 16 meses con una tasa del 5% anual compuesto.
        - **Fórmula:** $VF = VP \times (1 + i)^{n/12}$
        - **Desarrollo:** $VF = 1.000 \times (1 + 0.05)^{16/12} = 1.000 \times 1.06725 = \mathbf{USD\ 1.067,25}$
        """)
        st.success("Respuesta Correcta: USD 1.067,25")
    elif "Pregunta 2:" in preg:
        st.markdown(r"""
        **Enunciado:** ¿En cuántos años USD 2.000 se convertirán en USD 3.525 al 12% anual compuesto?
        - **Fórmula:** $n = \frac{\ln(VF / VP)}{\ln(1 + i)}$
        - **Desarrollo:** $n = \frac{\ln(3525 / 2000)}{\ln(1.12)} = \frac{0.5660}{0.1133} = \mathbf{5,00\ \text{años}}$
        """)
        st.success("Respuesta Correcta: 5,00 años")
    elif "Pregunta 9:" in preg:
        st.markdown(r"""
        **Enunciado:** Préstamo de $1.000.000 a 5 años al 18% anual. ¿Cuál es el saldo de capital al inicio del año 4 (después del 3er pago)?
        - **Cuota Anual (R):** $PMT(18\%, 5, -1M) = \mathbf{\$319.777,84}$
        - **Saldo al Año 3:** $VP \text{ de las 2 cuotas restantes} = 319.777,84 \times \frac{1 - (1.18)^{-2}}{0.18} = \mathbf{\$480.334,10}$
        """)
        st.success("Respuesta Correcta: $480.334,10")
    elif "Pregunta 10:" in preg:
        st.markdown(r"""
        **Enunciado:** Préstamo de USD 1.800 a pagar en 36 cuotas mensuales al 1.25% mensual.
        - **Fórmula:** $R = VP \times \frac{i}{1 - (1+i)^{-36}}$
        - **Desarrollo:** $R = 1.800 \times \frac{0.0125}{1 - (1.0125)^{-36}} = \mathbf{USD\ 62,25}$
        """)
        st.success("Respuesta Correcta: USD 62,25 mensual")
    else:
        st.markdown(r"""
        **Enunciado:** Hallar la Tasa Efectiva Anual (TEA) de una tasa nominal del 24% capitalizable trimestralmente ($m=4$).
        - **Fórmula:** $TEA = (1 + 0.24/4)^4 - 1 = (1.06)^4 - 1$
        - **Desarrollo:** $1.262477 - 1 = \mathbf{26,25\%}$
        """)
        st.success("Respuesta Correcta: 26,25% TEA")

st.markdown("---")
st.caption("04 Finanzas App Web — Generado automáticamente para Gemini Notebook")
