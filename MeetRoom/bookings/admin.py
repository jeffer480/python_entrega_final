from django.contrib import admin
from .models import Reserva, Sala, Comentario

# Register your models here.
admin.site.register(Reserva)
admin.site.register(Sala)
admin.site.register(Comentario)
