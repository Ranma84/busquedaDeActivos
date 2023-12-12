"""
1. Evaluación técnica del mercado
2. Señales de alerta del mercado
3. Análisis adicionales que pueda necesitar



Este script de Python es un "screener" o "cribador" de mercado que utiliza datos históricos de precios de acciones para identificar señales técnicas y patrones en diferentes activos financieros. 
El script utiliza la biblioteca investpy para obtener datos de mercado y diversas bibliotecas de análisis técnico (ta) para calcular indicadores como el MACD, RSI y las Bandas de Bollinger.

A continuación, se describen las principales funcionalidades del script:

Definición de Variables:

Se definen varias listas vacías para almacenar los resultados después de que se lanza el screener.
Definición de Funciones:

Se definen varias funciones, cada una diseñada para analizar un aspecto específico de los datos del mercado utilizando indicadores técnicos como MACD, RSI y Bandas de Bollinger.
Las funciones toman un DataFrame que contiene datos de precios y aplican lógica para identificar señales alcistas, bajistas o condiciones específicas del indicador.
Parámetros del Screener:

Se establecen parámetros como el país, el número de días hacia atrás y el número máximo de resultados para el screener.
Se obtiene una lista de resúmenes de acciones utilizando investpy.
Screener Principal:

Se realiza un bucle sobre los símbolos de acciones obtenidos.
Para cada acción, se obtienen los datos históricos y se aplican las funciones de análisis técnico definidas anteriormente.
Se almacenan las acciones que cumplen con ciertos criterios en las listas definidas al principio.
Resultados del Screener:

Al final del script, se imprimen los resultados del screener, mostrando las acciones que cumplen con las diferentes señales técnicas identificadas.
Esencialmente, este script automatiza el análisis técnico de acciones para identificar oportunidades potenciales en el mercado, basándose en señales de indicadores comunes. Las señales incluyen cruces de MACD, 
condiciones de sobrecompra/sobreventa en RSI, y eventos de Bandas de Bollinger. Los resultados se imprimen para que el usuario pueda revisar y tomar decisiones informadas sobre las acciones que podrían ser de interés.

"""

import investpy
import time
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')


# Lista para almacenar variables después de iniciar el evaluador

b_out = []
cons = []
mcd_up = []
mcd_up0 = []
mcd_d = []
mcd_d0 = []
bb_up  = []
already_bb_up = []
bb_d  = []
already_bb_d = []
rsi_d = []
on_rsi_d = []
on_rsi_up = []
rsi_up = []
rsi_bf_d = []
rsi_bf_up = []

# Área de funciones. Cree aquí tantas funciones como sean necesarias para el evaluador. 
# Se muestran algunos ejemplos técnicos básicos (MACD, RSI, BB) y algunas acciones de precios de Consolidación y Ruptura.

