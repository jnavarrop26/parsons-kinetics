# Generated by Django 5.1.3 on 2024-11-18 08:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Consulta',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('lat', models.FloatField()),
                ('lon', models.FloatField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='GraficasConsulta',
            fields=[
                ('consulta', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='api.consulta')),
                ('serie_temporal', models.ImageField(upload_to='charts/')),
                ('dist_vel_viento', models.ImageField(upload_to='charts/')),
                ('dist_acum_viento', models.ImageField(upload_to='charts/')),
                ('rosetas_viento', models.ImageField(upload_to='charts/')),
                ('curva_weibull', models.ImageField(upload_to='charts/')),
                ('dist_weibull', models.ImageField(upload_to='charts/')),
                ('curva_eficiencia', models.ImageField(upload_to='charts/')),
                ('coeficiente_cp', models.ImageField(upload_to='charts/')),
                ('potencia_eolica', models.ImageField(upload_to='charts/')),
            ],
        ),
    ]
