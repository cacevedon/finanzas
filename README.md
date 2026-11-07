# 📊 Plataforma Interactiva de Finanzas & Solucionario — 04 Finanzas

Bienvenido al repositorio oficial de la **Plataforma de Simulación y Solucionario Integral de Finanzas** para la asignatura **04 Finanzas**. Esta herramienta está desarrollada en **Python** utilizando **Streamlit**, **Pandas**, **NumPy-Financial** y **Matplotlib**, ofreciendo una interfaz gráfica ágil e intuitiva para explorar la teoría, resolver ejercicios y simular escenarios económicos en tiempo real [1, 2].

---

## 🚀 Demo e Interfaz Web

La aplicación permite navegar dinámicamente a través de los **8 módulos clave** del curso:

1. **Unidad 1: Fundamentos y Decisiones Financieras**  
   * Conceptos clave sobre el **Valor del Dinero en el Tiempo (VDT)** [3], costo de oportunidad y compensación riesgo-liquidez [4].
   * Análisis cualitativo y matriz de recomendación para los 4 casos prácticos (Lucía, Carlos, Presupuesto e imprevisto médico del 15%, y Pyme Rápido) [4].
   * Mapa interactivo de intermediarios e instituciones del sistema financiero [3].

2. **Unidad 2: Interés Simple e Interés Compuesto**  
   * Calculadora dinámica para evaluar Capital Inicial (\\(VP\\)), Valor Futuro (\\(VF\\)), Tasa (\\(i\\)) y Tiempo (\\(n\\)) [5].
   * Comparativa visual en tiempo real entre crecimiento lineal (\\(I = VP \cdot i \cdot n\\)) [6] y exponencial (\\(VF = VP(1+i)^n\\)) [7, 8].
   * Solucionario completo de los 10 ejercicios del Taller Formativo [2] y el caso práctico del matrimonio (\\(S/ 25.000.000\\)).

3. **Unidad 3: Conversión de Tasas (TNA a TEA)**  
   * Conversor dinámico entre Tasa Nominal Anual (TNA) y Tasa Efectiva Anual (TEA) según la frecuencia de capitalización (\\(m\\)) [9, 10].
   * Matriz comparativa para decidir entre alternativas bancarias (ej. Banco X al 9% nominal trimestral vs. Banco Y al 9,2% TEA) [11].

4. **Unidad 4: Anualidades & Tablas de Amortización**  
   * Cálculo de cuota periódica (\\(R\\)) para anualidades ordinarias, anticipadas y diferidas [12, 13].
   * Generador de **tablas de amortización mensuales** (hasta 60 meses) con desglose dinámico de amortización de capital e intereses.
   * Gráfico de barras apiladas que ilustra la composición del pago a lo largo del tiempo.

5. **Unidad 5: Gradientes Financieros**  
   * Comparador gráfico a 10 años entre series constantes, gradientes aritméticos (\\(+G\\)) y gradientes geométricos (\\(+g\\)) [14, 15].
   * Solución paso a paso del proyecto de la planta de desalinización (\$5M diferido 4 años al 12% TMAR) [16].

6. **Unidad 6: Presupuestos y Control de Caja**  
   * Simulador de presupuesto operacional a 12 meses (*Rolling Forecast*) ajustado por **tasa de crecimiento de ventas** e **inflación de costos**.
   * Gráficos dinámicos de flujo de caja neto y acumulación de fondo de reserva de liquidez.

7. **Unidad 7: Evaluación de Proyectos (VAN / TIR / Punto de Equilibrio)**  
   * Calculadora de punto de equilibrio operacional (\\(Q = \frac{CF}{P - CV}\\)) [17].
   * Simulador de proyectos de inversión con métricas automáticas de **Valor Actual Neto (VAN)**, **Tasa Interna de Retorno (TIR)** e **Índice de Rentabilidad** [17].
   * Matriz de sensibilidad bidimensional (2D) cruzando variaciones de TMAR vs. Flujos de caja.

8. **Unidad 8: Banco de Preguntas y Solemnes**  
   * Solucionario guiado paso a paso con respuestas verificadas para las 16 preguntas objetivas y numéricas extraídas de los exámenes del curso.

---

## 🛠️ Tecnologías Utilizadas

* **Python 3.12**
* **Streamlit** (Frontend y Dashboard interactivo)
* **Pandas & NumPy** (Procesamiento de datos y vectores)
* **NumPy-Financial** (Funciones financieras estandarizadas: `npf.pmt`, `npf.npv`, `npf.irr`)
* **Matplotlib** (Visualización gráfica de datos)
* **OpenPyXL** (Generación y auditoría de libros de trabajo en Excel)

---

## 📦 Estructura del Repositorio

```text
├── solucionario_finanzas_streamlit.py  # Código principal de la Web App en Streamlit
├── solucionario_finanzas_app.py        # Versión de escritorio basada en Tkinter
├── solucionario_finanzas_completo-v7.xlsx # Modelo completo en Excel con gráficos y fórmulas
├── requirements.txt                    # Dependencias de librerías Python
└── README.md                           # Documentación del proyecto
