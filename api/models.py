from django.db import models



class Consulta(models.Model):
    name = models.CharField(max_length=200)  
    lat = models.DecimalField(max_digits=10, decimal_places=7)  
    lon = models.DecimalField(max_digits=11, decimal_places=7)  
    start_date = models.DateField()  
    end_date = models.DateField() 
    created_at = models.DateTimeField(auto_now_add=True)  
    elevation = models.FloatField(null=True, blank=True)  
    air_density = models.FloatField(null=True, blank=True)  
    wind_speed_timeseries = models.BinaryField(null=True, blank=True) 
    wind_speed_distribution = models.BinaryField(null=True, blank=True)  
    wind_distribucion_acumulada = models.BinaryField(null=True, blank=True)  
    wind_rose_10m = models.BinaryField(null=True, blank=True)  
    wind_rose_100m = models.BinaryField(null=True, blank=True)  
    weibull_curves = models.BinaryField(null=True, blank=True)  
    weibull_distribution = models.BinaryField(null=True, blank=True)  
    eficiencia_generador = models.BinaryField(null=True, blank=True) 
    potencia_viento = models.BinaryField(null=True, blank=True)  
    potencia_turbina = models.BinaryField(null=True, blank=True)  
    potencia_acumulada = models.BinaryField(null=True, blank=True) 
    weibull_params_10m = models.JSONField(null=True, blank=True)  
    weibull_params_100m = models.JSONField(null=True, blank=True)  
    weibull_params_hm = models.JSONField(null=True, blank=True)  
    eficiencia_coefficients = models.JSONField(null=True, blank=True)  
    potencia_max = models.FloatField(null=True, blank=True)  

    def __str__(self):
        return f"{self.name} ({self.lat}, {self.lon})"
