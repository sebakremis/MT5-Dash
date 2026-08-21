# MT5-Dash 📈

**MT5-Dash** es un dashboard interactivo desarrollado en Python con [Streamlit](https://streamlit.io/). Su objetivo principal es monitorear el rendimiento del trading en Forex, analizar métricas de riesgo y calcular el tamaño óptimo de nuevas posiciones directamente a partir de los datos de MetaTrader 5 (MT5).

## 🚀 Características Principales (Roadmap)
- **Extracción de Datos Nativos:** Conexión directa con la terminal de MetaTrader 5 utilizando la librería oficial `MetaTrader5` de Python para extraer el historial de operaciones y convertirlos en DataFrames de `pandas`.
- **Cotizaciones en Tiempo Real:** Integración con `forex-python` para obtener los tipos de cambio actuales y calcular con precisión el valor del pip y la exposición.
- **Métricas de Performance y Riesgo:** Visualización de KPIs clave (Win Rate, Profit Factor, Drawdown Máximo, Ratio de Sharpe) y curva de crecimiento de la cuenta.
- **Calculadora de Tamaño de Posición:** Herramienta interactiva para determinar el lotaje exacto de una nueva operación basándose en un porcentaje máximo de riesgo sobre el capital actual y la distancia al Stop Loss.

## 📂 Estructura Tentativa del Proyecto

```text
MT5-Dash/
│
├── data/                   # Directorio para almacenar datos locales o volcados CSV temporales
│
├── src/                    # Código fuente de la aplicación
│   ├── api/                # Scripts para conectar con MT5 y forex-python
│   ├── processing/         # Limpieza, transformación y manejo de DataFrames de pandas
│   ├── metrics/            # Lógica para cálculo de KPIs financieros y de riesgo
│   └── ui/                 # Componentes visuales y layouts de Streamlit
│
├── app.py                  # Archivo principal para ejecutar el dashboard de Streamlit
├── requirements.txt        # Dependencias del proyecto (pandas, streamlit, MetaTrader5, etc.)
├── .gitignore              # Archivos y carpetas ignorados por git (ej. venv, __pycache__)
└── README.md               # Documentación principal del repositorio
```

## 🛠️ Requisitos Previos (Próximamente)
* **Sistema Operativo Windows:** La librería oficial `MetaTrader5` para Python está diseñada para funcionar exclusivamente en entornos Windows.
* **MetaTrader 5:** La terminal de MT5 debe estar instalada, ejecutándose y con una sesión iniciada en tu cuenta de trading.
* **Python 3.9+**

## ⚙️ Instalación Rápida
*Instrucciones detalladas de instalación y despliegue local se añadirán a medida que avance el desarrollo.*

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/tu-usuario/MT5-Dash.git
   ```
2. Crear un entorno virtual:
   ```bash
   python -m venv venv
   ```
3. Instalar las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
4. Ejecutar el dashboard:
   ```bash
   streamlit run app.py
   ```

## 📝 Licencia
Este proyecto es de código abierto.