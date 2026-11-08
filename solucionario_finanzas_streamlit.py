import streamlit as st
import numpy as np
import pandas as pd
import numpy_financial as npf
import math
import io

# Configuración de página
st.set_page_config(
    page_title="04 Finanzas — Plataforma Web de Ingeniería Financiera",
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
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            key=f"dl_btn_{filename_prefix}"
        )
    except Exception as e:
        csv_data = df.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="📥 Exportar Tabla a CSV (Compatible con Excel)",
            data=csv_data,
            file_name=f"{filename_prefix}.csv",
            mime="text/csv",
            key=f"dl_csv_{filename_prefix}"
        )

# Encabezado Principal
st.markdown('<div class="main-header">04 FINANZAS — Plataforma de Simulación & Ingeniería Financiera</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Herramienta interactiva de cálculo y simulación desarrollada para la comunidad estudiantil.</div>', unsafe_allow_html=True)

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
        "8. Calculadoras Especializadas y Simuladores"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info("💡 **Tip:** Puedes modificar todos los parámetros de las calculadoras en tiempo real para simular cualquier escenario financiero.")

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
            "Caso 1: Evaluación de Ahorro a Plazo Fijo",
            "Caso 2: Compra al Contado vs. Crédito",
            "Caso 3: Gestión de Fondo de Emergencia (15%)",
            "Caso 4: Optimización de Excedentes de Caja Pyme"
        ])
        
        if "Caso 1" in caso:
            st.info("**Situación:** Evaluación de un excedente personal de $500.000 entre consumo inmediato o depósito a plazo fijo al 0.6% mensual.")
            st.success("**Recomendación Financiera:** Depositar a plazo o invertir en un fondo mutuo conservador. En 12 meses se obtendrían $537.026. Prioriza la acumulación de capital y el VDT.")
        elif "Caso 2" in caso:
            st.info("**Situación:** Elección entre comprar equipamiento al contado ($600.000) o en 12 cuotas de $62.000 (Total $744.000).")
            st.warning("**Recomendación Financiera:** Comprar al contado si se dispone de liquidez. La alternativa a crédito implica un costo financiero total (CAE) implícito superior al 40% anual.")
        elif "Caso 3" in caso:
            st.info("**Situación:** Presupuesto familiar de $1.200.000 afectado por un imprevisto equivalente al 15% de sus ingresos ($180.000).")
            st.error("**Recomendación Financiera:** Recurrir al fondo de reserva. Si no existe, reestructurar gastos prescindibles del mes y evitar créditos rotativos de alto costo.")
        else:
            st.info("**Situación:** Empresa con $5.000.000 ociosos en la cuenta corriente operativa.")
            st.success("**Recomendación Financiera:** Colocar el 60% en pactos diarios o fondos de liquidez inmediata para rentabilizar el saldo sin perder operatividad.")

# ==========================================
# MÓDULO 2: INTERÉS SIMPLE Y COMPUESTO
# ==========================================
elif modulo == "2. Interés Simple y Compuesto":
    st.header("Unidad 2: Interés Simple e Interés Compuesto")
    
    st.subheader("⚙️ Calculadora Interactiva de Régimen de Interés")
    
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        vp_input = st.number_input("Capital Inicial (VP $):", value=1000000.0, step=50000.0)
    with c2:
        tasa_input = st.number_input("Tasa Periódica (%):", value=1.5, step=0.1) / 100.0
    with c3:
        n_input = st.number_input("Plazo (Períodos):", value=12, min_value=1, max_value=120)
    with c4:
        regimen = st.selectbox("Régimen de Capitalización:", ["Interés Compuesto", "Interés Simple", "Comparar Ambos"])
        
    vf_simple = vp_input * (1 + tasa_input * n_input)
    vf_compuesto = vp_input * ((1 + tasa_input) ** n_input)
    
    res_df = pd.DataFrame({
        "Período": list(range(0, n_input + 1)),
        "Interés Simple ($)": [vp_input * (1 + tasa_input * t) for t in range(0, n_input + 1)],
        "Interés Compuesto ($)": [vp_input * ((1 + tasa_input) ** t) for t in range(0, n_input + 1)]
    })
    
    st.markdown("#### Resultados Proyectados")
    mc1, mc2, mc3 = st.columns(3)
    mc1.metric("Valor Futuro (Simple)", f"${vf_simple:,.2f}")
    mc2.metric("Valor Futuro (Compuesto)", f"${vf_compuesto:,.2f}")
    mc3.metric("Diferencia por Capitalización", f"${(vf_compuesto - vf_simple):,.2f}")
    
    st.line_chart(res_df.set_index("Período"))
    
    st.markdown("---")
    st.subheader("📝 Caso Práctico de Comparación de Regímenes")
    st.markdown("""
    **Escenario:** Inversión de un capital de $25.000.000 a un plazo de 5 años (60 meses).
    - Opción A: Interés Simple al 0,8% mensual.
    - Opción B: Interés Compuesto al 0,75% mensual.
    """)
    vf_mat_a = 25000000 * (1 + 0.008 * 60)
    vf_mat_b = 25000000 * ((1 + 0.0075) ** 60)
    
    st.write(f"• **Opción A (Simple 0,8%):** VF = $25M × (1 + 0.008 × 60) = **${vf_mat_a:,.2f}**")
    st.write(f"• **Opción B (Compuesto 0,75%):** VF = $25M × (1 + 0.0075)^60 = **${vf_mat_b:,.2f}**")
    if vf_mat_b > vf_mat_a:
        st.success(f"✅ Conviene la **Opción B (Interés Compuesto)** con una diferencia favorable de **${(vf_mat_b - vf_mat_a):,.2f}** gracias al efecto exponencial del interés compuesto.")
    else:
        st.success(f"✅ Conviene la **Opción A (Interés Simple)** por una diferencia a favor de **${(vf_mat_a - vf_mat_b):,.2f}**.")

