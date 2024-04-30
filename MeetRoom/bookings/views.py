from django.shortcuts import render, redirect
from django.http import HttpResponse

from .forms import ReservaCreateForm, ReservaSearchForm, RoomCreateForm, RoomSearchForm, CustomUserCreationForm
from django.forms import TextInput, CheckboxInput, NumberInput, Textarea, Select
from .models import Reserva, Sala, Comentario

from django.contrib.auth.decorators import login_required


# -------------------------------------bookings---------------------------------------

# def create_booking_view(request):
#     contexto = {"booking_create": ReservaCreateForm() }
#     return render(request, "bookings/form_create-room.html", contexto)

def home_view(request):
    return render(request, "bookings/home.html")

@login_required
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

@login_required
def list_view_bookings(request):
    reservas = Reserva.objects.all()
    contexto_dict = {'todas_las_reservas': reservas}
    return render(request, "bookings/list.html", contexto_dict)

@login_required
def detail_view_bookings(request, booking_id):
    reserva = Reserva.objects.get(id=booking_id)
    contexto_dict = {"reserva": reserva}
    return render(request, "bookings/detail.html", contexto_dict)

@login_required
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
@login_required
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
@login_required
def detail_room_view(request, room_id):
    sala = Sala.objects.get(id=room_id)
    contexto_dict = {"todas_las_sala": sala}
    return render(request, "rooms/detail.html", contexto_dict)

@login_required
def list_room_view(request):
    all_the_rooms = Sala.objects.all()
    contexto = {"list_rooms": all_the_rooms}
    return render(request, "rooms/list.html", contexto)

# Update
@login_required
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
@login_required
def delete_room_view(request, room_id):
    sala_a_borrar = Sala.objects.filter(id=room_id).first()
    sala_a_borrar.delete()
    return redirect("room_list")

@login_required
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
from django.contrib.auth.mixins import LoginRequiredMixin

class RoomListView(LoginRequiredMixin, ListView):
    model = Sala
    template_name = 'vbc/room_list.html'
    context_object_name = 'list_room_vbc'

class RoomDetailView(LoginRequiredMixin, DetailView):
    model = Sala
    template_name = 'vbc/room_detail.html'
    context_object_name = 'detail_room_vbc'

class RoomCreateView(LoginRequiredMixin, CreateView):
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

class RoomUpdateView(LoginRequiredMixin, UpdateView):
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


# --------------------------------Vistas basadas en clases "VBC" Comentarios------------------------------------

class CommentListView(ListView):
    model = Comentario
    template_name = 'comment/comment_list.html'
    context_object_name = 'list_comment_vbc'

class MyCommentsListView(ListView):
    model = Comentario
    template_name = 'comment/comment_my_list.html'
    context_object_name = 'comentarios_por_sala'

    def get_queryset(self):
        # Obtener los comentarios del usuario actual
        comentarios_del_usuario = Comentario.objects.filter(usuario=self.request.user)
        # Agrupar los comentarios por sala
        comentarios_por_sala = {}
        for comentario in comentarios_del_usuario:
            sala_id = comentario.sala.id
            if sala_id not in comentarios_por_sala:
                comentarios_por_sala[sala_id] = []
            comentarios_por_sala[sala_id].append(comentario)
        
        return comentarios_por_sala

class MisComentariosListView(LoginRequiredMixin, ListView):
    model = Comentario
    template_name = 'mis_comentarios.html'
    context_object_name = 'comentarios_por_sala'

    def get_queryset(self):
        # Obtener los comentarios del usuario actual
        comentarios_del_usuario = Comentario.objects.filter(usuario=self.request.user)
        
        # Agrupar los comentarios por sala
        comentarios_por_sala = {}
        for comentario in comentarios_del_usuario:
            sala_id = comentario.sala.id
            if sala_id not in comentarios_por_sala:
                comentarios_por_sala[sala_id] = []
            comentarios_por_sala[sala_id].append(comentario)
        
        return comentarios_por_sala


    
class CommentDetailView(LoginRequiredMixin, DetailView):
    model = Comentario
    template_name = 'comment/comment_detail.html'
    context_object_name = 'comment_detail_context'

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comentario
    template_name = 'comment/comment_form.html'
    fields = ['sala', 'contenido', 'calificacion']
    success_url = reverse_lazy('comment_list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)  # Obtén el formulario estándar
        form.fields['sala'].widget.attrs.update({'class': 'form-select', 'placeholder': 'Ingrese una sala ej: Literatura', 'type': 'select'})
        form.fields['calificacion'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Ingrese cantidad', 'type': 'number'})
        form.fields['contenido'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Ingrese una breve descripción', 'rows': '5'})
        return form

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)
    
class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comentario
    template_name = 'comment/comment_form.html'
    fields = ['sala', 'contenido', 'calificacion']
    context_object_name = 'comentario'
    success_url = reverse_lazy('comment_list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)  # Obtén el formulario estándar
        form.fields['sala'].widget.attrs.update({'class': 'form-select', 'placeholder': 'Ingrese una sala ej: Literatura', 'type': 'select'})
        form.fields['calificacion'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Ingrese cantidad', 'type': 'number'})
        form.fields['contenido'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Ingrese una breve descripción', 'rows': '5'})
        return form

class CommentDeleteView(DeleteView):
    model = Comentario
    template_name = 'comment/comment_confirm_delete.html'
    success_url = reverse_lazy('comment_list')

    

#-----------------------------------------------------user login logout------------------------------------------
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .forms import UserEditForm
from django.contrib import messages

# ----------------iniciar sesion
def user_login_view(request):
    if request.method == "GET":
        form = AuthenticationForm()
        form.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Nombre de usuario'})
        form.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Contraseña'})
    elif request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.user_cache
            if user is not None:
                login(request, user)
                return redirect("booking_home")

    return render(request, "users/login.html", {"form_login": form})

# ----------------crear usuario
def user_creation_view(request):
    if request.method == "GET":
        #este es el form por defecto
        # form = UserCreationForm()
        # y este es el form personalizado que viene desde forms.py
        form = CustomUserCreationForm(request.POST)
    if request.method == "POST":
        #este es el form por defecto 
        # form = UserCreationForm(request.POST)
        # y este es el form personalizado que viene desde forms.py
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("booking_home")
    return render(request, "users/crear_usuario.html", {"form_create": form})

# ----------------cerrar sesion
def user_logout_view(request):
    logout(request)
    return redirect("login")

# ----------------editar usario

class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserEditForm
    template_name = 'users/user_edit_form.html'
    success_url = reverse_lazy('update_perfil')

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, '¡Perfil actualizado exitosamente!')
        return response

#-----------------------------avatar

from .models import Avatar
from .forms import AvatarCreateForm


def avatar_view(request):
    if request.method == "GET":
        contexto = {"PABLOCALA": AvatarCreateForm()}
    else:
        form = AvatarCreateForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data["image"]
            avatar_existente = Avatar.objects.filter(user=request.user)
            avatar_existente.delete()
            nuevo_avatar = Avatar(image=image, user=request.user)
            nuevo_avatar.save()
            return redirect("booking_home")
        else:
            contexto = {"PABLOCALA": form}


    return render(request, "users/avatar_create.html", context=contexto)
