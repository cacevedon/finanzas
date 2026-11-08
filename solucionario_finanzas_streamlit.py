import streamlit as st
import numpy as np
import pandas as pd
import numpy_financial as npf
import math

# Configuración de página
st.set_page_config(
    page_title="04 Finanzas — Plataforma Web de Simulación & Ingeniería Financiera",
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

# Helper functions for LatAm formatting and parsing
def parse_latam_number(val_str):
    if not val_str or str(val_str).strip() == "":
        return 0.0
    s = str(val_str).strip().replace("$", "").replace("%", "").replace(" ", "")
    if "." in s and "," in s:
        s = s.replace(".", "").replace(",", ".")
    elif "," in s:
        s = s.replace(",", ".")
    elif "." in s:
        parts = s.split(".")
        if len(parts) > 2:
            s = s.replace(".", "")
        elif len(parts) == 2:
            if len(parts[1]) == 3 and 1 <= len(parts[0]) <= 3:
                s = s.replace(".", "")
    try:
        return float(s)
    except ValueError:
        return 0.0

def fmt_currency(val):
    try:
        val = float(val)
    except (ValueError, TypeError):
        return "$0"
    if abs(val - round(val)) < 1e-7:
        s = f"{int(round(val)):,}".replace(",", ".")
    else:
        s = f"{val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"${s}"

def fmt_num(val):
    try:
        val = float(val)
    except (ValueError, TypeError):
        return "0"
    if abs(val - round(val)) < 1e-7:
        return f"{int(round(val)):,}".replace(",", ".")
    else:
        return f"{val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def smart_num_input(label, default_val=0.0, key=None, is_currency=True, is_percent=False, help_text=None):
    if is_currency:
        init_str = fmt_currency(default_val) if default_val != 0 else "$0"
    elif is_percent:
        init_str = f"{default_val:.2f}%" if default_val != 0 else "0,0%"
    else:
        init_str = fmt_num(default_val) if default_val != 0 else "0"

    val_str = st.text_input(label, value=init_str, key=key, help=help_text or label)
    val_num = parse_latam_number(val_str)

    if is_currency:
        st.caption(f"📌 *Monto ingresado:* **{fmt_currency(val_num)}**")
    elif is_percent:
        st.caption(f"📌 *Tasa ingresada:* **{val_num:.4f}%**")
    else:
        st.caption(f"📌 *Valor ingresado:* **{fmt_num(val_num)}**")

    return val_num

# Encabezado Principal
st.markdown('<div class="main-header">04 FINANZAS — Plataforma de Simulación & Ingeniería Financiera</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Plataforma interactiva de cálculo y simulación desarrollada para la comunidad estudiantil.</div>', unsafe_allow_html=True)

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
st.sidebar.info("💡 **Tip:** Modifica los parámetros de los simuladores en tiempo real para evaluar diferentes escenarios financieros.")

# ==========================================
# MÓDULO 1: FUNDAMENTOS Y DECISIONES
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
        st.subheader("🎯 Evaluador de Decisiones de Inversión y Liquidez")
        monto_dec = smart_num_input("Capital o Excedente de Caja ($):", default_val=0.0, key="m1_monto", is_currency=True)
        tasa_dec = smart_num_input("Tasa de Rendimiento Ofrecida Mensual (%):", default_val=0.0, key="m1_tasa", is_percent=True)
        plazo_dec = smart_num_input("Plazo en Meses:", default_val=0.0, key="m1_plazo", is_currency=False)
        
        if monto_dec > 0 and tasa_dec > 0 and plazo_dec > 0:
            vf_dec = monto_dec * ((1 + tasa_dec/100.0) ** plazo_dec)
            int_dec = vf_dec - monto_dec
            st.success(f"• **Valor Futuro Proyectado:** **{fmt_currency(vf_dec)}**")
            st.info(f"• **Intereses Generados:** **{fmt_currency(int_dec)}**")
        else:
            st.info("Ingresa un monto, tasa y plazo superiores a cero para evaluar la decisión.")

# ==========================================
# MÓDULO 2: INTERÉS SIMPLE Y COMPUESTO
# ==========================================
elif modulo == "2. Interés Simple y Compuesto":
    st.header("Unidad 2: Interés Simple e Interés Compuesto")
    st.subheader("⚙️ Calculadora Interactiva de Interés")
    
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        vp_m2 = smart_num_input("Capital Inicial (VP $):", default_val=0.0, key="m2_vp", is_currency=True)
    with c2:
        tasa_m2 = smart_num_input("Tasa Periódica (%):", default_val=0.0, key="m2_tasa", is_percent=True)
    with c3:
        n_m2 = smart_num_input("Plazo (Períodos):", default_val=0.0, key="m2_n", is_currency=False)
    with c4:
        regimen_m2 = st.selectbox("Régimen:", ["Interés Compuesto", "Interés Simple", "Comparar Ambos"], key="m2_reg")

    if vp_m2 > 0 and n_m2 > 0:
        n_int = int(n_m2)
        r_per = tasa_m2 / 100.0
        vf_s = vp_m2 * (1 + r_per * n_int)
        vf_c = vp_m2 * ((1 + r_per) ** n_int)
        
        col_r1, col_r2, col_r3 = st.columns(3)
        col_r1.metric("Valor Futuro (Simple)", fmt_currency(vf_s))
        col_r2.metric("Valor Futuro (Compuesto)", fmt_currency(vf_c))
        col_r3.metric("Diferencia por Capitalización", fmt_currency(vf_c - vf_s))

        df_m2 = pd.DataFrame({
            "Período": list(range(0, n_int + 1)),
            "Interés Simple ($)": [vp_m2 * (1 + r_per * t) for t in range(0, n_int + 1)],
            "Interés Compuesto ($)": [vp_m2 * ((1 + r_per) ** t) for t in range(0, n_int + 1)]
        })
        st.line_chart(df_m2.set_index("Período"))
    else:
        st.info("Ingresa los parámetros del capital y plazo para ver la proyección.")

# ==========================================
# MÓDULO 3: CONVERSIÓN DE TASAS
# ==========================================
elif modulo == "3. Conversión de Tasas (TNA/TEA)":
    st.header("Unidad 3: Conversión y Decodificación de Tasas")
    
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        st.subheader("🔄 Conversor TNA ➔ TEA")
        tna_m3 = smart_num_input("Tasa Nominal Anual (TNA %):", default_val=0.0, key="m3_tna", is_percent=True)
        freq_dict = {
            "Mensual (m=12)": 12,
            "Bimestral (m=6)": 6,
            "Trimestral (m=4)": 4,
            "Cuatrimestral (m=3)": 3,
            "Semestral (m=2)": 2,
            "Diaria (m=360)": 360
        }
        freq_sel = st.selectbox("Frecuencia de Capitalización (m):", list(freq_dict.keys()), key="m3_freq")
        m_m3 = freq_dict[freq_sel]
        
        if tna_m3 > 0:
            i_per = (tna_m3 / 100.0) / m_m3
            tea_calc = ((1 + i_per) ** m_m3) - 1.0
            st.write(f"• **Tasa Periódica ($i$):** {i_per*100:.4f}%")
            st.metric("Tasa Efectiva Anual (TEA Equivalent)", f"{tea_calc*100:.4f}%")

    with col_t2:
        st.subheader("⚖️ Comparador de Alternativas Financieras")
        tasa_alt1 = smart_num_input("Alternativa A (TNA % Nominal):", default_val=0.0, key="m3_t1", is_percent=True)
        freq_alt1 = st.selectbox("Frecuencia Cap. Alt. A:", list(freq_dict.keys()), key="m3_f1")
        tasa_alt2 = smart_num_input("Alternativa B (TEA % Efectiva):", default_val=0.0, key="m3_t2", is_percent=True)
        
        if tasa_alt1 > 0 and tasa_alt2 > 0:
            m1_val = freq_dict[freq_alt1]
            tea_a = ((1 + (tasa_alt1/100.0)/m1_val)**m1_val) - 1.0
            tea_b = tasa_alt2 / 100.0
            diff_pct = abs(tea_a - tea_b) * 100.0
            
            st.write(f"• **TEA Alternativa A:** **{tea_a*100:.4f}%**")
            st.write(f"• **TEA Alternativa B:** **{tea_b*100:.4f}%**")
            st.success(f"• **Diferencia Porcentual de Rendimiento:** **{diff_pct:.4f}%**")

# ==========================================
# MÓDULO 4: ANUALIDADES Y AMORTIZACIÓN
# ==========================================
elif modulo == "4. Anualidades y Amortización":
    st.header("Unidad 4: Anualidades y Tablas de Amortización")
    st.subheader("💳 Simulador de Préstamos y Amortización (Método Francés)")
    
    ac1, ac2, ac3 = st.columns(3)
    with ac1:
        vp_m4 = smart_num_input("Monto del Préstamo ($):", default_val=0.0, key="m4_vp", is_currency=True)
    with ac2:
        tasa_m4 = smart_num_input("Tasa Efectiva Mensual (%):", default_val=0.0, key="m4_tasa", is_percent=True)
    with ac3:
        plazo_m4 = smart_num_input("Plazo en Meses (n):", default_val=0.0, key="m4_n", is_currency=False)
        
    if vp_m4 > 0 and tasa_m4 > 0 and plazo_m4 > 0:
        n_m4_int = int(plazo_m4)
        r_m4 = tasa_m4 / 100.0
        cuota_m4 = vp_m4 * (r_m4 / (1 - (1 + r_m4)**(-n_m4_int)))
        
        st.metric("Cuota Mensual Calculada (R)", fmt_currency(cuota_m4))
        
        saldo = vp_m4
        amort_data = []
        for mes in range(1, n_m4_int + 1):
            int_mes = saldo * r_m4
            cap_mes = cuota_m4 - int_mes
            saldo_fin = max(0.0, saldo - cap_mes)
            amort_data.append({
                "Mes": mes,
                "Saldo Inicial ($)": fmt_currency(saldo),
                "Cuota ($)": fmt_currency(cuota_m4),
                "Interés ($)": fmt_currency(int_mes),
                "Amortización ($)": fmt_currency(cap_mes),
                "Saldo Final ($)": fmt_currency(saldo_fin)
            })
            saldo = saldo_fin
            
        df_amort = pd.DataFrame(amort_data)
        st.markdown("#### Tabla de Amortización Dinámica")
        st.dataframe(df_amort, hide_index=True)
        
        # Download Excel
        buf_m4 = pd.ExcelWriter("/workspace/scratch/amortizacion.xlsx", engine="openpyxl")
        df_amort.to_excel(buf_m4, index=False, sheet_name="Amortización")
        buf_m4.close()
        with open("/workspace/scratch/amortizacion.xlsx", "rb") as f_ex:
            st.download_button("📥 Exportar Tabla de Amortización a Excel (.xlsx)", f_ex, file_name="tabla_amortizacion.xlsx")
    else:
        st.info("Ingresa el monto del préstamo, tasa y plazo para generar la tabla.")

# ==========================================
# MÓDULO 5: GRADIENTES FINANCIEROS
# ==========================================
elif modulo == "5. Gradientes Financieros":
    st.header("Unidad 5: Gradientes Financieros (Series Variables)")
    st.subheader("📈 Comparativa de Series: Constante vs. Aritmética vs. Geométrica")
    
    gc1, gc2, gc3, gc4 = st.columns(4)
    with gc1:
        base_a = smart_num_input("Flujo Base Inicial (A $):", default_val=0.0, key="m5_base", is_currency=True)
    with gc2:
        grad_g = smart_num_input("Gradiente Aritmético (G $):", default_val=0.0, key="m5_g", is_currency=True)
    with gc3:
        grad_pct = smart_num_input("Gradiente Geométrico (g %):", default_val=0.0, key="m5_gpct", is_percent=True)
    with gc4:
        n_g = smart_num_input("Número de Períodos (n):", default_val=0.0, key="m5_n", is_currency=False)
        
    if base_a > 0 and n_g > 0:
        n_g_int = int(n_g)
        g_pct_dec = grad_pct / 100.0
        grad_df = pd.DataFrame({
            "Período": list(range(1, n_g_int + 1)),
            "Serie Constante ($)": [base_a] * n_g_int,
            "Gradiente Aritmético (+G $)": [base_a + (t - 1) * grad_g for t in range(1, n_g_int + 1)],
            "Gradiente Geométrico (+g $)": [base_a * ((1 + g_pct_dec)**(t - 1)) for t in range(1, n_g_int + 1)]
        })
        st.line_chart(grad_df.set_index("Período"))
    else:
        st.info("Ingresa el flujo base y número de períodos para proyectar las series.")

# ==========================================
# MÓDULO 6: PRESUPUESTO Y FLUJO DE CAJA (FIX X-AXIS ORDER)
# ==========================================
elif modulo == "6. Presupuesto y Flujo de Caja":
    st.header("Unidad 6: Presupuestos y Control de Caja Operacional")
    st.subheader("📊 Simulador de Presupuesto Mensual a 12 Meses con Inflación")
    
    pc1, pc2, pc3, pc4 = st.columns(4)
    with pc1:
        v_base = smart_num_input("Ventas Mes 1 ($):", default_val=0.0, key="m6_vbase", is_currency=True)
    with pc2:
        g_ventas = smart_num_input("Crecimiento Ventas Mensual (%):", default_val=0.0, key="m6_gventas", is_percent=True)
    with pc3:
        inf_m = smart_num_input("Inflación Costos Mensual (%):", default_val=0.0, key="m6_inf", is_percent=True)
    with pc4:
        caja_ini = smart_num_input("Caja Inicial ($):", default_val=0.0, key="m6_caja", is_currency=True)
        
    if v_base > 0:
        g_v_dec = g_ventas / 100.0
        inf_dec = inf_m / 100.0
        p_data = []
        caja_acum = caja_ini
        
        for m in range(1, 13):
            v_m = v_base * ((1 + g_v_dec)**(m - 1))
            c_m = (v_m * 0.40) * ((1 + inf_dec)**(m - 1))
            f_m = 5000.0 * ((1 + inf_dec)**(m - 1))
            egresos_tot = c_m + f_m
            f_neto = v_m - egresos_tot
            caja_acum += f_neto
            
            p_data.append({
                "Mes_ID": m,
                "Mes": f"Mes {m}",
                "Ventas ($)": v_m,
                "Total Egresos ($)": egresos_tot,
                "Flujo Neto ($)": f_neto,
                "Caja Acumulada ($)": caja_acum
            })
            
        df_pres = pd.DataFrame(p_data)
        
        # RIGOROUS FIX FOR X-AXIS ORDERING:
        # Use Categorical index with explicit ordered categories [Mes 1, Mes 2, ..., Mes 12]
        cat_order = [f"Mes {i}" for i in range(1, 13)]
        df_pres["Mes"] = pd.Categorical(df_pres["Mes"], categories=cat_order, ordered=True)
        
        st.markdown("#### Tabla de Proyección Mensual de Caja")
        df_pres_disp = df_pres.copy()
        for col in ["Ventas ($)", "Total Egresos ($)", "Flujo Neto ($)", "Caja Acumulada ($)"]:
            df_pres_disp[col] = df_pres_disp[col].apply(fmt_currency)
        st.dataframe(df_pres_disp.drop(columns=["Mes_ID"]), hide_index=True)
        
        st.markdown("#### Gráfico Ordenado: Ventas vs. Egresos por Mes")
        st.bar_chart(df_pres.set_index("Mes")[["Ventas ($)", "Total Egresos ($)"]])
        
        st.markdown("#### Gráfico de Evolución de Caja Acumulada")
        st.line_chart(df_pres.set_index("Mes")[["Caja Acumulada ($)"]])
    else:
        st.info("Ingresa el monto de ventas iniciales para generar el presupuesto.")

# ==========================================
# MÓDULO 7: EVALUACIÓN DE PROYECTOS
# ==========================================
elif modulo == "7. Evaluación de Proyectos (VAN/TIR)":
    st.header("Unidad 7: Evaluación Financiera de Proyectos")
    
    st.subheader("🎯 Punto de Equilibrio Operacional")
    eq1, eq2, eq3 = st.columns(3)
    with eq1:
        cf_val = smart_num_input("Costos Fijos Totales ($):", default_val=0.0, key="m7_cf", is_currency=True)
    with eq2:
        p_val = smart_num_input("Precio Unitario ($):", default_val=0.0, key="m7_p", is_currency=True)
    with eq3:
        cv_val = smart_num_input("Costo Variable Unitario ($):", default_val=0.0, key="m7_cv", is_currency=True)
        
    if cf_val > 0 and p_val > cv_val:
        mc_u = p_val - cv_val
        q_eq = cf_val / mc_u
        ing_eq = q_eq * p_val
        st.success(f"• **Punto de Equilibrio en Unidades:** **{fmt_num(q_eq)} unidades**")
        st.success(f"• **Ingreso de Equilibrio:** **{fmt_currency(ing_eq)}**")
    else:
        st.info("Ingresa los costos fijos, precio y costo variable (con precio > costo variable) para calcular.")
        
    st.markdown("---")
    st.subheader("💰 Evaluación de Flujos de Caja (VAN y TIR)")
    
    inv_ini = smart_num_input("Inversión Inicial ($):", default_val=0.0, key="m7_inv", is_currency=True)
    tmar_val = smart_num_input("Tasa de Descuento / TMAR (%):", default_val=0.0, key="m7_tmar", is_percent=True)
    
    st.write("Ingresa los flujos proyectados a 5 años:")
    fc_cols = st.columns(5)
    flujos = []
    for idx, col in enumerate(fc_cols):
        with col:
            f_val = smart_num_input(f"Año {idx+1} ($):", default_val=0.0, key=f"m7_f_{idx}", is_currency=True)
            flujos.append(f_val)
            
    if inv_ini > 0 and tmar_val > 0 and any(f > 0 for f in flujos):
        tmar_dec = tmar_val / 100.0
        van_val = npf.npv(tmar_dec, [0] + flujos) - inv_ini
        tir_val = npf.irr([-inv_ini] + flujos)
        
        col_v1, col_v2 = st.columns(2)
        col_v1.metric("Valor Actual Neto (VAN)", fmt_currency(van_val), delta="Viable" if van_val > 0 else "No Viable")
        col_v2.metric("Tasa Interna de Retorno (TIR)", f"{tir_val*100:.2f}%", delta="TIR > TMAR" if tir_val > tmar_dec else "TIR < TMAR")

# ==========================================
# MÓDULO 8: CALCULADORAS ESPECIALIZADAS Y SIMULADORES
# ==========================================
elif modulo == "8. Calculadoras Especializadas y Simuladores":
    st.header("Unidad 8: Calculadoras Especializadas e Ingeniería Financiera")
    st.markdown("Suite avanzada de 14 herramientas cuantitativas de cómputo financiero con entradas limpias en cero.")
    
    herramientas = [
        "I. Desglose de Interés y Amortización para Cuota k con Convertidor",
        "II. Valor Futuro con Interés Compuesto (Plazos Enteros y Fraccionados)",
        "III. Valor Futuro de Anualidades y Fondos de Ahorro",
        "IV. Valuación de Flujos Múltiples e Irregulares (VP y VF)",
        "V. Despeje de Plazo Requerido (n) y Tasa Implícita",
        "VI. Conversión Avanzada de Tasas Nominales/Efectivas y Spread",
        "VII. Valor Presente (VP) de Pagos Futuros Específicos Discretos",
        "VIII. Valor Futuro (VF) de Depósitos Proyectados Discretos (Tasas Variables)",
        "IX. Comparador de Ofertas Bancarias a Plazo Fijo (Múltiples Bancos y Tasas)",
        "X. Crédito Comercial / Bienes de Capital",
        "XI. Tasa Implícita Anual para Créditos o Inversiones de Pago Único",
        "XII. Valor Presente de Cero / Descuento (4 Decimales)",
        "XIII. Calculadora Universal de Cuotas e Intereses de Préstamos (4 Decimales)",
        "XIV. Calculadora de Costo Financiero Total (CFT) y Comisiones"
    ]
    
    h_sel = st.selectbox("Selecciona la Herramienta Financiera a Utilizar:", herramientas)
    
    # ----------------------------------------------------
    # H1
    # ----------------------------------------------------
    if "I. Desglose" in h_sel:
        st.subheader("I. Desglose de Interés y Amortización para Cuota k")
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            vp_h1 = smart_num_input("Monto del Préstamo ($):", default_val=0.0, key="h1_vp", is_currency=True)
        with c2:
            tasa_h1 = smart_num_input("Tasa Anual (%):", default_val=0.0, key="h1_tasa", is_percent=True)
        with c3:
            n_h1 = smart_num_input("Plazo en Cuotas (n):", default_val=0.0, key="h1_n", is_currency=False)
        with c4:
            k_h1 = smart_num_input("Número de Cuota a Consultar (k):", default_val=0.0, key="h1_k", is_currency=False)
            
        if vp_h1 > 0 and tasa_h1 > 0 and n_h1 > 0 and k_h1 > 0:
            n_int = int(n_h1)
            k_int = int(k_h1)
            r_per = (tasa_h1 / 100.0) / 12.0
            pmt = vp_h1 * (r_per / (1 - (1 + r_per)**(-n_int)))
            
            saldo = vp_h1
            for m in range(1, k_int):
                int_m = saldo * r_per
                cap_m = pmt - int_m
                saldo -= cap_m
                
            int_k = saldo * r_per
            cap_k = pmt - int_k
            saldo_k = max(0.0, saldo - cap_k)
            
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Cuota Mensual (R)", fmt_currency(pmt))
            m2.metric(f"Interés Cuota #{k_int}", fmt_currency(int_k))
            m3.metric(f"Amortización Cuota #{k_int}", fmt_currency(cap_k))
            m4.metric(f"Saldo Tras Cuota #{k_int}", fmt_currency(saldo_k))
        else:
            st.info("Ingresa los datos del préstamo superiores a cero para calcular la cuota k.")

    # ----------------------------------------------------
    # H2
    # ----------------------------------------------------
    elif "II. Valor Futuro" in h_sel:
        st.subheader("II. Valor Futuro con Interés Compuesto")
        c1, c2, c3 = st.columns(3)
        with c1:
            vp_h2 = smart_num_input("Capital Inicial (VP $):", default_val=0.0, key="h2_vp", is_currency=True)
        with c2:
            tasa_h2 = smart_num_input("Tasa Anual (%):", default_val=0.0, key="h2_tasa", is_percent=True)
        with c3:
            meses_h2 = smart_num_input("Plazo en Meses:", default_val=0.0, key="h2_meses", is_currency=False)
            
        if vp_h2 > 0 and tasa_h2 > 0 and meses_h2 > 0:
            i_dec = tasa_h2 / 100.0
            vf_h2 = vp_h2 * ((1 + i_dec) ** (meses_h2 / 12.0))
            st.success(f"• **Valor Futuro Calculado:** **{fmt_currency(vf_h2)}**")

    # ----------------------------------------------------
    # H3
    # ----------------------------------------------------
    elif "III. Valor Futuro de Anualidades" in h_sel:
        st.subheader("III. Valor Futuro de Anualidades y Fondos de Ahorro")
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            r_h3 = smart_num_input("Aporte Periódico (R $):", default_val=0.0, key="h3_r", is_currency=True)
        with c2:
            tasa_h3 = smart_num_input("Tasa Periódica (%):", default_val=0.0, key="h3_tasa", is_percent=True)
        with c3:
            n_h3 = smart_num_input("Número de Períodos (n):", default_val=0.0, key="h3_n", is_currency=False)
        with c4:
            tipo_h3 = st.selectbox("Modalidad:", ["Vencida (Fin de Período)", "Anticipada (Inicio de Período)"], key="h3_tipo")
            
        if r_h3 > 0 and tasa_h3 > 0 and n_h3 > 0:
            i_dec = tasa_h3 / 100.0
            n_int = int(n_h3)
            vf_h3 = r_h3 * (((1 + i_dec)**n_int - 1) / i_dec)
            if "Anticipada" in tipo_h3:
                vf_h3 *= (1 + i_dec)
            st.success(f"• **Valor Futuro Acumulado:** **{fmt_currency(vf_h3)}**")

    # ----------------------------------------------------
    # H4
    # ----------------------------------------------------
    elif "IV. Valuación de Flujos Múltiples" in h_sel:
        st.subheader("IV. Valuación de Flujos Múltiples e Irregulares")
        c1, c2 = st.columns(2)
        with c1:
            tasa_h4 = smart_num_input("Tasa de Descuento/Capitalización Periódica (%):", default_val=0.0, key="h4_tasa", is_percent=True)
        with c2:
            n_flujos_h4 = smart_num_input("Cantidad de Flujos a Ingresar:", default_val=0.0, key="h4_cant", is_currency=False)
            
        n_cant = int(n_flujos_h4)
        if n_cant > 0 and tasa_h4 > 0:
            flujos_h4 = []
            f_cols = st.columns(min(n_cant, 5))
            for idx in range(n_cant):
                with f_cols[idx % 5]:
                    f_val = smart_num_input(f"Flujo Período {idx+1} ($):", default_val=0.0, key=f"h4_f_{idx}", is_currency=True)
                    flujos_h4.append(f_val)
                    
            r_dec = tasa_h4 / 100.0
            vp_tot = sum(f / ((1 + r_dec)**(idx+1)) for idx, f in enumerate(flujos_h4))
            vf_tot = vp_tot * ((1 + r_dec)**n_cant)
            
            st.metric("Valor Presente Total (t=0)", fmt_currency(vp_tot))
            st.metric("Valor Futuro Total (t=N)", fmt_currency(vf_tot))

    # ----------------------------------------------------
    # H5
    # ----------------------------------------------------
    elif "V. Despeje de Plazo" in h_sel:
        st.subheader("V. Despeje de Plazo Requerido (n) y Tasa Implícita")
        c1, c2, c3 = st.columns(3)
        with c1:
            vp_h5 = smart_num_input("Capital Inicial (VP $):", default_val=0.0, key="h5_vp", is_currency=True)
        with c2:
            vf_h5 = smart_num_input("Meta de Capital (VF $):", default_val=0.0, key="h5_vf", is_currency=True)
        with c3:
            tasa_h5 = smart_num_input("Tasa Anual (%):", default_val=0.0, key="h5_tasa", is_percent=True)
            
        if vp_h5 > 0 and vf_h5 > vp_h5 and tasa_h5 > 0:
            i_dec = tasa_h5 / 100.0
            n_anos = math.log(vf_h5 / vp_h5) / math.log(1 + i_dec)
            st.success(f"• **Plazo Requerido:** **{n_anos:.2f} años** ({n_anos*12:.1f} meses)")

    # ----------------------------------------------------
    # H6
    # ----------------------------------------------------
    elif "VI. Conversión Avanzada" in h_sel:
        st.subheader("VI. Conversión Avanzada de Tasas Nominales/Efectivas")
        c1, c2 = st.columns(2)
        with c1:
            tna_h6 = smart_num_input("Tasa Nominal Anual (TNA %):", default_val=0.0, key="h6_tna", is_percent=True)
        with c2:
            freq_h6 = smart_num_input("Frecuencia de Capitalización (m):", default_val=0.0, key="h6_m", is_currency=False)
            
        if tna_h6 > 0 and freq_h6 > 0:
            m_val = float(freq_h6)
            i_per = (tna_h6 / 100.0) / m_val
            tea_h6 = ((1 + i_per)**m_val) - 1.0
            st.metric("Tasa Efectiva Anual (TEA)", f"{tea_h6*100:.4f}%")

    # ----------------------------------------------------
    # H7
    # ----------------------------------------------------
    elif "VII. Valor Presente (VP) de Pagos Futuros" in h_sel:
        st.subheader("VII. Valor Presente (VP) de Pagos Futuros Específicos Discretos")
        c1, c2 = st.columns(2)
        with c1:
            tasa_h7 = smart_num_input("Tasa Mensual de Descuento (%):", default_val=0.0, key="h7_tasa", is_percent=True)
        with c2:
            cant_h7 = smart_num_input("Cantidad de Pagos Discretos:", default_val=0.0, key="h7_cant", is_currency=False)
            
        n_cant = int(cant_h7)
        if n_cant > 0 and tasa_h7 > 0:
            pagos_h7 = []
            for idx in range(n_cant):
                col_m, col_val = st.columns(2)
                with col_m:
                    m_pago = smart_num_input(f"Mes del Pago #{idx+1}:", default_val=0.0, key=f"h7_m_{idx}", is_currency=False)
                with col_val:
                    v_pago = smart_num_input(f"Monto Pago #{idx+1} ($):", default_val=0.0, key=f"h7_v_{idx}", is_currency=True)
                pagos_h7.append((int(m_pago), v_pago))
                
            r_dec = tasa_h7 / 100.0
            vp_tot = sum(v / ((1 + r_dec)**m) for m, v in pagos_h7 if m > 0)
            st.success(f"• **Valor Presente Consolidado (t=0):** **{fmt_currency(vp_tot)}**")

    # ----------------------------------------------------
    # H8
    # ----------------------------------------------------
    elif "VIII. Valor Futuro (VF) de Depósitos Proyectados" in h_sel:
        st.subheader("VIII. Valor Futuro (VF) de Depósitos Proyectados Discretos (Tasas Variables)")
        
        c1, c2, c3 = st.columns(3)
        with c1:
            horizonte_h8 = smart_num_input("Horizonte Total en Meses (N):", default_val=0.0, key="h8_horizonte", is_currency=False)
        with c2:
            tasa_ini_h8 = smart_num_input("Tasa Inicial Mensual (%):", default_val=0.0, key="h8_tasa_ini", is_percent=True)
        with c3:
            modo_h8 = st.selectbox("Momento del Depósito:", ["Fin del Mes / Vencido (por defecto)", "Inicio del Mes / Anticipado"], key="h8_modo")
            
        col_ch1, col_ch2 = st.columns(2)
        with col_ch1:
            mes_cambio_h8 = smart_num_input("Mes a partir del cual cambia la tasa:", default_val=0.0, key="h8_mcamb", is_currency=False)
        with col_ch2:
            tasa_nueva_h8 = smart_num_input("Nueva Tasa Mensual (%):", default_val=0.0, key="h8_tnueva", is_percent=True)
            
        cant_dep_h8 = smart_num_input("Cantidad de Depósitos a Realizar:", default_val=0.0, key="h8_cdeps", is_currency=False)
        
        N_int = int(horizonte_h8)
        n_cdeps = int(cant_dep_h8)
        
        if N_int > 0 and tasa_ini_h8 > 0 and n_cdeps > 0:
            depositos_dict = {}
            st.markdown("#### Ingreso de Depósitos Específicos")
            d_cols = st.columns(min(n_cdeps, 4))
            for d_idx in range(n_cdeps):
                with d_cols[d_idx % 4]:
                    m_dep = smart_num_input(f"Mes Depósito #{d_idx+1}:", default_val=0.0, key=f"h8_mdep_{d_idx}", is_currency=False)
                    v_dep = smart_num_input(f"Monto Depósito #{d_idx+1} ($):", default_val=0.0, key=f"h8_vdep_{d_idx}", is_currency=True)
                    if int(m_dep) > 0 and v_dep > 0:
                        depositos_dict[int(m_dep)] = v_dep
                        
            # Array de tasas por mes
            tasas_mes = []
            m_cambio_int = int(mes_cambio_h8)
            for m in range(1, N_int + 1):
                if m_cambio_int > 0 and m >= m_cambio_int and tasa_nueva_h8 > 0:
                    tasas_mes.append(tasa_nueva_h8 / 100.0)
                else:
                    tasas_mes.append(tasa_ini_h8 / 100.0)
                    
            es_vencido = "Vencido" in modo_h8
            desglose_h8 = []
            for d_idx, (m_dep, monto_dep) in enumerate(sorted(depositos_dict.items())):
                if es_vencido:
                    meses_cap = max(0, N_int - m_dep)
                    factor = 1.0
                    for m in range(m_dep + 1, N_int + 1):
                        factor *= (1.0 + tasas_mes[m - 1])
                else:
                    meses_cap = max(0, N_int - m_dep + 1)
                    factor = 1.0
                    for m in range(m_dep, N_int + 1):
                        factor *= (1.0 + tasas_mes[m - 1])
                        
                vf_ind = monto_dep * factor
                desglose_h8.append({
                    "Depósito #": d_idx + 1,
                    "Mes del Depósito": f"Mes {m_dep}",
                    "Monto Depositado ($)": fmt_currency(monto_dep),
                    "Meses Capitalizados": meses_cap,
                    "Valor Futuro del Depósito ($)": fmt_currency(vf_ind),
                    "_vf_raw": vf_ind
                })
                
            if desglose_h8:
                vf_total = sum(item["_vf_raw"] for item in desglose_h8)
                df_desglose = pd.DataFrame(desglose_h8).drop(columns=["_vf_raw"])
                
                st.markdown("#### Desglose del Valor Futuro Individual de Cada Depósito")
                st.dataframe(df_desglose, hide_index=True)
                st.success(f"• **Valor Futuro Total Acumulado (t={N_int}):** **{fmt_currency(vf_total)}**")

    # ----------------------------------------------------
    # H9
    # ----------------------------------------------------
    elif "IX. Comparador de Ofertas Bancarias" in h_sel:
        st.subheader("IX. Comparador de Ofertas Bancarias a Plazo Fijo / Depósitos")
        
        c1, c2 = st.columns(2)
        with c1:
            monto_h9 = smart_num_input("Monto del Depósito ($):", default_val=0.0, key="h9_monto", is_currency=True)
        with c2:
            plazo_m_h9 = smart_num_input("Plazo Total en Meses:", default_val=0.0, key="h9_plazo_m", is_currency=False)
            
        n_bancos_h9 = smart_num_input("Cantidad de Entidades Bancarias a Comparar:", default_val=2.0, key="h9_n_bancos", is_currency=False)
        n_b_int = max(2, min(5, int(n_bancos_h9)))
        
        if monto_h9 > 0 and plazo_m_h9 > 0:
            opciones_tasa = [
                "TEA (Efectiva Anual)",
                "TEC (Efectiva Cuatrimestral)",
                "TES (Efectiva Semestral)",
                "TET (Efectiva Trimestral)",
                "TEB (Efectiva Bimestral)",
                "TEM (Efectiva Mensual)",
                "TED (Efectiva Diaria)",
                "TNC (Nominal Cuatrimestral - Cap. Mensual m=4)",
                "TNS (Nominal Semestral - Cap. Mensual m=6)",
                "TNT (Nominal Trimestral - Cap. Mensual m=3)",
                "TNA (Nominal Anual)",
                "Tasa Simple Cuatrimestral",
                "Tasa Simple Anual"
            ]
            
            bancos_data = []
            for idx in range(n_b_int):
                st.markdown(f"**Configuración Banco #{idx+1}**")
                cb1, cb2, cb3 = st.columns(3)
                with cb1:
                    b_name = st.text_input(f"Nombre del Banco #{idx+1}:", value="", placeholder=f"Banco {idx+1}", key=f"h9_name_{idx}")
                    name_final = b_name.strip() if b_name.strip() else f"Banco {idx+1}"
                with cb2:
                    b_tipo = st.selectbox(f"Tipo de Tasa Banco #{idx+1}:", opciones_tasa, key=f"h9_tipo_{idx}")
                with cb3:
                    b_tasa = smart_num_input(f"Tasa Banco #{idx+1} (%):", default_val=0.0, key=f"h9_tasa_{idx}", is_percent=True)
                    
                if b_tasa > 0:
                    r_val = b_tasa / 100.0
                    # Convierte a TEA
                    if "TEA" in b_tipo:
                        tea_b = r_val
                    elif "TEC" in b_tipo:
                        tea_b = ((1 + r_val)**3) - 1.0
                    elif "TES" in b_tipo:
                        tea_b = ((1 + r_val)**2) - 1.0
                    elif "TET" in b_tipo:
                        tea_b = ((1 + r_val)**4) - 1.0
                    elif "TEB" in b_tipo:
                        tea_b = ((1 + r_val)**6) - 1.0
                    elif "TEM" in b_tipo:
                        tea_b = ((1 + r_val)**12) - 1.0
                    elif "TED" in b_tipo:
                        tea_b = ((1 + r_val)**360) - 1.0
                    elif "TNC" in b_tipo:
                        tea_b = ((1 + r_val/4.0)**12) - 1.0
                    elif "TNS" in b_tipo:
                        tea_b = ((1 + r_val/6.0)**12) - 1.0
                    elif "TNT" in b_tipo:
                        tea_b = ((1 + r_val/3.0)**12) - 1.0
                    elif "TNA" in b_tipo:
                        tea_b = ((1 + r_val/12.0)**12) - 1.0
                    elif "Simple Cuatrimestral" in b_tipo:
                        tea_b = (1 + r_val*3) - 1.0
                    else:
                        tea_b = r_val
                        
                    tem_b = ((1 + tea_b)**(1/12.0)) - 1.0
                    vf_b = monto_h9 * ((1 + tea_b)**(plazo_m_h9 / 12.0))
                    int_b = vf_b - monto_h9
                    
                    bancos_data.append({
                        "Entidad Bancaria": name_final,
                        "Tasa Ofrecida": f"{b_tasa:.2f}% ({b_tipo.split(' ')[0]})",
                        "TEA Equivalente (%)": f"{tea_b*100:.4f}%",
                        "Tasa Mensual Equivalente (%)": f"{tem_b*100:.4f}%",
                        "Monto Final Acumulado ($)": fmt_currency(vf_b),
                        "Intereses Ganados ($)": fmt_currency(int_b),
                        "_vf_raw": vf_b
                    })
                    
            if bancos_data:
                bancos_sorted = sorted(bancos_data, key=lambda x: x["_vf_raw"], reverse=True)
                best_vf = bancos_sorted[0]["_vf_raw"]
                for b_item in bancos_sorted:
                    diff_v = best_vf - b_item["_vf_raw"]
                    b_item["Diferencia vs. Mejor ($)"] = "🥇 Mejor Oferta" if diff_v < 1e-5 else f"-{fmt_currency(diff_v)}"
                    
                df_bancos = pd.DataFrame(bancos_sorted).drop(columns=["_vf_raw"])
                st.markdown("#### Tabla Comparativa de Ofertas Bancarias")
                st.dataframe(df_bancos, hide_index=True)

    # ----------------------------------------------------
    # H10
    # ----------------------------------------------------
    elif "X. Crédito Comercial" in h_sel:
        st.subheader("X. Crédito Comercial / Bienes de Capital")
        c1, c2, c3 = st.columns(3)
        with c1:
            monto_h10 = smart_num_input("Monto del Préstamo ($):", default_val=0.0, key="hx_monto", is_currency=True)
        with c2:
            tasa_sem_h10 = smart_num_input("Tasa Semestral (%):", default_val=0.0, key="hx_tsem", is_percent=True)
        with c3:
            anos_h10 = smart_num_input("Plazo en Años:", default_val=0.0, key="hx_anos", is_currency=False)
            
        if monto_h10 > 0 and tasa_sem_h10 > 0 and anos_h10 > 0:
            r_sem = tasa_sem_h10 / 100.0
            tea_h10 = ((1 + r_sem)**2) - 1.0
            n_anos_int = int(anos_h10)
            pmt_anual = monto_h10 * (tea_h10 / (1 - (1 + tea_h10)**(-n_anos_int)))
            r_mens = ((1 + tea_h10)**(1/12.0)) - 1.0
            pmt_mens = monto_h10 * (r_mens / (1 - (1 + r_mens)**(-n_anos_int * 12)))
            
            st.metric("Tasa Efectiva Anual (TEA)", f"{tea_h10*100:.4f}%")
            st.metric("Cuota Anual Equivalente", fmt_currency(pmt_anual))
            st.metric("Cuota Mensual Equivalente", fmt_currency(pmt_mens))

    # ----------------------------------------------------
    # H11
    # ----------------------------------------------------
    elif "XI. Tasa Implícita Anual" in h_sel:
        st.subheader("XI. Tasa Implícita Anual para Créditos/Inversiones de Pago Único")
        c1, c2, c3 = st.columns(3)
        with c1:
            vp_h11 = smart_num_input("Monto Inicial / Préstamo ($):", default_val=0.0, key="hxi_vp", is_currency=True)
        with c2:
            vf_h11 = smart_num_input("Monto Final a Devolver ($):", default_val=0.0, key="hxi_vf", is_currency=True)
        with c3:
            trim_h11 = smart_num_input("Plazo en Trimestres:", default_val=0.0, key="hxi_trim", is_currency=False)
            
        if vp_h11 > 0 and vf_h11 > vp_h11 and trim_h11 > 0:
            n_trim = float(trim_h11)
            i_trim = ((vf_h11 / vp_h11)**(1.0 / n_trim)) - 1.0
            tea_h11 = ((1 + i_trim)**4) - 1.0
            st.metric("Tasa Trimestral Implícita", f"{i_trim*100:.4f}%")
            st.metric("Tasa Efectiva Anual (TEA Implícita)", f"{tea_h11*100:.4f}%")

    # ----------------------------------------------------
    # H12
    # ----------------------------------------------------
    elif "XII. Valor Presente de Cero" in h_sel:
        st.subheader("XII. Valor Presente de Cero / Descuento (4 Decimales)")
        c1, c2, c3 = st.columns(3)
        with c1:
            vf_h12 = smart_num_input("Monto Futuro (VF $):", default_val=0.0, key="h12_vf", is_currency=True)
        with c2:
            tea_h12 = smart_num_input("Tasa Efectiva Anual (TEA %):", default_val=0.0, key="h12_tea", is_percent=True)
        with c3:
            meses_h12 = smart_num_input("Plazo en Meses:", default_val=0.0, key="h12_meses", is_currency=False)
            
        if vf_h12 > 0 and tea_h12 > 0 and meses_h12 > 0:
            i_dec = tea_h12 / 100.0
            vp_h12 = vf_h12 / ((1 + i_dec)**(meses_h12 / 12.0))
            st.success(f"• **Valor Presente Exacto (4 Decimales):** **{vp_h12:.4f}** ({fmt_currency(vp_h12)})")

    # ----------------------------------------------------
    # H13
    # ----------------------------------------------------
    elif "XIII. Calculadora Universal" in h_sel:
        st.subheader("XIII. Calculadora Universal de Cuotas e Intereses (4 Decimales)")
        c1, c2, c3 = st.columns(3)
        with c1:
            vp_h13 = smart_num_input("Monto del Préstamo ($):", default_val=0.0, key="h13_vp", is_currency=True)
        with c2:
            tasa_h13 = smart_num_input("Tasa Anual Compuesta (%):", default_val=0.0, key="h13_tasa", is_percent=True)
        with c3:
            n_h13 = smart_num_input("Número de Cuotas Iguales (n):", default_val=0.0, key="h13_n", is_currency=False)
            
        if vp_h13 > 0 and tasa_h13 > 0 and n_h13 > 0:
            i_dec = tasa_h13 / 100.0
            n_int = int(n_h13)
            pmt_h13 = vp_h13 * (i_dec / (1 - (1 + i_dec)**(-n_int)))
            
            st.write(f"• **Cuota Fija Exacta:** **{pmt_h13:.4f}**")
            st.write(f"• **Cuota Formateada (Coma Decimal):** **{fmt_num(pmt_h13)}**")
            st.success(f"• **Cuota Formateada en Pesos:** **{fmt_currency(pmt_h13)}**")

    # ----------------------------------------------------
    # H14
    # ----------------------------------------------------
    elif "XIV. Calculadora de Costo Financiero Total" in h_sel:
        st.subheader("XIV. Calculadora de Costo Financiero Total (CFT) y Comisiones")
        c1, c2, c3 = st.columns(3)
        with c1:
            monto_h14 = smart_num_input("Monto del Préstamo ($):", default_val=0.0, key="h14_monto", is_currency=True)
        with c2:
            tea_h14 = smart_num_input("Tasa Efectiva Anual (TEA %):", default_val=0.0, key="h14_tea", is_percent=True)
        with c3:
            comision_h14 = smart_num_input("Comisión Anual ($):", default_val=0.0, key="h14_com", is_currency=True)
            
        if monto_h14 > 0:
            pct_com = (comision_h14 / monto_h14) * 100.0
            cft_pct = tea_h14 + pct_com
            int_anual = monto_h14 * (tea_h14 / 100.0)
            costo_tot = int_anual + comision_h14
            
            st.metric("Porcentaje de Comisión sobre Crédito", f"{pct_com:.2f}%")
            st.metric("Costo Financiero Total (CFT %)", f"{cft_pct:.2f}%")
            st.metric("Costo Financiero Total en Dinero ($)", fmt_currency(costo_tot))

st.markdown("---")
st.caption("04 Finanzas — Plataforma de Simulación & Ingeniería Financiera")