# ==========================================
# MÓDULO 3: CONVERSIÓN DE TASAS
# ==========================================
elif modulo == "3. Conversión de Tasas (TNA/TEA)":
    st.header("Unidad 3: Conversión y Decodificación de Tasas de Interés")
    
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
        st.metric("Tasa Efectiva Anual (TEA Equivalente)", f"{tea_calc*100:.4f}%")

    with col_t2:
        st.subheader("⚖️ Comparador de Tasas Nominales vs. Efectivas")
        st.markdown("""
        - **Opción A:** 9,0% TNA con capitalización trimestral ($m=4$).
        - **Opción B:** 9,2% TEA directa.
        """)
        tea_x = ((1 + 0.09/4)**4) - 1.0
        tea_y = 0.092
        
        st.write(f"• **TEA Opción A:** $(1 + 0,09/4)^4 - 1 =$ **{tea_x*100:.4f}%**")
        st.write(f"• **TEA Opción B:** **{tea_y*100:.4f}%**")
        
        if tea_x > tea_y:
            st.success(f"✅ **Para Inversión/Ahorro:** Conviene **Opción A** ({tea_x*100:.2f}% TEA).\n\n✅ **Para Crédito:** Conviene **Opción B** (9,20% TEA).")

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
    }), height=300, hide_index=True)
    
    st.markdown("#### Descomposición Cuota: Interés vs. Amortización")
    st.bar_chart(df_amort.set_index("Mes")[["Interés ($)", "Amortización ($)"]])

