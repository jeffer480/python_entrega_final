from django.shortcuts import render, redirect
from django.http import HttpResponse

from .forms import ReservaCreateForm, ReservaSearchForm, RoomCreateForm, RoomSearchForm
from django.forms import TextInput, CheckboxInput, NumberInput, Textarea, Select
from .models import Reserva, Sala, Comentario

def home_view(request):
    return render(request, "bookings/home.html")


# -------------------------------------bookings---------------------------------------

# def create_booking_view(request):
#     contexto = {"booking_create": ReservaCreateForm() }
#     return render(request, "bookings/form_create-room.html", contexto)

def create_booking_view(request):
    if request.method == "GET":
        contexto = {"booking_create": ReservaCreateForm() }
        return render(request, "bookings/form_create.html", contexto)
    elif request.method == "POST":
        form = ReservaCreateForm(request.POST)
        if form.is_valid():
            nombre_de_usuario = form.cleaned_data['nombre_de_usuario']
            sala = form.cleaned_data['sala']
            fecha = form.cleaned_data['fecha']
            hora_inicio = form.cleaned_data['hora_inicio']
            hora_fin = form.cleaned_data['hora_fin']
            descripcion = form.cleaned_data['descripcion']
            new_booking = Reserva(nombre_de_usuario=nombre_de_usuario, sala=sala, fecha=fecha, hora_inicio=hora_inicio, hora_fin=hora_fin, descripcion=descripcion)
            new_booking.save()
            return detail_view_bookings(request, new_booking.id)

def list_view_bookings(request):
    reservas = Reserva.objects.all()
    contexto_dict = {'todas_las_reservas': reservas}
    return render(request, "bookings/list.html", contexto_dict)

def detail_view_bookings(request, booking_id):
    reserva = Reserva.objects.get(id=booking_id)
    contexto_dict = {"reserva": reserva}
    return render(request, "bookings/detail.html", contexto_dict)

def search_view_bookings(request):
    if request.method == "GET":
        form = ReservaSearchForm()
        return render(request, "bookings/form-search.html", context={"search_form": form})
    elif request.method == "POST":
        #  devolverle a "chrome" la lista de reservas encontrada o avisar que no se encontró nada
        form = ReservaSearchForm(request.POST)
        if form.is_valid():
            nombre_de_usuario = form.cleaned_data['nombre_de_usuario']
        reservas_del_usuario = Reserva.objects.filter(nombre_de_usuario=nombre_de_usuario).all()
        contexto_dict = {"todas_las_reservas": reservas_del_usuario}
        return render(request, "bookings/list.html", contexto_dict)


# --------------------------------CRUD Rooms----------------------------------
# Create
def create_room_view(request):
    if request.method == "GET":
        contexto = {"room_create": RoomCreateForm()}
        return render(request, "rooms/form_create.html", contexto)
    elif request.method == "POST":
        form = RoomCreateForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            disponible = form.cleaned_data['disponible']
            capacidad = form.cleaned_data['capacidad']
            descripcion = form.cleaned_data['descripcion']
            nueva_sala = Sala(nombre=nombre, disponible=disponible, capacidad=capacidad, descripcion=descripcion)
            nueva_sala.save()
            return detail_room_view(request, nueva_sala.id)
# Read
def detail_room_view(request, room_id):
    sala = Sala.objects.get(id=room_id)
    contexto_dict = {"todas_las_sala": sala}
    return render(request, "rooms/detail.html", contexto_dict)

def list_room_view(request):
    all_the_rooms = Sala.objects.all()
    contexto = {"list_rooms": all_the_rooms}
    return render(request, "rooms/list.html", contexto)
