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

def MACD_signal_up(df):
	"""
    Esta Función realiza el SIGNAL UP en el MACD del activo MACD de activos en cruce 
	SIGNAL y cruce de MACD de activos por debajo de 0
	"""	
	from ta.trend import MACD
	indicator_macd = MACD(df['Adj Close'])
	df['MACD'] = indicator_macd.macd()
	df['Signal']= indicator_macd.macd_signal()
	df['MACD Histogram']= indicator_macd.macd_diff()
	df['Below_0_Crossover_MACD_Signal'] = False
	df['Simple_Crossover_MACD_Signal'] = False

	# Lógicas de cruce MACD
	if (df[-2:]['MACD'].values[0] <= df[-1:]['MACD'].values[0]) and (df[-2:]['MACD'].values[0] <= df[-2:]['Signal'].values[0]) and (df[-1:]['MACD'].values[0]>=df[-1:]['Signal'].values[0]):
		

		# Cruce MACD Y por debajo de 0	
		if (df[-2:]['MACD'].values[0] <= df[-1:]['MACD'].values[0]) and (df[-2:]['MACD'].values[0] <= df[-2:]['Signal'].values[0]) and (df[-1:]['MACD'].values[0]>=df[-1:]['Signal'].values[0]) and df[-1:]['MACD'].values[0]<= 0:
			mcd_up0.append(symbol)
			df['Below_0_Crossover_MACD_Signal'][-1] = True
		else:
			mcd_up.append(symbol)
			df['Simple_Crossover_MACD_Signal'][-1] = True
			df['Below_0_Crossover_MACD_Signal'][-1] = False
			return True
	return False

def MACD_signal_down(df):
	"""
    Esta función analizará la SEÑAL ABAJO en el activo MACD
    MACD de activos en Crossunder SIGNAL y MACD de activos Crossunder por encima de 0
	"""	
	from ta.trend import MACD
	indicator_macd = MACD(df['Adj Close'])
	df['MACD'] = indicator_macd.macd()
	df['Signal']= indicator_macd.macd_signal()
	df['MACD Histogram']= indicator_macd.macd_diff()
	df['Simple_Crossdown_MACD_Signal'] = False
	df['Above_0_Crossunder_MACD_Signal'] = False

	#	Cruce MACD
	if (df[-2:]['MACD'].values[0] >= df[-1:]['MACD'].values[0]) and (df[-2:]['MACD'].values[0] >= df[-2:]['Signal'].values[0]) and (df[-1:]['MACD'].values[0]<=df[-1:]['Signal'].values[0]):
		# Cruce de MACD Y por encima de 0	
		if (df[-2:]['MACD'].values[0] >= df[-1:]['MACD'].values[0]) and (df[-2:]['MACD'].values[0] >= df[-2:]['Signal'].values[0]) and (df[-1:]['MACD'].values[0]<=df[-1:]['Signal'].values[0]) and df[-1:]['MACD'].values[0]>= 0:
			mcd_d0.append(symbol)
			df['Above_0_Crossunder_MACD_Signal'][-1] = True
			
		else:
			mcd_d.append(symbol)
			df['Simple_Crossdown_MACD_Signal'][-1] = True
			df['Above_0_Crossunder_MACD_Signal'][-1] = False
			return True
		return False

def Bollinger_signal_up(df, window=20, window_dev=2):
	"""
    Esta función analizará el Bollinger UP del activo.
    Señal de Bollinger Up, activo ya por encima de la banda de Bollinger superior
	"""	

	from ta.volatility import BollingerBands
	indicator_bb = BollingerBands(df["Adj Close"], 20, 2)
	df['bb_bbm'] = indicator_bb.bollinger_mavg()
	df['bb_bbh'] = indicator_bb.bollinger_hband()
	df['bb_bbl'] = indicator_bb.bollinger_lband()
	df['bb_bbhi'] = indicator_bb.bollinger_hband_indicator()
	df['bb_bbli'] = indicator_bb.bollinger_lband_indicator()
	df['Boll_UP'] = False
	df['Boll_UP2']= False

	# Activo en la señal de la banda superior de Bollinger
	if (df[-2:]['bb_bbhi'].values[0] == 0) and (df[-1:]['bb_bbhi'].values[0] == 1):
		df['Boll_UP'][-1] = True
		bb_up.append(symbol)
		return True
	
	# El activo ya está por encima de la banda superior de Bollinger
	elif (df[-2:]['bb_bbhi'].values[0] == 1) and (df[-1:]['bb_bbhi'].values[0] == 1):
		df['Boll_UP2'][-1] = True
		already_bb_up.append(symbol)
		return True
	return False