# ==========================================
# MÓDULO 5: GRADIENTES
# ==========================================
elif modulo == "5. Gradientes Financieros":
    st.header("Unidad 5: Gradientes Financieros (Series Variables)")
    
    st.subheader("📈 Comparativa de Series: Constante vs. Aritmética vs. Geométrica")
    
    gc1, gc2, gc3 = st.columns(3)
    with gc1:
        base_a = st.number_input("Flujo Base Inicial (A $):", value=1000.0, step=100.0)
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
    st.subheader("🏗️ Modelo de Valuación de Perpetuidades con Crecimiento")
    st.markdown(r"""
    - **Inversión Inicial:** $5.000.000 al término del año 4.
    - **Flujo Año 5:** $800.000 con crecimiento perpetuo al $g = 5\%$ anual.
    - **Tasa de Descuento (TMAR):** 12% anual.
    """)
    vp_perpetuidad_4 = 800000 / (0.12 - 0.05)
    vp_hoy_0 = vp_perpetuidad_4 / ((1 + 0.12)**4)
    st.write(f"• **Valor Presente en Año 4 ($VP_4$):** $800.000 / (0,12 - 0,05) = **${vp_perpetuidad_4:,.2f}**")
    st.write(f"• **Valor Presente Hoy ($VP_0$):** ${vp_perpetuidad_4:,.2f} / (1,12)^4 = **${vp_hoy_0:,.2f}**")

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
    }), hide_index=True)
    
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
# MÓDULO 8: CALCULADORAS ESPECIALIZADAS Y SIMULADORES
# ==========================================
elif modulo == "8. Calculadoras Especializadas y Simuladores":
    st.header("🛠️ Unidad 8: Suite de Calculadoras Especializadas de Ingeniería Financiera")
    st.caption("Herramientas interactivas de cómputo para simular amortizaciones, tasas variables, anualidades, evaluación de ofertas y costo financiero total.")
    
    herramienta_sel = st.selectbox(
        "Selecciona la Herramienta de Cálculo:",
        [
            "I. Desglose de Interés y Amortización para una Cuota Específica (k)",
            "II. Valor Futuro con Interés Compuesto (Plazos Enteros y Fraccionados)",
            "III. Valor Futuro de Anualidades y Fondos de Ahorro",
            "IV. Valuación de Flujos Múltiples e Irregulares (VP y VF)",
            "V. Despeje de Plazo Requerido (n) y Tasa Implícita",
            "VI. Conversión Avanzada de Tasas Nominales/Efectivas y Spread",
            "VII. Valor Presente (VP) de Pagos Futuros Específicos Discretos en Meses",
            "VIII. Valor Futuro (VF) de Depósitos Proyectados Discretos en Meses Específicos (Tasas Variables)",
            "IX. Comparador de Ofertas Bancarias a Plazo Fijo / Depósitos",
            "X. Crédito Comercial / Bienes de Capital",
            "XI. Tasa Implícita Anual para Créditos o Inversiones de Pago Único",
            "XII. Valor Presente de Cero / Descuento (4 Decimales de Precisión)",
            "XIII. Calculadora Universal de Cuotas e Intereses de Préstamos (Precisión a 4 Decimales)",
            "XIV. Calculadora de Costo Financiero Total (CFT) y Comisiones"
        ]
    )
    
    st.markdown("---")
    
    # -------------------------------------------------------------
    # HERRAMIENTA I
    # -------------------------------------------------------------
    if "I. Desglose de Interés" in herramienta_sel:
        st.subheader("🛠️ I. Desglose de Interés y Amortización para Cuota Específica (k)")
        st.caption("Ingresa los datos del crédito para consultar la cuota fija (R), la tasa homogénea y el desglose en el período k.")
        
        col_c1, col_c2, col_c3 = st.columns(3)
        with col_c1:
            monto_h1 = smart_num_input("Monto del Préstamo ($):", 15000000.0, key="calc1_monto")
            st.markdown(f'<div class="val-badge">💵 Préstamo: ${fmt_m(monto_h1)}</div>', unsafe_allow_html=True)
        with col_c2:
            n_cuotas_h1 = int(smart_num_input("Número de Cuotas Totales (n):", 24.0, key="calc1_n"))
            st.markdown(f'<div class="val-badge">📅 Plazo: {n_cuotas_h1} cuotas</div>', unsafe_allow_html=True)
        with col_c3:
            k_cons = int(smart_num_input("Número de Cuota a Consultar (k):", 5.0, key="calc1_k"))
            st.markdown(f'<div class="val-badge">🔍 Cuota a consultar: #{k_cons}</div>', unsafe_allow_html=True)

        col_t1, col_t2 = st.columns(2)
        with col_t1:
            tasa_val_h1 = smart_num_input("Tasa Ingresada (%):", 2.50, key="calc1_tasa") / 100.0
            st.markdown(f'<div class="val-badge">📈 Tasa: {fmt_n(tasa_val_h1*100, 2)}%</div>', unsafe_allow_html=True)
        with col_t2:
            tipo_tasa_h1 = st.selectbox("Tipo / Frecuencia de la Tasa:", [
                "Efectiva Mensual (TEM)",
                "Efectiva Trimestral (TET)",
                "Efectiva Cuatrimestral (TEC)",
                "Efectiva Semestral (TES)",
                "Efectiva Anual (TEA)",
                "Nominal Anual (TNA capitalizable mensualmente)"
            ], key="calc1_tipotasa")

        # Conversión a tasa periódica cuota
        if "Mensual" in tipo_tasa_h1:
            i_cuota = tasa_val_h1
        elif "Trimestral" in tipo_tasa_h1:
            i_cuota = ((1 + tasa_val_h1) ** (1/3.0)) - 1.0
        elif "Cuatrimestral" in tipo_tasa_h1:
            i_cuota = ((1 + tasa_val_h1) ** (1/4.0)) - 1.0
        elif "Semestral" in tipo_tasa_h1:
            i_cuota = ((1 + tasa_val_h1) ** (1/6.0)) - 1.0
        elif "Anual (TEA)" in tipo_tasa_h1:
            i_cuota = ((1 + tasa_val_h1) ** (1/12.0)) - 1.0
        else:
            i_cuota = tasa_val_h1 / 12.0

        if n_cuotas_h1 > 0 and i_cuota > 0 and k_cons <= n_cuotas_h1:
            # Cuota fija (PMT)
            r_cuota = monto_h1 * (i_cuota / (1 - (1 + i_cuota)**(-n_cuotas_h1)))
            
            # Amortización periódica
            saldo_act = monto_h1
            ik_val = 0.0
            ak_val = 0.0
            saldo_k = 0.0
            
            tabla_amort = []
            for t_i in range(1, n_cuotas_h1 + 1):
                int_i = saldo_act * i_cuota
                cap_i = r_cuota - int_i
                saldo_fin_i = max(0.0, saldo_act - cap_i)
                
                if t_i == k_cons:
                    ik_val = int_i
                    ak_val = cap_i
                    saldo_k = saldo_fin_i
                    
                tabla_amort.append({
                    "Cuota": t_i,
                    "Saldo Inicial ($)": fmt_m(saldo_act),
                    "Cuota Fija ($)": fmt_m(r_cuota),
                    "Interés ($)": fmt_m(int_i),
                    "Amortización ($)": fmt_m(cap_i),
                    "Saldo Insoluto ($)": fmt_m(saldo_fin_i)
                })
                saldo_act = saldo_fin_i

            st.markdown("### 📊 Resultados de la Cuota Consultada")
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Cuota Mensual (R)", f"${fmt_m(r_cuota)}")
            m2.metric(f"Interés Cuota #{k_cons} (I_k)", f"${fmt_m(ik_val)}")
            m3.metric(f"Amortización Cuota #{k_cons} (A_k)", f"${fmt_m(ak_val)}")
            m4.metric(f"Saldo Insoluto tras #{k_cons}", f"${fmt_m(saldo_k)}")

            st.markdown("#### Tabla Completa de Amortización (Método Francés)")
            df_amort_h1 = pd.DataFrame(tabla_amort)
            st.dataframe(df_amort_h1, hide_index=True, height=300)
            export_dataframe_button(df_amort_h1, f"tabla_amortizacion_cuota_{k_cons}")

    # -------------------------------------------------------------
    # HERRAMIENTA II
    # -------------------------------------------------------------
    elif "II. Valor Futuro con Interés Compuesto" in herramienta_sel:
        st.subheader("🛠️ II. Valor Futuro con Interés Compuesto (Plazos Enteros y Fraccionados)")
        
        c21, c22, c23 = st.columns(3)
        with c21:
            vp_h2 = smart_num_input("Capital Inicial (VP $):", 1000000.0, key="calc2_vp")
            st.markdown(f'<div class="val-badge">💵 VP: ${fmt_m(vp_h2)}</div>', unsafe_allow_html=True)
        with c22:
            tasa_h2 = smart_num_input("Tasa Anual Efectiva (%):", 5.0, key="calc2_tasa") / 100.0
            st.markdown(f'<div class="val-badge">📈 TEA: {fmt_n(tasa_h2*100, 2)}%</div>', unsafe_allow_html=True)
        with c23:
            meses_h2 = smart_num_input("Plazo Total en Meses:", 16.0, key="calc2_meses")
            st.markdown(f'<div class="val-badge">⏳ Plazo: {meses_h2} meses</div>', unsafe_allow_html=True)

        n_anos_h2 = meses_h2 / 12.0
        vf_h2 = vp_h2 * ((1 + tasa_h2) ** n_anos_h2)
        int_h2 = vf_h2 - vp_h2

        res1, res2 = st.columns(2)
        res1.metric("Valor Futuro (VF)", f"${fmt_m(vf_h2)}")
        res2.metric("Intereses Ganados", f"${fmt_m(int_h2)}")

    # -------------------------------------------------------------
    # HERRAMIENTA III
    # -------------------------------------------------------------
    elif "III. Valor Futuro de Anualidades" in herramienta_sel:
        st.subheader("🛠️ III. Valor Futuro de Anualidades y Fondos de Ahorro")
        
        ca1, ca2, ca3, ca4 = st.columns(4)
        with ca1:
            r_h3 = smart_num_input("Aporte Periódico (R $):", 500000.0, key="calc3_r")
            st.markdown(f'<div class="val-badge">💵 Aporte: ${fmt_m(r_h3)}</div>', unsafe_allow_html=True)
        with ca2:
            tasa_h3 = smart_num_input("Tasa Periódica (%):", 4.0, key="calc3_tasa") / 100.0
            st.markdown(f'<div class="val-badge">📈 Tasa: {fmt_n(tasa_h3*100, 2)}%</div>', unsafe_allow_html=True)
        with ca3:
            n_per_h3 = int(smart_num_input("Número de Períodos (n):", 8.0, key="calc3_n"))
            st.markdown(f'<div class="val-badge">📅 Períodos: {n_per_h3}</div>', unsafe_allow_html=True)
        with ca4:
            tipo_anu_h3 = st.selectbox("Tipo de Anualidad:", ["Vencida / Ordinaria", "Anticipada"], key="calc3_tipo")

        if tipo_anu_h3 == "Vencida / Ordinaria":
            vf_h3 = r_h3 * (((1 + tasa_h3)**n_per_h3 - 1) / tasa_h3)
        else:
            vf_h3 = r_h3 * (((1 + tasa_h3)**n_per_h3 - 1) / tasa_h3) * (1 + tasa_h3)

        total_aportes_h3 = r_h3 * n_per_h3
        int_ganados_h3 = vf_h3 - total_aportes_h3

        ar1, ar2, ar3 = st.columns(3)
        ar1.metric("Valor Futuro Acumulado (VF)", f"${fmt_m(vf_h3)}")
        ar2.metric("Total Capital Aportado", f"${fmt_m(total_aportes_h3)}")
        ar3.metric("Intereses Ganados", f"${fmt_m(int_ganados_h3)}")

    # -------------------------------------------------------------
    # HERRAMIENTA IV
    # -------------------------------------------------------------
    elif "IV. Valuación de Flujos Múltiples" in herramienta_sel:
        st.subheader("🛠️ IV. Valuación de Flujos Múltiples e Irregulares (VP y VF)")
        st.caption("Calcula el Valor Presente Neto (VP en t=0) y Valor Futuro (VF en t=N) de flujos proyectados.")
        
        f1, f2 = st.columns(2)
        with f1:
            tasa_h4 = smart_num_input("Tasa de Descuento Periódica (%):", 2.50, key="calc4_tasa") / 100.0
            st.markdown(f'<div class="val-badge">📈 Tasa: {fmt_n(tasa_h4*100, 2)}%</div>', unsafe_allow_html=True)
        with f2:
            num_flujos_h4 = int(st.slider("Número de Períodos de Flujos (N):", min_value=2, max_value=12, value=4, key="calc4_numf"))

        st.markdown("##### Ingreso de Flujos de Caja por Período:")
        flujos_inputs = []
        cols_fl = st.columns(min(num_flujos_h4, 6))
        for idx in range(num_flujos_h4):
            col_idx = cols_fl[idx % len(cols_fl)]
            with col_idx:
                def_val = 5000000.0 if idx == 0 else (7000000.0 if idx == 2 else (12000000.0 if idx == 3 else 0.0))
                val_fl = smart_num_input(f"Flujo Mes {idx+1} ($):", def_val, key=f"calc4_flujo_{idx}")
                flujos_inputs.append(val_fl)

        vp_total_h4 = sum(fl / ((1 + tasa_h4)**(i + 1)) for i, fl in enumerate(flujos_inputs))
        vf_total_h4 = vp_total_h4 * ((1 + tasa_h4)**num_flujos_h4)

        vr1, vr2 = st.columns(2)
        vr1.metric("Valor Presente Total (VP t=0)", f"${fmt_m(vp_total_h4)}")
        vr2.metric(f"Valor Futuro Total (VF t={num_flujos_h4})", f"${fmt_m(vf_total_h4)}")

    # -------------------------------------------------------------
    # HERRAMIENTA V
    # -------------------------------------------------------------
    elif "V. Despeje de Plazo Requerido" in herramienta_sel:
        st.subheader("🛠️ V. Despeje de Plazo Requerido (n) y Tasa Implícita")
        
        mode_v = st.radio("Modo de Cálculo:", ["Despejar Plazo Requerido (n)", "Despejar Tasa Implícita (i)"], key="calc5_mode")
        
        if "Plazo" in mode_v:
            cp1, cp2, cp3 = st.columns(3)
            with cp1:
                vp_h5 = smart_num_input("Capital Inicial (VP $):", 2000.0, key="calc5_vp")
                st.markdown(f'<div class="val-badge">💵 VP: ${fmt_m(vp_h5)}</div>', unsafe_allow_html=True)
            with cp2:
                vf_h5 = smart_num_input("Meta de Capital (VF $):", 3525.0, key="calc5_vf")
                st.markdown(f'<div class="val-badge">🎯 VF: ${fmt_m(vf_h5)}</div>', unsafe_allow_html=True)
            with cp3:
                tasa_h5 = smart_num_input("Tasa Anual Efectiva (%):", 12.0, key="calc5_tasa") / 100.0
                st.markdown(f'<div class="val-badge">📈 Tasa: {fmt_n(tasa_h5*100, 2)}%</div>', unsafe_allow_html=True)

            if vf_h5 > vp_h5 and tasa_h5 > 0:
                n_despejado = math.log(vf_h5 / vp_h5) / math.log(1 + tasa_h5)
                st.markdown(f"### ⏱️ Plazo Requerido: **{fmt_n(n_despejado, 2)} años** ({fmt_n(n_despejado*12, 1)} meses)")
        else:
            ct1, ct2, ct3 = st.columns(3)
            with ct1:
                vp_h5b = smart_num_input("Capital Inicial (VP $):", 2000.0, key="calc5b_vp")
                st.markdown(f'<div class="val-badge">💵 VP: ${fmt_m(vp_h5b)}</div>', unsafe_allow_html=True)
            with ct2:
                vf_h5b = smart_num_input("Valor Futuro (VF $):", 3525.0, key="calc5b_vf")
                st.markdown(f'<div class="val-badge">🎯 VF: ${fmt_m(vf_h5b)}</div>', unsafe_allow_html=True)
            with ct3:
                n_h5b = smart_num_input("Plazo en Años:", 5.0, key="calc5b_n")
                st.markdown(f'<div class="val-badge">⏳ Plazo: {n_h5b} años</div>', unsafe_allow_html=True)

            if vf_h5b > vp_h5b and n_h5b > 0:
                i_despejada = ((vf_h5b / vp_h5b) ** (1.0 / n_h5b)) - 1.0
                st.markdown(f"### 📈 Tasa Implícita Efectiva Anual: **{fmt_n(i_despejada*100, 4)}%**")

    # -------------------------------------------------------------
    # HERRAMIENTA VI
    # -------------------------------------------------------------
    elif "VI. Conversión Avanzada" in herramienta_sel:
        st.subheader("🛠️ VI. Conversión Avanzada de Tasas Nominales/Efectivas y Spread")
        
        sc1, sc2, sc3 = st.columns(3)
        with sc1:
            tna_h6 = smart_num_input("Tasa Nominal Anual (TNA %):", 24.0, key="calc6_tna") / 100.0
            st.markdown(f'<div class="val-badge">📈 TNA: {fmt_n(tna_h6*100, 2)}%</div>', unsafe_allow_html=True)
        with sc2:
            m_h6 = st.selectbox("Frecuencia de Capitalización (m):", [
                "Mensual (m=12)", "Trimestral (m=4)", "Semestral (m=2)", "Diaria (m=360)"
            ], key="calc6_m")
        with sc3:
            spread_h6 = smart_num_input("Spread Adicional (Puntos Básicos - bps):", 150.0, key="calc6_spread") / 10000.0
            st.markdown(f'<div class="val-badge">➕ Spread: {fmt_n(spread_h6*10000, 0)} bps</div>', unsafe_allow_html=True)

        m_num = 12 if "Mensual" in m_h6 else (4 if "Trimestral" in m_h6 else (2 if "Semestral" in m_h6 else 360))
        i_per_h6 = tna_h6 / m_num
        tea_base = ((1 + i_per_h6)**m_num) - 1.0
        tea_con_spread = tea_base + spread_h6

        tr1, tr2, tr3 = st.columns(3)
        tr1.metric("Tasa Periódica Implícita", f"{fmt_n(i_per_h6*100, 4)}%")
        tr2.metric("TEA Base Equivalente", f"{fmt_n(tea_base*100, 4)}%")
        tr3.metric("TEA Total con Spread", f"{fmt_n(tea_con_spread*100, 4)}%")

    # -------------------------------------------------------------
    # HERRAMIENTA VII
    # -------------------------------------------------------------
    elif "VII. Valor Presente (VP) de Pagos Futuros" in herramienta_sel:
        st.subheader("🛠️ VII. Valor Presente (VP) de Pagos Futuros Específicos Discretos en Meses")
        st.caption("Calcula el Valor Presente total descontado al mes t=0 de pagos específicos que ocurren en meses distintos.")
        
        vc1, vc2 = st.columns(2)
        with vc1:
            tasa_mensual_h7 = smart_num_input("Tasa Efectiva Mensual (%):", 2.50, key="calc7_tasa") / 100.0
            st.markdown(f'<div class="val-badge">📈 Tasa Mensual: {fmt_n(tasa_mensual_h7*100, 2)}%</div>', unsafe_allow_html=True)
        with vc2:
            num_pagos_h7 = int(st.slider("Cantidad de Pagos Proyectados:", min_value=1, max_value=8, value=3, key="calc7_nump"))

        pagos_lista = []
        vp_total_h7 = 0.0
        
        cols_p = st.columns(min(num_pagos_h7, 4))
        for idx_p in range(num_pagos_h7):
            col_p = cols_p[idx_p % len(cols_p)]
            with col_p:
                def_m = 1 if idx_p == 0 else (3 if idx_p == 1 else 4)
                def_monto = 5000000.0 if idx_p == 0 else (7000000.0 if idx_p == 1 else 12000000.0)
                
                mes_val = int(smart_num_input(f"Mes del Pago #{idx_p+1}:", float(def_m), key=f"calc7_mes_{idx_p}"))
                monto_val = smart_num_input(f"Monto Pago #{idx_p+1} ($):", def_monto, key=f"calc7_monto_{idx_p}")
                
                vp_ind = monto_val / ((1 + tasa_mensual_h7)**mes_val)
                vp_total_h7 += vp_ind
                
                pagos_lista.append({
                    "Pago #": idx_p + 1,
                    "Mes": mes_val,
                    "Monto Futuro ($)": fmt_m(monto_val),
                    "VP Descontado ($)": fmt_m(vp_ind)
                })

        st.markdown(f"### 🎯 Valor Presente Total Descontado (t=0): **${fmt_m(vp_total_h7)}**")
        df_vp_h7 = pd.DataFrame(pagos_lista)
        st.dataframe(df_vp_h7, hide_index=True)

    # -------------------------------------------------------------
    # HERRAMIENTA VIII
    # -------------------------------------------------------------
    elif "VIII. Valor Futuro (VF) de Depósitos Proyectados" in herramienta_sel:
        st.subheader("🛠️ VIII. Valor Futuro (VF) de Depósitos Proyectados Discretos en Meses Específicos (Tasas Variables)")
        st.caption("Simulador dinámico con soporte de múltiples tasas de interés variables por período y desglose de Valor Futuro por abono.")
        
        c81, c82, c83 = st.columns(3)
        with c81:
            horiz_h8 = int(smart_num_input("Horizonte Total de Ahorro (Meses):", 12.0, key="calc8_horiz"))
            st.markdown(f'<div class="val-badge">⏳ Horizonte: {horiz_h8} meses</div>', unsafe_allow_html=True)
        with c82:
            modo_tasa_h8 = st.selectbox("Estructura de Tasas de Interés:", [
                "Tasa Fija Mensual",
                "Cambio de Tasa a partir de un Mes Específico",
                "Tabla / Matriz Personalizada por Mes"
            ], key="calc8_modotasa")
        with c83:
            momento_dep_h8 = st.selectbox("Momento en que se Realiza el Depósito:", [
                "Fin del Mes / Vencido (por defecto)",
                "Inicio del Mes / Anticipado"
            ], key="calc8_momentodep")

        # Construcción del vector de tasas por mes
        tasas_mes = [0.03] * horiz_h8
        if "Cambio de Tasa" in modo_tasa_h8:
            col_ts1, col_ts2, col_ts3 = st.columns(3)
            with col_ts1:
                t_ini_h8 = smart_num_input("Tasa Inicial (% Mensual):", 3.0, key="calc8_tini") / 100.0
            with col_ts2:
                mes_cambio_h8 = int(smart_num_input("Mes a Partir del Cual Cambia la Tasa:", 6.0, key="calc8_mcambio"))
            with col_ts3:
                t_nueva_h8 = smart_num_input("Nueva Tasa (% Mensual):", 4.0, key="calc8_tnueva") / 100.0
                
            for m_i in range(1, horiz_h8 + 1):
                tasas_mes[m_i - 1] = t_nueva_h8 if m_i >= mes_cambio_h8 else t_ini_h8
        elif "Matriz" in modo_tasa_h8:
            st.write("Configuración de Tasas por Mes:")
            cols_tmat = st.columns(min(horiz_h8, 6))
            for idx_m in range(horiz_h8):
                col_m = cols_tmat[idx_m % len(cols_tmat)]
                with col_m:
                    def_t_val = 3.0 if idx_m < 5 else 4.0
                    t_user_m = smart_num_input(f"Tasa Mes {idx_m+1} (%):", def_t_val, key=f"calc8_mat_t_{idx_m}") / 100.0
                    tasas_mes[idx_m] = t_user_m
        else:
            t_fija_h8 = smart_num_input("Tasa Fija (% Mensual):", 3.0, key="calc8_tfija") / 100.0
            tasas_mes = [t_fija_h8] * horiz_h8

        st.markdown("##### Configuración de Depósitos Proyectados por Mes:")
        num_deps_h8 = int(st.slider("Cantidad de Depósitos a Realizar:", min_value=1, max_value=8, value=4, key="calc8_numdep"))
        
        depositos_lista = []
        cols_dep = st.columns(min(num_deps_h8, 4))
        for idx_d in range(num_deps_h8):
            col_d = cols_dep[idx_d % len(cols_dep)]
            with col_d:
                def_m_d = idx_d + 1
                def_monto_d = 30000000.0 if idx_d == 0 else (40000000.0 if idx_d == 1 else 50000000.0)
                
                m_dep_val = int(smart_num_input(f"Mes del Depósito #{idx_d+1}:", float(def_m_d), key=f"calc8_mdep_{idx_d}"))
                monto_dep_val = smart_num_input(f"Monto Depósito #{idx_d+1} ($):", def_monto_d, key=f"calc8_montodep_{idx_d}")
                depositos_lista.append((m_dep_val, monto_dep_val))

        # Vector de depósitos
        deps_dict = {}
        for md, montd in depositos_lista:
            deps_dict[md] = deps_dict.get(md, 0.0) + montd

        # Simulación mes a mes
        saldo_corr = 0.0
        tot_dep_sum = sum(deps_dict.values())
        tot_int_sum = 0.0
        
        es_vencido = "Vencido" in momento_dep_h8
        tabla_evolucion = []

        for m in range(1, horiz_h8 + 1):
            dep_m = deps_dict.get(m, 0.0)
            tasa_m = tasas_mes[m - 1]
            
            if es_vencido:
                saldo_ini = saldo_corr
                int_m = saldo_ini * tasa_m
                saldo_fin = saldo_ini + int_m + dep_m
            else:
                saldo_ini = saldo_corr
                saldo_mas_dep = saldo_ini + dep_m
                int_m = saldo_mas_dep * tasa_m
                saldo_fin = saldo_mas_dep + int_m

            tot_int_sum += int_m
            saldo_corr = saldo_fin

            tabla_evolucion.append({
                "Mes": m,
                "Saldo Inicial ($)": fmt_m(saldo_ini),
                "Depósito ($)": fmt_m(dep_m),
                "Tasa Aplicada (%)": f"{fmt_n(tasa_m*100, 2)}%",
                "Interés del Mes ($)": fmt_m(int_m),
                "Saldo Final ($)": fmt_m(saldo_fin)
            })

        vf_total_h8 = saldo_corr

        # Desglose individual de cada depósito
        desglose_ind = []
        for idx_d, (md, montd) in enumerate(depositos_lista):
            if es_vencido:
                meses_cap = horiz_h8 - md
                start_m = md + 1
            else:
                meses_cap = horiz_h8 - md + 1
                start_m = md

            factor_acum = 1.0
            if start_m <= horiz_h8:
                for k_m in range(start_m, horiz_h8 + 1):
                    factor_acum *= (1.0 + tasas_mes[k_m - 1])

            vf_ind = montd * factor_acum
            pct_part = (vf_ind / vf_total_h8 * 100.0) if vf_total_h8 > 0 else 0.0

            desglose_ind.append({
                "Depósito #": idx_d + 1,
                "Mes del Depósito": md,
                "Monto Depositado ($)": fmt_m(montd),
                "Meses Capitalizados": max(0, meses_cap),
                "Tasa Acumulada (%)": f"{fmt_n((factor_acum - 1.0)*100, 4)}%",
                "Valor Futuro del Depósito ($)": fmt_m(vf_ind),
                "Participación (%)": f"{fmt_n(pct_part, 2)}%"
            })

        st.markdown("### 🎯 Resultados Consolidados")
        r81, r82, r83 = st.columns(3)
        r81.metric("Valor Futuro Total Acumulado (VF)", f"${fmt_m(vf_total_h8)}")
        r82.metric("Total Capital Depositado", f"${fmt_m(tot_dep_sum)}")
        r83.metric("Total Intereses Ganados", f"${fmt_m(tot_int_sum)}")

        st.markdown("#### 1. Desglose del Valor Futuro Individual por Depósito")
        df_ind_h8 = pd.DataFrame(desglose_ind)
        st.dataframe(df_ind_h8, hide_index=True)

        st.markdown("#### 2. Evolución Mensual Detallada del Fondo de Ahorro")
        df_evol_h8 = pd.DataFrame(tabla_evolucion)
        st.dataframe(df_evol_h8, hide_index=True, height=300)
        export_dataframe_button(df_evol_h8, "tabla_evolucion_depositos")

    # -------------------------------------------------------------
    # HERRAMIENTA IX
    # -------------------------------------------------------------
    elif "IX. Comparador de Ofertas Bancarias" in herramienta_sel:
        st.subheader("🛠️ IX. Comparador de Ofertas Bancarias a Plazo Fijo / Depósitos (Múltiples Bancos y Tipos de Tasa)")
        st.caption("Compara el rendimiento real, TEA y Tasa Mensual Equivalente (TEM) de múltiples opciones bancarias.")
        
        bc1, bc2 = st.columns(2)
        with bc1:
            cap_h9 = smart_num_input("Monto a Invertir ($):", 17000000.0, key="calc9_cap")
            st.markdown(f'<div class="val-badge">💵 Capital: ${fmt_m(cap_h9)}</div>', unsafe_allow_html=True)
        with bc2:
            plazo_meses_h9 = smart_num_input("Plazo Total en Meses:", 24.0, key="calc9_plazo")
            st.markdown(f'<div class="val-badge">⏳ Plazo: {plazo_meses_h9} meses</div>', unsafe_allow_html=True)

        cant_bancos_h9 = int(st.slider("Cantidad de Bancos a Comparar:", min_value=2, max_value=5, value=3, key="calc9_cantb"))

        tipos_tasa_opciones = [
            "TEA (Efectiva Anual)", "TEC (Efectiva Cuatrimestral)", "TES (Efectiva Semestral)",
            "TET (Efectiva Trimestral)", "TEB (Efectiva Bimestral)", "TEM (Efectiva Mensual)",
            "TED (Efectiva Diaria)", "TNC (Nominal Cuatrimestral m=4)", "TNC (Nominal Cuatrimestral m=120)",
            "TNS (Nominal Semestral m=6)", "TNT (Nominal Trimestral m=3)", "TNA (Nominal Anual)",
            "Tasa Simple Cuatrimestral", "Tasa Simple Anual", "Tasa Simple Semestral",
            "Tasa Simple Trimestral", "Tasa Simple Mensual"
        ]

        bancos_inputs = []
        for b_idx in range(cant_bancos_h9):
            st.markdown(f"##### 🏛️ Banco / Entidad #{b_idx+1}")
            col_b1, col_b2, col_b3, col_b4 = st.columns(4)
            
            with col_b1:
                b_nom = st.text_input(f"Nombre del Banco #{b_idx+1}:", value="", key=f"calc9_nom_{b_idx}")
                b_nom_final = b_nom.strip() if b_nom.strip() else f"Banco {b_idx+1}"
            with col_b2:
                b_tipo = st.selectbox(f"Tipo de Tasa #{b_idx+1}:", tipos_tasa_opciones, key=f"calc9_tipo_{b_idx}")
            with col_b3:
                def_tasa_val = 12.5 if b_idx == 0 else (4.1 if b_idx == 1 else 1.0)
                b_tasa_val = smart_num_input(f"Tasa Ingresada #{b_idx+1} (%):", def_tasa_val, key=f"calc9_tasa_{b_idx}") / 100.0
            with col_b4:
                b_m_val = 12.0
                if "TNA" in b_tipo:
                    b_m_val = smart_num_input(f"Capitalizaciones m/año #{b_idx+1}:", 12.0, key=f"calc9_m_{b_idx}")

            # Cálculo de TEA equivalente
            if "TEA" in b_tipo:
                tea_b = b_tasa_val
            elif "TEC" in b_tipo:
                tea_b = ((1 + b_tasa_val) ** 3.0) - 1.0
            elif "TES" in b_tipo:
                tea_b = ((1 + b_tasa_val) ** 2.0) - 1.0
            elif "TET" in b_tipo:
                tea_b = ((1 + b_tasa_val) ** 4.0) - 1.0
            elif "TEB" in b_tipo:
                tea_b = ((1 + b_tasa_val) ** 6.0) - 1.0
            elif "TEM" in b_tipo:
                tea_b = ((1 + b_tasa_val) ** 12.0) - 1.0
            elif "TED" in b_tipo:
                tea_b = ((1 + b_tasa_val) ** 360.0) - 1.0
            elif "TNC (Nominal Cuatrimestral m=4)" in b_tipo:
                tea_b = ((1 + b_tasa_val / 4.0) ** 12.0) - 1.0
            elif "TNC (Nominal Cuatrimestral m=120)" in b_tipo:
                tea_b = ((1 + b_tasa_val / 120.0) ** 360.0) - 1.0
            elif "TNS" in b_tipo:
                tea_b = ((1 + b_tasa_val / 6.0) ** 12.0) - 1.0
            elif "TNT" in b_tipo:
                tea_b = ((1 + b_tasa_val / 3.0) ** 12.0) - 1.0
            elif "TNA" in b_tipo:
                tea_b = ((1 + b_tasa_val / b_m_val) ** b_m_val) - 1.0
            elif "Tasa Simple Cuatrimestral" in b_tipo:
                tea_b = b_tasa_val * 3.0
            elif "Tasa Simple Semestral" in b_tipo:
                tea_b = b_tasa_val * 2.0
            elif "Tasa Simple Trimestral" in b_tipo:
                tea_b = b_tasa_val * 4.0
            elif "Tasa Simple Mensual" in b_tipo:
                tea_b = b_tasa_val * 12.0
            else:
                tea_b = b_tasa_val

            tem_b = ((1 + tea_b) ** (1.0 / 12.0)) - 1.0
            anos_p9 = plazo_meses_h9 / 12.0
            vf_b = cap_h9 * ((1 + tea_b) ** anos_p9)
            int_b = vf_b - cap_h9

            bancos_inputs.append({
                "nombre": b_nom_final,
                "tipo": b_tipo,
                "tasa_orig": b_tasa_val,
                "tea": tea_b,
                "tem": tem_b,
                "vf": vf_b,
                "interes": int_b
            })

        # Ordenar por rentabilidad (VF)
        bancos_sorted = sorted(bancos_inputs, key=lambda x: x["vf"], reverse=True)
        mejor_b = bancos_sorted[0]
        segundo_b = bancos_sorted[1] if len(bancos_sorted) > 1 else mejor_b

        st.markdown("### 🏆 Conclusión y Ranking de Rentabilidad")
        dif_pesos_mejor = mejor_b["interes"] - segundo_b["interes"]
        dif_bps_mejor = (mejor_b["tea"] - segundo_b["tea"]) * 10000.0

        st.success(f"✅ **La mejor alternativa es {mejor_b['nombre']}** con un Valor Futuro de **${fmt_m(mejor_b['vf'])}** (Intereses: **${fmt_m(mejor_b['interes'])}**).\n\n"
                   f"• Genera **${fmt_m(dif_pesos_mejor)}** adicionales respecto a la segunda opción ({segundo_b['nombre']}) y supera la tasa en **{fmt_n(dif_bps_mejor, 0)} bps de TEA**.")

        tabla_bancos_res = []
        for rk, b_item in enumerate(bancos_sorted):
            dif_vs_top = mejor_b["vf"] - b_item["vf"]
            tabla_bancos_res.append({
                "Ranking": f"🥇 #{rk+1}" if rk == 0 else (f"🥈 #{rk+1}" if rk == 1 else f"🥉 #{rk+1}"),
                "Entidad Bancaria": b_item["nombre"],
                "Tasa Ofrecida": f"{fmt_n(b_item['tasa_orig']*100, 2)}% ({b_item['tipo']})",
                "TEA Equivalente (%)": f"{fmt_n(b_item['tea']*100, 4)}%",
                "Tasa Mensual Equivalente (%)": f"{fmt_n(b_item['tem']*100, 4)}%",
                "Monto Final Acumulado ($)": fmt_m(b_item["vf"]),
                "Intereses Ganados ($)": fmt_m(b_item["interes"]),
                "Diferencia vs. Mejor ($)": "🥇 Mejor Oferta" if rk == 0 else f"-${fmt_m(dif_vs_top)}"
            })

        df_bancos_res = pd.DataFrame(tabla_bancos_res)
        st.dataframe(df_bancos_res, hide_index=True)
        export_dataframe_button(df_bancos_res, "comparativa_ofertas_bancarias")

    # -------------------------------------------------------------
    # HERRAMIENTA X
    # -------------------------------------------------------------
    elif "X. Crédito Comercial" in herramienta_sel:
        st.subheader("🛠️ X. Crédito Comercial / Bienes de Capital (Pagos Anuales & Cuota Mensual)")
        
        xc1, xc2, xc3 = st.columns(3)
        with xc1:
            monto_x = smart_num_input("Monto del Bien / Crédito ($):", 12000000.0, key="calc10_monto")
            st.markdown(f'<div class="val-badge">💵 Préstamo: ${fmt_m(monto_x)}</div>', unsafe_allow_html=True)
        with xc2:
            plazo_meses_x = int(smart_num_input("Plazo en Meses:", 36.0, key="calc10_meses"))
            st.markdown(f'<div class="val-badge">⏳ Plazo: {plazo_meses_x} meses</div>', unsafe_allow_html=True)
        with xc3:
            tasa_sem_x = smart_num_input("Tasa Semestral (%):", 7.40, key="calc10_tsem") / 100.0
            st.markdown(f'<div class="val-badge">📈 Tasa Semestral: {fmt_n(tasa_sem_x*100, 2)}%</div>', unsafe_allow_html=True)

        anos_x = plazo_meses_x / 12.0
        tea_x = ((1 + tasa_sem_x) ** 2.0) - 1.0
        cuota_anual_x = monto_x * (tea_x / (1 - (1 + tea_x)**(-anos_x)))
        tem_x = ((1 + tea_x) ** (1/12.0)) - 1.0
        cuota_mensual_x = monto_x * (tem_x / (1 - (1 + tem_x)**(-plazo_meses_x)))
        int_totales_x = (cuota_anual_x * anos_x) - monto_x

        m_x1, m_x2, m_x3, m_x4 = st.columns(4)
        m_x1.metric("TEA Equivalente", f"{fmt_n(tea_x*100, 4)}%")
        m_x2.metric("Cuota Anual (PMT)", f"${fmt_m(cuota_anual_x)}")
        m_x3.metric("Cuota Mensual Equivalente", f"${fmt_m(cuota_mensual_x)}")
        m_x4.metric("Intereses Totales Anuales", f"${fmt_m(int_totales_x)}")

    # -------------------------------------------------------------
    # HERRAMIENTA XI
    # -------------------------------------------------------------
    elif "XI. Tasa Implícita Anual" in herramienta_sel:
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

    # -------------------------------------------------------------
    # HERRAMIENTA XII
    # -------------------------------------------------------------
    elif "XII. Valor Presente de Cero" in herramienta_sel:
        st.subheader("🛠️ XII. Valor Presente de Cero / Descuento (4 Decimales de Precisión)")
        
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

    # -------------------------------------------------------------
    # HERRAMIENTA XIII
    # -------------------------------------------------------------
    elif "XIII. Calculadora Universal de Cuotas" in herramienta_sel:
        st.subheader("🛠️ XIII. Calculadora Universal de Cuotas e Intereses de Préstamos (Precisión a 4 Decimales)")
        st.caption("Calcula el valor exacto de la cuota fija periódica expresada con 2 y 4 decimales.")
        
        u1, u2, u3 = st.columns(3)
        with u1:
            vp_u13 = smart_num_input("Monto del Préstamo (VP $):", 12000.0, key="calc13_vp")
            st.markdown(f'<div class="val-badge">💵 Préstamo: ${fmt_m(vp_u13)}</div>', unsafe_allow_html=True)
        with u2:
            n_u13 = int(smart_num_input("Número de Cuotas (n):", 45.0, key="calc13_n"))
            st.markdown(f'<div class="val-badge">📅 Cuotas: {n_u13}</div>', unsafe_allow_html=True)
        with u3:
            tasa_u13 = smart_num_input("Tasa Periódica / Anual (%):", 5.0, key="calc13_tasa") / 100.0
            st.markdown(f'<div class="val-badge">📈 Tasa: {fmt_n(tasa_u13*100, 2)}%</div>', unsafe_allow_html=True)

        if n_u13 > 0 and tasa_u13 > 0:
            pmt_exact = vp_u13 * (tasa_u13 / (1 - (1 + tasa_u13)**(-n_u13)))
            total_pagado_u13 = pmt_exact * n_u13
            int_totales_u13 = total_pagado_u13 - vp_u13

            col_res1, col_res2 = st.columns(2)
            with col_res1:
                st.metric("Cuota Fija (2 Decimales)", f"${fmt_n(pmt_exact, 2)}")
            with col_res2:
                st.metric("Cuota Fija Exacta (4 Decimales)", f"{fmt_n(pmt_exact, 4)}")

            st.info(f"• **Total Pagado al Final del Plazo:** ${fmt_m(total_pagado_u13)}\n"
                    f"• **Total Intereses Generados:** ${fmt_m(int_totales_u13)}")

    # -------------------------------------------------------------
    # HERRAMIENTA XIV
    # -------------------------------------------------------------
    else:
        st.subheader("🛠️ XIV. Calculadora de Costo Financiero Total (CFT) y Comisiones")
        st.caption("Calcula el Costo Financiero Total porcentual (%) y monetario ($) incluyendo gastos administrativos.")
        
        cft1, cft2, cft3 = st.columns(3)
        with cft1:
            vp_cft = smart_num_input("Monto del Crédito ($):", 1000000.0, key="calc14_vp")
            st.markdown(f'<div class="val-badge">💵 Crédito: ${fmt_m(vp_cft)}</div>', unsafe_allow_html=True)
        with cft2:
            tea_cft = smart_num_input("Tasa Efectiva Anual (TEA %):", 18.0, key="calc14_tea") / 100.0
            st.markdown(f'<div class="val-badge">📈 TEA: {fmt_n(tea_cft*100, 2)}%</div>', unsafe_allow_html=True)
        with cft3:
            comision_cft = smart_num_input("Comisión / Gastos Administrativos ($):", 20000.0, key="calc14_comision")
            st.markdown(f'<div class="val-badge">🧾 Comisión: ${fmt_m(comision_cft)}</div>', unsafe_allow_html=True)

        if vp_cft > 0:
            pct_comision = (comision_cft / vp_cft)
            cft_porcentual = (tea_cft + pct_comision) * 100.0
            interes_dinero = vp_cft * tea_cft
            cft_dinero = interes_dinero + comision_cft

            rcft1, rcft2, rcft3 = st.columns(3)
            rcft1.metric("Porcentaje de Comisión", f"{fmt_n(pct_comision*100, 2)}%")
            rcft2.metric("Costo Financiero Total (CFT %)", f"{fmt_n(cft_porcentual, 2)}%")
            rcft3.metric("Costo Financiero Total en Dinero ($)", f"${fmt_m(cft_dinero)}")

            st.success(f"• **Intereses Anuales:** ${fmt_m(interes_dinero)}\n"
                       f"• **Comisiones:** ${fmt_m(comision_cft)}\n"
                       f"• **Costo TotalAnual:** ${fmt_m(cft_dinero)} ({fmt_n(cft_porcentual, 2)}%)")

st.markdown("---")
st.caption("Plataforma de Simulación & Cálculo Financiero — Desarrollo Académico para la Comunidad Estudiantil")
