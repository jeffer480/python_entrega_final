from django import forms
from django.forms import TextInput, CheckboxInput, NumberInput, Textarea, EmailField

from .models import Reserva, Sala, Avatar

class RoomCreateForm(forms.ModelForm):
    class Meta:
        model = Sala
        fields = ['nombre', 'disponible', 'capacidad', 'descripcion']
        labels = {
            'nombre': 'Elegir un nombre para la Sala',
            'disponible': 'Disponible',
            'capacidad': 'Capacidad máxima',
            'descripcion': 'Descripción',
        }
        widgets = {
            'nombre': TextInput(attrs={'class': 'form-control','placeholder': 'Ingrese una sala ej: Literatura'}),
            'disponible': CheckboxInput(attrs={'class': 'form-check-input',}),
            'capacidad': NumberInput(attrs={'class': 'form-control','placeholder': 'Ingrese cantidad','style': 'width: 320px;'}),
            'descripcion': Textarea(attrs={'class': 'form-control','placeholder': 'Ingrese una breve descripción','rows': 5}),
        }

class RoomSearchForm(forms.Form):
    nombre = forms.CharField(max_length=50, required=True, label="Ingresar nombre de la sala", widget=forms.TextInput(attrs={'placeholder': 'Ingrese nombre a buscar ej. literatura', 'class': 'form-control mt-3'}))
    
# --------------------------------------form bookins------------------------------------------

class ReservaCreateForm(forms.Form):
    pass

class ReservaCreateForm(forms.ModelForm):
    class Meta:
        model = Reserva
        # Specifying which fields should appear in the form, including 'sala'
        fields = ['nombre_de_usuario', 'sala', 'fecha', 'hora_inicio', 'hora_fin', 'descripcion']
        widgets = {
            'nombre_de_usuario': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Ingrese nombre ej: Jefferson Varela'}),
            'sala': forms.Select(attrs={'class': 'form-select','style': 'width: 320px;'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control','style': 'width: 320px;','type': 'date'}),
            'hora_inicio':forms.TimeInput(attrs={'class': 'form-control','style': 'width: 320px;','type': 'time'}),
            'hora_fin': forms.TimeInput(attrs={'class': 'form-control','style': 'width: 320px;','type': 'time'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control','placeholder': 'Ingrese una breve descripción','rows': 5}),
        }
        labels = {
            'nombre_de_usuario': 'Elegir un nombre de usuario para la reserva',
            'sala': 'Seleccione una sala',
            'fecha': 'Fecha',
            'hora_inicio': 'Hora de inicio',
            'hora_fin': 'Hora de finalización',
            'descripcion': 'Descripción de la reserva'
        }
    def __init__(self, *args, **kwargs):
        super(ReservaCreateForm, self).__init__(*args, **kwargs)
        self.fields['sala'].queryset = Sala.objects.filter(disponible=True) 
        self.fields['sala'].label = "Sala" 

# class ReservaSearchForm(forms.Form):
#     nombre_de_usuario = forms.CharField(max_length=50, required=False, label="Nombre de Usuario")
#     sala = forms.ModelChoiceField(queryset=Sala.objects.all(), required=False, label="Sala")

#     def __init__(self, *args, **kwargs):
#         super(ReservaSearchForm, self).__init__(*args, **kwargs)
#         self.fields['sala'].queryset = Sala.objects.filter(disponible=True) if self.data.get('disponible') else Sala.objects.all()

class ReservaSearchForm(forms.Form):
    nombre_de_usuario = forms.CharField(max_length=50, required=True, label="Ingresar nombre de usuario", widget=forms.TextInput(attrs={'placeholder': 'Ingrese un nombre ej. Jefferson', 'class': 'form-control'}))

# -----------------------------------------------editar user------------------------------------------------------
from django.contrib.auth.models import User

class UserEditForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'type': 'email'})

# -------------------crear usuario personalizado (por defecto no se hace esta class) ---------------------

from django.contrib.auth.forms import UserCreationForm
#from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')  # Campos que quieres personalizar

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Nombre de usuario'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Contraseña'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirmar contraseña'})


# -------------avatar
class AvatarCreateForm(forms.ModelForm):
    class Meta:
        model = Avatar
        fields = ['image']
        labels = {
            'image': 'Seleccione una imagen',
        }

    def __init__(self, *args, **kwargs):
        super(AvatarCreateForm, self).__init__(*args, **kwargs)
        self.fields['image'].widget.attrs.update({'class': 'form-control mt-3', 'placeholder': 'Seleccione una imagen'})