# Update
def update_room_view(request, room_id):
    room_to_edit = Sala.objects.filter(id=room_id).first()
    if request.method == "GET":
        valores_iniciales = {
            "nombre": room_to_edit.nombre,
            "disponible": room_to_edit.disponible,
            "capacidad": room_to_edit.capacidad,
            "descripcion": room_to_edit.descripcion
        }
        formulario = RoomCreateForm(initial=valores_iniciales)
        contexto = {
            "edit_room": formulario,
            "OBJETO": room_to_edit
        }
        return render(request, "rooms/form_update.html", contexto)
    elif request.method == "POST":
        form = RoomCreateForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            disponible = form.cleaned_data['disponible']
            capacidad = form.cleaned_data['capacidad']
            descripcion = form.cleaned_data['descripcion']
            room_to_edit.nombre = nombre
            room_to_edit.disponible = disponible
            room_to_edit.capacidad = capacidad
            room_to_edit.descripcion = descripcion
            room_to_edit.save()
            return redirect("room_detail", room_to_edit.id)
# Delete
def delete_room_view(request, room_id):
    sala_a_borrar = Sala.objects.filter(id=room_id).first()
    sala_a_borrar.delete()
    return redirect("room_list")

def search_room_view(request):
    if request.method == "GET":
        form = RoomSearchForm()
        return render(request, "rooms/form-search.html", context={"search_form": form})
    elif request.method == "POST":
        #  devolverle a "chrome" la lista de reservas encontrada o avisar que no se encontró nada
        form = RoomSearchForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
        rooms = Sala.objects.filter(nombre=nombre).all()
        contexto_dict = {"list_rooms": rooms}
        return render(request, "rooms/list.html", contexto_dict)
    

# ----------------------------------------Vistas basadas en clases "VBC"------------------------------------

from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from django.views.generic.edit import CreateView

class RoomListView(ListView):
    model = Sala
    template_name = 'vbc/room_list.html'
    context_object_name = 'list_room_vbc'

class RoomDetailView(DetailView):
    model = Sala
    template_name = 'vbc/room_detail.html'
    context_object_name = 'detail_room_vbc'

class RoomCreateView(CreateView):
    model = Sala
    template_name = 'vbc/room_form.html'
    fields = ['nombre', 'disponible', 'capacidad', 'descripcion']
    success_url = reverse_lazy('vbc_room_list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)  # Obtén el formulario estándar
        form.fields['nombre'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Ingrese una sala ej: Literatura'})
        form.fields['disponible'].widget.attrs.update({'class': 'form-check-input'})
        form.fields['capacidad'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Ingrese cantidad'})
        form.fields['descripcion'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Ingrese una breve descripción', 'rows': '5'})
        return form

class RoomUpdateView(UpdateView):
    model = Sala
    template_name = 'vbc/room_form.html'
    fields = ['nombre', 'disponible', 'capacidad', 'descripcion']
    context_object_name = 'sala'
    success_url = reverse_lazy('vbc_room_list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)  # Obtén el formulario estándar
        form.fields['nombre'].widget.attrs.update({'class': 'form-control'})
        form.fields['disponible'].widget.attrs.update({'class': 'form-check-input'})
        form.fields['capacidad'].widget.attrs.update({'class': 'form-control'})
        form.fields['descripcion'].widget.attrs.update({'class': 'form-control', 'rows': '5'})
        return form

class RoomDeleteView(DeleteView):
    model = Sala
    template_name = 'vbc/room_confirm_delete.html'
    success_url = reverse_lazy('vbc_room_list')


# --------------------------------Vistas basadas en clases "VBC" CATEGORY------------------------------------

class listCommentView(ListView):
    model = Comentario
    template_name = 'comment/comment_list.html'
    context_object_name = 'list_comment_vbc'

class CommentCreateView(CreateView):
    model = Comentario
    template_name = 'comment/comment_form.html'
    fields = ['sala', 'texto', 'calificacion']
    success_url = reverse_lazy('comment_list')

    # def get_form(self, form_class=None):
    #     form = super().get_form(form_class)  # Obtén el formulario estándar
    #     form.fields['sala'].widget.attrs.update({'class': 'form-select'})
    #     form.fields['texto'].widget.attrs.update({'class': 'form-control'})
    #     form.fields['calificacion'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Ingrese su calificación'})
    #     form.fields['fecha_publicacion'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Ingrese una breve descripción', 'rows': '5'})
    #     return form
    