def Bollinger_signal_down(df, window=20, window_dev=2):
	"""
    Esta función analizará el Bollinger DOWN en el activo.
    Señal de caída de Bollinger, activo ya por debajo de la banda de Bollinger inferior
	"""	

	from ta.volatility import BollingerBands
	indicator_bb = BollingerBands(df["Adj Close"], 20, 2)
	df['bb_bbm'] = indicator_bb.bollinger_mavg()
	df['bb_bbh'] = indicator_bb.bollinger_hband()
	df['bb_bbl'] = indicator_bb.bollinger_lband()
	df['bb_bbhi'] = indicator_bb.bollinger_hband_indicator()
	df['bb_bbli'] = indicator_bb.bollinger_lband_indicator()
	df['Boll_Down'] = False
	df['Boll_Down2']= False

	# Asset on Signal Lower Bollinger Band
	if (df[-2:]['bb_bbli'].values[0] == 0) and (df[-1:]['bb_bbli'].values[0] == 1):	
		bb_d.append(symbol)
		df['Boll_Down'][-1]= True
		return True
	
	# Asset already below lower Bollinger
	elif (df[-2:]['bb_bbli'].values[0] == 1) and (df[-1:]['bb_bbli'].values[0] == 1):
		already_bb_d.append(symbol)	
		df['Boll_Down2'][-1]= True
		return True
	return False

def RSI_signal_up(df, window = 14):
	"""
    Esta función analizará el SIGNAL UP en el activo RSI.
    Señal de sobrecompra, activo ya sobrecomprado y activo que vuelve al rango de sobrecompra
	"""	

	from ta.momentum import RSIIndicator
	indicator_rsi= RSIIndicator(df['Adj Close'], window= 14)
	df['RSI'] = indicator_rsi.rsi()
	df['RSI_Overbought'] = False
	
	# El activo vuelve al rango 70-30 desde Sobrecompra
	if (df[-2:]['RSI'].values[0] >= 70) and (df[-1:]['RSI'].values[0] <= 70):
		rsi_bf_up.append(symbol)

	# Activo con RSI > 70		
	if (df[-1:]['RSI'].values[0] >= 70):
		on_rsi_up.append(symbol)
		df['RSI_Overbought'][-1] = True
		
		# SEÑAL de sobrecompra RSI	
		if (df[-2:]['RSI'].values[0] <= 70) and (df[-1:]['RSI'].values[0] >= 70):
			rsi_up.append(symbol)
			return True
	return False

def RSI_signal_down(df, window= 14):
	"""
    Esta función analizará la SEÑAL ABAJO en el activo RSI
    Señal de sobreventa, activo ya sobrevendido y activo que vuelve a estar en el rango de sobrevendido
	"""	

	from ta.momentum import RSIIndicator
	indicator_rsi= RSIIndicator(df['Adj Close'], window= 14)
	df['RSI'] = indicator_rsi.rsi()
	df['RSI_Oversold'] = False
	
	# El activo vuelve al rango 30-70 desde sobrevendido
	if (df[-2:]['RSI'].values[0] <= 30) and (df[-1:]['RSI'].values[0] >= 30):
		rsi_bf_d.append(symbol)

	# Activo en RSI <30
	if (df[-1:]['RSI'].values[0] <= 30):
		on_rsi_d.append(symbol)
		df['RSI_Oversold'][-1] = True
		
		# RSI acaba de cruzar hacia abajo SEÑAL
		if (df[-2:]['RSI'].values[0] >= 30) and (df[-1:]['RSI'].values[0] <= 30):
			rsi_d.append(symbol)
			return True
	return False

def consolidating_signal(df, perc = 3.5):
	"""
    Esta función analizará si el activo se está consolidando dentro del rango de perc.
    Ej: perc = 3,5 significa que el precio de cierre en las últimas 15 sesiones no ha cambiado
    más del 3,5%
	"""	
	range_of_candlesticks= df[-15:]
	max_close_price = range_of_candlesticks['Adj Close'].max()
	min_close_price = range_of_candlesticks['Adj Close'].min()
	threshold_detection = 1 - (perc / 100)
	if min_close_price > (max_close_price * threshold_detection):
		cons.append(symbol)
		return True
	return False

