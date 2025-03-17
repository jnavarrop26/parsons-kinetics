from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt

from .calculos import codificar_img_base, wind_analysis
from .forms import CrearConsultaForm
from .models import Consulta


def index(request):
    return render(request,'index.html')

def formulario(request):
    return render(request,'formulario.html')

def lista_estimaciones(request):
    consultas = Consulta.objects.all()
    for consulta in consultas:
        if consulta.wind_speed_timeseries:
            consulta.wind_speed_timeseries_base64 = codificar_img_base(consulta.wind_speed_timeseries)
        if consulta.wind_speed_distribution:
            consulta.wind_speed_distribution_base64 = codificar_img_base(consulta.wind_speed_distribution)
        if consulta.wind_distribucion_acumulada:
            consulta.wind_distribucion_acumulada_base64 = codificar_img_base(consulta.wind_distribucion_acumulada)
        if consulta.wind_rose_10m:
            consulta.wind_rose_10m_base64 = codificar_img_base(consulta.wind_rose_10m)
        if consulta.wind_rose_100m:
            consulta.wind_rose_100m_base64 = codificar_img_base(consulta.wind_rose_100m)
        if consulta.weibull_curves:
            consulta.weibull_curves_base64 = codificar_img_base(consulta.weibull_curves)
        if consulta.weibull_distribution:
            consulta.weibull_distribution_base64 = codificar_img_base(consulta.weibull_distribution)
        if consulta.eficiencia_generador:
            consulta.eficiencia_generador_base64 = codificar_img_base(consulta.eficiencia_generador)
        if consulta.potencia_viento:
            consulta.potencia_viento_base64 = codificar_img_base(consulta.potencia_viento)
        if consulta.potencia_turbina:
            consulta.potencia_turbina_base64 = codificar_img_base(consulta.potencia_turbina)
        if consulta.potencia_acumulada:
            consulta.potencia_acumulada_base64 = codificar_img_base(consulta.potencia_acumulada)
    return render(request,'lista_estimaciones.html',{
        'consultas':consultas
    })


def consulta(request):
    if request.method == 'POST':  
        form = CrearConsultaForm(request.POST)  
        if form.is_valid():  
            consulta_obj = form.save()

            try:
                # Llamar a la función wind_analysis con los datos del formulario
                resultados = wind_analysis(
                    lat=consulta_obj.lat,
                    lon=consulta_obj.lon,
                    start_date=consulta_obj.start_date,
                    end_date=consulta_obj.end_date
                )

                
                consulta_obj.elevation = resultados['datos']['Elevation']
                consulta_obj.air_density = resultados['datos']['air_density']

                # Gráficas en formato binario
                consulta_obj.wind_speed_timeseries = resultados['Series Temporales'].getvalue()
                consulta_obj.wind_speed_distribution = resultados['Distribucion Velocidad'].getvalue()
                consulta_obj.wind_distribucion_acumulada = resultados['Distribucion Acumulada'].getvalue()
                consulta_obj.wind_rose_10m = resultados['Roseta 10m'].getvalue()
                consulta_obj.wind_rose_100m = resultados['Roseta 100m'].getvalue()
                consulta_obj.weibull_curves = resultados['Curva Weibull']['Grafica'].getvalue()
                consulta_obj.weibull_distribution = resultados['Distribucion Weibull']['Grafica'].getvalue()
                consulta_obj.eficiencia_generador = resultados['Eficiencia Generador']['Grafica'].getvalue()
                consulta_obj.potencia_viento = resultados['Potencia Viento'].getvalue()
                consulta_obj.potencia_turbina = resultados['Potencia Turbina'].getvalue()
                consulta_obj.potencia_acumulada = resultados['Potencia Acumulada']['Grafica'].getvalue()

                # Parámetros y coeficientes
                consulta_obj.weibull_params_10m = resultados['Curva Weibull']['Parametros 10m']
                consulta_obj.weibull_params_100m = resultados['Curva Weibull']['Parametros 100m']
                consulta_obj.weibull_params_hm = resultados['Distribucion Weibull']['Parametros']
                consulta_obj.eficiencia_coefficients = resultados['Eficiencia Generador']['Coeficientes']

                # Potencia acumulada
                consulta_obj.potencia_max = resultados['Potencia Acumulada']['Max']
                consulta_obj.potencia_promedio = resultados['Potencia Acumulada']['Promedio']

                # Guardar los resultados adicionales en la base de datos
                consulta_obj.save()

                # Redirigir al índice tras éxito
                return redirect('index')

            except Exception as e:
                # Manejar errores de la función wind_analysis
                form.add_error(None, f"Error al procesar el análisis: {str(e)}")
                consulta_obj.delete()  

    else:  
        form = CrearConsultaForm()  

    return render(request, 'formulario.html', {'form': form})



def eliminar_consulta(request, consulta_id):
    try:
        consulta = Consulta.objects.get(id=consulta_id)
    except Consulta.DoesNotExist:
        raise Http404("Consulta no encontrada")
    consulta.delete()
    
    return redirect('lista')  
