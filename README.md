Python_entrega_final
Autor: Jefferson Varela F
Curso python

# Entrega Final
### alumno: jeffersonvarela480@gmail.com

# Comandos

1. Crear proyecto Django
    ```bash
    django-admin startproject <nombre del proyecto que quieran ustedes>
    ```
    en este tutorial utilizaremos como ejemplo:
    ```bash
    django-admin startproject MeetingRooms
    ```

    Si el comando anterior falla, se puede utilizar:

    ```bash
    python -m django startproject nombre_del_proyecto
    # o
    python3 -m django startproject nombre_del_proyecto
    ```
2. Testear servidor
    ```bash
    python manage.py runserver
    ```
3. Crear una `application` dentro de mi proyecto:
    ```bash
    python manage.py startapp <nombre de su aplicacion>
    ```
    en el caso de este tutorial sería `bookings`:
    ```bash
    python manage.py startapp bookings
    ```
4. Creamos un archivo que se llame `urls.py` en `<nombre_del_proyecto>/<nombre_de_su_aplicacion>/urls.py`. En mi caso sería: `MeetingRooms/bookings/urls.py`


## Templates

1. Los templates son archivos con extensión `.html` que se deben guardar dentro de una carpeta llamada `templates` dentro de la carpeta de cada aplicación.

    En este tutorial: [clase-19/MeetingRooms/bookings/templates](clase-19/MeetingRooms/bookings/templates)

2. Para utilizarlo en alguna vista se recomienda utilizar la función `render`.

   Por ejemplo, si tenemos un template llamado `home.html` guardado en

   [clase-19/MeetingRooms/bookings/templates/bookings/home.html](clase-19/MeetingRooms/bookings/templates/bookings/home.html),

   lo utilizamos desde

   [clase-19/MeetingRooms/bookings/views.py](clase-19/MeetingRooms/bookings/views.py)
   ```python
    from django.shortcuts import render
    from django.http import HttpResponse

    from .models import Reserva

    # Create your views here.

    def home_view(request):
        return render(request, "bookings/home.html")
    ```

## Modelos

Después de agregar o modificar un modelo en `models.py` tenemos que correr 2 comandos:

1. `python manage.py makemigrations`
2. `python manage.py migrate`