def breaking_out_signal(df, perc=1,):
	"""
    Esta función analizará un activo que sale de una consolidación.
    período.

    [perc] = será el umbral en % para que el precio de cierre determine si el activo es
    en proceso de consolidación.

    En el ejemplo perc = 1, el activo cerrará dentro del rango del 1% en las últimas 15 sesiones y luego
    en la vela actual está estallando.
	
	"""	
	last_close = df[-1:]['Adj Close'].values[0]
	if consolidating_signal(df[:-1], perc = perc):
		recent_close = df[-16:-1]
		if last_close > recent_close['Adj Close'].max():
			b_out.append(symbol)
			return True
	return False


# Se deben cambiar los parámetros del filtro (país, días_atrás y n_resultados) según los indicadores y el mercado.

country ='Argentina'
days_back = 120
today = datetime.now()
start = today -timedelta(days_back)
today = datetime.strftime(today, '%d/%m/%Y')
start = datetime.strftime(start, '%d/%m/%Y')
stocks = investpy.get_stocks_overview(country, n_results=1000)
stocks = stocks.drop_duplicates(subset='symbol')

# Dates
today = datetime.now()
start = today -timedelta(days_back)
today = datetime.strftime(today, '%d/%m/%Y')
start = datetime.strftime(start, '%d/%m/%Y')

# Se agrega la variable de recuento de lanzamientos del analizador al límite del bucle while si es necesario para controlar las llamadas/solicitudes API-HTTP.
# Descomente el while y aplique sangría si es necesario.

count = 0
for symbol in stocks['symbol']:
    try:
        df = investpy.get_stock_historical_data(stock=symbol,country=country,from_date=f'{start}', to_date=f'{today}')
        time.sleep(0.25)
        df= df.rename(columns={"Close": "Adj Close"})
        if breaking_out_signal(df, 3):
            pass		
        if consolidating_signal(df, perc=2):
            pass
        if RSI_signal_up(df):
            pass
        if RSI_signal_down(df):
            pass
        if MACD_signal_up(df):
            pass
        if MACD_signal_down(df):
            pass
        if Bollinger_signal_up(df):
            pass
        if Bollinger_signal_down(df):
            pass
        
    except Exception as e:
        print(f'No data on {symbol}')
        print(e)


# SALIDA => Para el ejemplo, solo una impresión, pero tiene los tickers almacenados en las variables para realizar un análisis más detallado.


print(f'--------- GENERAL MARKET SCREENER in {country} for {len(stocks)} assets: data analyzed from {start} until {today} --------\n')
print('--- BOLLINGER ANALYSIS --- \n')
print(f'The stocks on SIGNAL BOLLINGER UP are:\n==> {bb_up}\n')
print(f'The stocks are already in BOLLINGER UP:\n==> {already_bb_up}\n')
print(f'The stocks on SIGNAL BOLLINGER DOWN are:\n==> {bb_d}\n')
print(f'The stocks are already in BOLLINGER_DOWN:\n==> {already_bb_d}\n')
print('--- MACD ANALYSIS --- \n')
print(f'The stocks on MACD SIGNAL UP are:\n==> {mcd_up}\n')
print(f'The stocks on MACD SIGNAL UP BELOW 0 are:\n==> {mcd_up0}\n')
print(f'The stocks on MACD SIGNAL DOWN are:\n==> {mcd_d} \n')
print(f'The stocks on MACD SIGNAL DOWN above 0 are:\n==> {mcd_d0}\n')
print('--- RSI ANALYSIS --- \n')
print(f'The stocks on OVERBOUGHT SIGNAL [RSI] are:\n==> {rsi_up}\n')
print(f'The stocks on OVERSOLD SIGNAL [RSI] are:\n==> {rsi_d}\n')
print(f'The stocks went to RANGE from OVERSOLD are:\n==> {rsi_bf_d}\n')
print(f'The stocks went to RANGE from OVERBOUGHT are:\n==> {rsi_bf_up}\n')
print(f'The stocks on OVERBOUGHT [RSI] are:\n==> {on_rsi_up}\n')
print(f'The stocks on OVERSOLD [RSI] are:\n==> {on_rsi_d}\n')
print('--- PRICE ACTION ANALYSIS --- \n')
print(f'The stocks on CONSOLIDATION are:\n==> {cons}\n')
print(f'The stocks on BREAKOUT are:\n==> {b_out}\n')