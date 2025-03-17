import base64
import io

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests_cache
import seaborn as sns
from numpy.polynomial.polynomial import Polynomial
from openmeteo_requests import Client
from scipy.stats import weibull_min
from windrose import WindroseAxes


def codificar_img_base(image_data):
    return base64.b64encode(image_data).decode('utf-8')


def wind_analysis(lat, lon, start_date, end_date):
    def retry(session, retries=5, backoff_factor=0.2):
        from requests.adapters import HTTPAdapter
        from urllib3.util.retry import Retry
        retry_strategy = Retry(
            total=retries,
            backoff_factor=backoff_factor,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        return session

    
    cache_session = requests_cache.CachedSession('.cache', expire_after=-1)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = Client(session=retry_session)

    
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": start_date,
        "end_date": end_date,
        "hourly": ["wind_speed_10m", "wind_speed_100m", "wind_direction_10m", "wind_direction_100m"]
    }

    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]

    response_dict = {
            "Latitude": response.Latitude(),
            "Longitude": response.Longitude(),
            "Elevation": response.Elevation(),
            "Timezone": response.Timezone(),
            "TimezoneAbbreviation": response.TimezoneAbbreviation(),
            "UtcOffsetSeconds": response.UtcOffsetSeconds(),
        }
    
    hourly = response.Hourly()
    hourly_data = {
        "date": pd.date_range(
            start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
            end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=hourly.Interval()),
            inclusive="left"
        ),
        "wind_speed_10m": hourly.Variables(0).ValuesAsNumpy(),
        "wind_speed_100m": hourly.Variables(1).ValuesAsNumpy(),
        "wind_direction_10m": hourly.Variables(2).ValuesAsNumpy(),
        "wind_direction_100m": hourly.Variables(3).ValuesAsNumpy()
    }

    
    hourly_dataframe = pd.DataFrame(data=hourly_data)

    def calculate_air_density(altitude):
        
        rho_0 = 1.225  # sea level standard air density in kg/m^3
        L = 0.0065  # standard temperature lapse rate in K/m
        T_0 = 288.15  # sea level standard temperature in K
        g = 9.80665  # acceleration due to gravity in m/s^2
        R = 287.058  # ideal gas constant for air in J/(kg·K)

        # Air density calculation
        rho = rho_0 * (1 - (L * altitude / T_0)) ** ((g / (R * L)) - 1)
        return rho


    altitude = response_dict['Elevation'] 
    air_density = calculate_air_density(altitude)

    
    plt.figure(figsize=(14, 7))
    plt.plot(hourly_dataframe['date'], hourly_dataframe['wind_speed_10m'], label='Velocidad del viento a 10m')
    plt.title('Series Temporales de Velocidad del Viento')
    plt.xlabel('Fecha')
    plt.ylabel('Velocidad del Viento (m/s)')
    plt.legend()

    # Guardar la gráfica en memoria como PNG
    wind_speed_timeseries_bytes = io.BytesIO() 
    plt.savefig(wind_speed_timeseries_bytes, format='png', bbox_inches='tight')  # Guardar como PNG
    plt.close()  
    wind_speed_timeseries_bytes.seek(0) 



    plt.figure(figsize=(14, 7))
    # Graficar las distribuciones usando seaborn
    sns.histplot(hourly_dataframe['wind_speed_10m'], kde=True, color='blue', label='Velocidad del viento a 10m', bins=30)
    sns.histplot(hourly_dataframe['wind_speed_100m'], kde=True, color='red', label='Velocidad del viento a 100m', bins=30)
    plt.title('Distribuciones de Velocidad del Viento')
    plt.xlabel('Velocidad del Viento (m/s)')
    plt.ylabel('Frecuencia')
    plt.legend()

    # Guardar la gráfica en memoria como PNG
    wind_speed_distribution = io.BytesIO()
    plt.savefig(wind_speed_distribution, format='png', bbox_inches='tight')  # Guardar como PNG
    plt.close()  
    wind_speed_distribution.seek(0)  



    # Distribución Acumulada de Velocidad del Viento -----------------------------------------------------------------
    
    plt.figure(figsize=(8, 4))
    sns.ecdfplot(hourly_dataframe['wind_speed_10m'], color='blue', label='Velocidad del viento a 10m')
    sns.ecdfplot(hourly_dataframe['wind_speed_100m'], color='red', label='Velocidad del viento a 100m')
    plt.title('Distribuciones Acumuladas de Velocidad del Viento')
    plt.xlabel('Velocidad del Viento (m/s)',fontsize=12)
    plt.ylabel('Probabilidad Acumulada',fontsize=12)
    plt.xlim(0,40 )

    plt.legend()
    wind_distribucion_acomulada = io.BytesIO()
    plt.savefig(wind_distribucion_acomulada, format='png', bbox_inches='tight')  # Guardar como PNG
    plt.close() 
    wind_distribucion_acomulada.seek(0)  

    # Rosetas de Viento para las Direcciones del Viento -------------------------------------------------------

    plt.figure(figsize=(1, 1))
    ax = WindroseAxes.from_ax()
    ax.bar(hourly_dataframe['wind_direction_10m'], hourly_dataframe['wind_speed_10m'], normed=True, opening=0.8, edgecolor='white')
    ax.set_title('Roseta de Viento a 10m',fontsize=25)
    ax.set_legend()
    wind_rose_10m = io.BytesIO()
    plt.savefig(wind_rose_10m, format='png', bbox_inches='tight')  
    plt.close()  
    wind_rose_10m.seek(0)  

    # Crear la roseta de viento para la dirección del viento a 100m
    plt.figure(figsize=(4, 4))
    ax = WindroseAxes.from_ax()
    ax.bar(hourly_dataframe['wind_direction_100m'], hourly_dataframe['wind_speed_100m'], normed=True, opening=0.8, edgecolor='white')
    ax.set_title('Roseta de Viento a 100m' ,fontsize=12)
    ax.set_legend()
    wind_rose_100m = io.BytesIO()
    plt.savefig(wind_rose_100m, format='png', bbox_inches='tight')  # Guardar como PNG
    plt.close()  
    wind_rose_100m.seek(0)  

    # Cálculo de la curva de Weibull------------------------------------------
        
    params_10m = weibull_min.fit(hourly_dataframe['wind_speed_10m'], floc=0)
    params_100m = weibull_min.fit(hourly_dataframe['wind_speed_100m'], floc=0)
    shape_10m, loc_10m, scale_10m = params_10m
    shape_100m, loc_100m, scale_100m = params_100m
   
    # Generar una gama de velocidades de viento para la curva de Weibull
    wind_speeds = np.linspace(0, max(hourly_dataframe['wind_speed_10m'].max(), hourly_dataframe['wind_speed_100m'].max()), 100)
   
    # Calcular la densidad de probabilidad de Weibull para las velocidades de viento
    weibull_pdf_10m = weibull_min.pdf(wind_speeds, shape_10m, loc_10m, scale_10m)
    weibull_pdf_100m = weibull_min.pdf(wind_speeds, shape_100m, loc_100m, scale_100m)
   
    # Graficar la curva de Weibull
    plt.figure(figsize=(10, 4))
    plt.plot(wind_speeds, weibull_pdf_10m, label='Weibull (10m)', color='blue')
    plt.plot(wind_speeds, weibull_pdf_100m, label='Weibull (100m)', color='red')
    plt.hist(hourly_dataframe['wind_speed_10m'], bins=30, density=True, alpha=0.5, color='blue', label='Histograma (10m)')
    plt.hist(hourly_dataframe['wind_speed_100m'], bins=30, density=True, alpha=0.5, color='red', label='Histograma (100m)')
    plt.title('Distribución de Weibull de la Velocidad del Viento')
    plt.xlabel('Velocidad del Viento (m/s)',fontsize=12)
    plt.ylabel('Densidad de Probabilidad',fontsize=12)
    plt.ylim(0, 0.2)
    plt.xlim(0,40 )
    plt.legend()
    

    Weibull_curves = io.BytesIO()
    plt.savefig(Weibull_curves, format='png', bbox_inches='tight')  
    plt.close()  
    Weibull_curves.seek(0)  
    
    R = 10  
    h = 20  
    alpha = 0.143
    shape_hm = (shape_10m + shape_100m) / 2
    scale_hm = ((scale_10m * (h / 10)**alpha) + (scale_100m * (h / 100)**alpha)) / 2
    wind_speeds = np.linspace(0, max(hourly_dataframe['wind_speed_10m'].max(), hourly_dataframe['wind_speed_100m'].max()), 100)

    # Calcular la densidad de probabilidad de Weibull para las velocidades de viento a hm
    weibull_pdf_hm = weibull_min.pdf(wind_speeds, shape_hm, loc=0, scale=scale_hm)
    
    # Gráfica de la curva de Weibull a hm
    plt.figure(figsize=(14, 7))
    plt.plot(wind_speeds, weibull_pdf_hm, label=f'Weibull ({h} m)', color='green')
    plt.hist(hourly_dataframe['wind_speed_10m'], bins=30, density=True, alpha=0.5, color='blue', label='Histograma (10m)')
    plt.hist(hourly_dataframe['wind_speed_100m'], bins=30, density=True, alpha=0.5, color='red', label='Histograma (100m)')
    plt.title(f'Distribución de Weibull de la Velocidad del Viento a {h} m')
    plt.xlabel('Velocidad del Viento (m/s)')
    plt.ylabel('Densidad de Probabilidad')
    plt.legend()
    parametrosWeibull = (shape_hm, scale_hm)
    weibull_distribution = io.BytesIO()
    plt.savefig(weibull_distribution, format='png', bbox_inches='tight')  
    plt.close()  
    weibull_distribution.seek(0)  

    # Ajuste de curva de eficiencia del Aerogenerador ---------------------------------------------------
    
    lambda_values = np.array([0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0])
    cp_values = np.array([0.0, 0.15, 0.3, 0.45, 0.52, 0.55, 0.53, 0.5, 0.4, 0.3, 0.1])
    p = Polynomial.fit(lambda_values, cp_values, 4)
    
    coefficients = p.convert().coef
    lambda_fit = np.linspace(0, 2, 100)
    cp_fit = p(lambda_fit)

    plt.scatter(lambda_values, cp_values, label='Datos Originales')
    plt.plot(lambda_fit, cp_fit, label='Curva Ajustada', color='red')
    plt.xlabel('λ')
    plt.ylabel('Cp')
    plt.title('Ajuste de Curva de Eficiencia del Aerogenerador')
    plt.legend()
    eficiencia_aerogenerador = io.BytesIO()
    plt.savefig(eficiencia_aerogenerador, format='png', bbox_inches='tight')  
    plt.close()  
    eficiencia_aerogenerador.seek(0)  


    # Potencia vs Velocidad del Viento ---------------------------------------------------------------
    
    v_wind = np.linspace(1, 25, 50)  
    Omega_min = 0 
    Omega_max = 40 * 2 * np.pi / 60  
    Omega_values = np.linspace(Omega_min, Omega_max, len(v_wind))
    lambda_values =  (Omega_values * R) /v_wind
    cp_values = p(lambda_values)

    plt.figure(figsize=(10, 6))
    plt.plot(v_wind, cp_values, label='Cp vs Velocidad del Viento')
    plt.xlabel('Velocidad del Viento (m/s)')
    plt.ylabel('Cp')
    plt.title('Coeficiente de Potencia (Cp) vs Velocidad del Viento')
    plt.legend()
    plt.grid(True)
    
    potencia_viento = io.BytesIO()
    plt.savefig(potencia_viento, format='png', bbox_inches='tight')  
    plt.close()  
    potencia_viento.seek(0)  
  


    # Función para calcular la potencia eólica disponible --------------------------------------------
    def power_available(v, air_density, R):
        return 0.5 * air_density * np.pi * R**2 * v**3
   
    # Función para calcular la potencia generada por la turbina
    def power_generated(v, air_density, R, Omega, p):
        lambda_value = Omega * R / v
        cp = p(lambda_value)
        return power_available(v, air_density, R) * cp
   
    # Calcular la densidad de potencia eólica para cada velocidad del viento
    Omega = 400 * 2 * np.pi / 60
    power_densities = [power_generated(v, air_density, R, Omega , p) for v in wind_speeds]
    
    # Graficar la densidad de potencia eólica vs velocidad del viento
    plt.figure(figsize=(10, 6))
    plt.plot(wind_speeds,power_densities*weibull_pdf_hm, label='Potencia Eólica')
    plt.xlabel('Velocidad del Viento (m/s)')
    plt.ylabel('Potencia (W)')
    plt.title('Potencia Eólica vs Velocidad del Viento')
    plt.legend()
    plt.grid(True)
    windturbine_power = io.BytesIO()
    plt.savefig(windturbine_power, format='png', bbox_inches='tight') 
    plt.close()  
    windturbine_power.seek(0)  


    # Potencia acumulada de la turbina vs la velocidad del  viento --------------------------------
    cumulative_power = np.array([
        np.trapz(np.nan_to_num(power_densities[:i+1] * weibull_pdf_hm[:i+1]), wind_speeds[:i+1])
        for i in range(len(wind_speeds))
    ])

    plt.figure(figsize=(10, 6))
    plt.plot(wind_speeds, cumulative_power, label='Potencia Acumulada')
    plt.xlabel('Velocidad del Viento (m/s)')
    plt.ylabel('Potencia Acumulada (W)')
    plt.title('Potencia Acumulada de la Turbina vs Velocidad del Viento')
    plt.legend()
    plt.grid(True)
    
    potencia_maxima = np.max(np.nan_to_num(power_densities*weibull_pdf_hm))
    potencia_promedio = np.mean(np.nan_to_num(power_densities*weibull_pdf_hm))
    windturbine_power_cumulative = io.BytesIO()
    plt.savefig(windturbine_power_cumulative, format='png', bbox_inches='tight')  
    plt.close()  
    windturbine_power_cumulative.seek(0)  

    params_10m_list = list(params_10m)
    params_100m_list = list(params_100m)
    parametrosWeibull_list = list(parametrosWeibull)
    coefficients_list = coefficients.tolist()
    return {
        'datos': {
            'Elevation':response.Elevation(),
            'air_density': air_density
        },
        'Series Temporales': wind_speed_timeseries_bytes,
        'Distribucion Velocidad':wind_speed_distribution,
        'Distribucion Acumulada': wind_distribucion_acomulada,
        'Roseta 10m':wind_rose_10m, 
        'Roseta 100m':wind_rose_100m, 
        'Curva Weibull': {
            'Grafica': Weibull_curves ,
            'Parametros 10m':  params_10m_list,
            'Parametros 100m':  params_100m_list,
        } ,
        'Distribucion Weibull':{
            'Grafica': weibull_distribution,
            'Parametros': parametrosWeibull_list
        },
        'Eficiencia Generador':{
            'Grafica': eficiencia_aerogenerador,
            'Coeficientes':coefficients_list
        },
        'Potencia Viento': potencia_viento,
        'Potencia Turbina':windturbine_power,
        'Potencia Acumulada':{
            'Grafica': windturbine_power_cumulative,
            'Max':potencia_maxima,
            'Promedio':potencia_promedio,
        }
    }

