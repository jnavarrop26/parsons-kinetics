from django import forms
from .models import Consulta

class CrearConsultaForm(forms.ModelForm):
    class Meta:
        model = Consulta
        fields = ['name', 'lat', 'lon', 'start_date', 'end_date']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Ejemplo: Quibdó',
                'class': 'form-control',
            }),
            'lat': forms.NumberInput(attrs={
                'placeholder': 'Ejemplo: 5.6918832',
                'class': 'form-control',
                'step': '0.0000001',  # Permite hasta 7 decimales
            }),
            'lon': forms.NumberInput(attrs={
                'placeholder': 'Ejemplo: -76.6583512',
                'class': 'form-control',
                'step': '0.0000001',  # Permite hasta 7 decimales
            }),
            'start_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
            }),
            'end_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
            }),
        }

    # Validación personalizada para latitud
    def clean_lat(self):
        lat = self.cleaned_data.get('lat')
        if lat is not None and not (-90 <= lat <= 90):
            raise forms.ValidationError('La latitud debe estar entre -90 y 90.')
        return lat

    # Validación personalizada para longitud
    def clean_lon(self):
        lon = self.cleaned_data.get('lon')
        if lon is not None and not (-180 <= lon <= 180):
            raise forms.ValidationError('La longitud debe estar entre -180 y 180.')
        return lon