from django import forms
from django.forms import TextInput, CheckboxInput, NumberInput, Textarea

from .models import Reserva, Sala

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
            'nombre': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese una sala ej: Literatura'
                }),
            'disponible': CheckboxInput(attrs={
                'class': 'form-check-input',
                }),
            'capacidad': NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese cantidad',
                'style': 'width: 320px;'
                }),
            'descripcion': Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese una breve descripción',
                'rows': 5
                }),
        }

class RoomSearchForm(forms.Form):
    nombre = forms.CharField(max_length=50, required=True, label="Ingresar nombre de la sala", widget=forms.TextInput(attrs={'placeholder': 'Ingrese nombre a buscar ej. literatura', 'class': 'form-control'}))
    
# --------------------------------------form bookins------------------------------------------

class ReservaCreateForm(forms.Form):
    pass

class ReservaCreateForm(forms.ModelForm):
    class Meta:
        model = Reserva
        # Specifying which fields should appear in the form, including 'sala'
        fields = ['nombre_de_usuario', 'sala', 'fecha', 'hora_inicio', 'hora_fin', 'descripcion']
        widgets = {
            'nombre_de_usuario': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese nombre ej: Jefferson Varela'
                }),
            'sala': forms.Select(attrs={
                'class': 'form-select',
                'style': 'width: 320px;'
                }),
            'fecha': forms.DateInput(attrs={
                'class': 'form-control',
                'style': 'width: 320px;',
                'type': 'date'
                }),
            'hora_inicio':forms.TimeInput(attrs={
                'class': 'form-control',
                'style': 'width: 320px;',
                'type': 'time'
                }),
            'hora_fin': forms.TimeInput(attrs={
                'class': 'form-control',
                'style': 'width: 320px;',
                'type': 'time'
                }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese una breve descripción',
                'rows': 5
                }),
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
        # Optionally, you can further customize the 'sala' field here, for example:
        self.fields['sala'].queryset = Sala.objects.filter(disponible=True)  # Limit choices to available rooms
        self.fields['sala'].label = "Sala"  # Customize the field label
        # Any other field customizations can be done here

# class ReservaSearchForm(forms.Form):
#     nombre_de_usuario = forms.CharField(max_length=50, required=False, label="Nombre de Usuario")
#     sala = forms.ModelChoiceField(queryset=Sala.objects.all(), required=False, label="Sala")

#     def __init__(self, *args, **kwargs):
#         super(ReservaSearchForm, self).__init__(*args, **kwargs)
#         self.fields['sala'].queryset = Sala.objects.filter(disponible=True) if self.data.get('disponible') else Sala.objects.all()

class ReservaSearchForm(forms.Form):
    nombre_de_usuario = forms.CharField(max_length=50, required=True, label="Ingresar nombre de usuario", widget=forms.TextInput(attrs={'placeholder': 'Ingrese un nombre ej. Jefferson', 'class': 'form-control'}))