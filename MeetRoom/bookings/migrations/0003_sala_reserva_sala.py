# Generated by Django 5.0.3 on 2024-04-09 02:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0002_remove_reserva_destino_reserva_descripcion_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sala',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('disponible', models.BooleanField(default=True)),
                ('capacidad', models.IntegerField()),
                ('descripcion', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='reserva',
            name='sala',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='reservas', to='bookings.sala'),
            preserve_default=False,
        ),
    ]
